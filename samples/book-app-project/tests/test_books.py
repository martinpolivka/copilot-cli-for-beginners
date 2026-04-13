import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
import books
from books import BookCollection


@pytest.fixture(autouse=True)
def use_temp_data_file(tmp_path, monkeypatch):
    """Use a temporary data file for each test."""
    temp_file = tmp_path / "data.json"
    temp_file.write_text("[]")
    monkeypatch.setattr(books, "DATA_FILE", str(temp_file))


def test_add_book():
    collection = BookCollection()
    initial_count = len(collection.books)
    collection.add_book("1984", "George Orwell", 1949)
    assert len(collection.books) == initial_count + 1
    book = collection.find_book_by_title("1984")
    assert book is not None
    assert book.author == "George Orwell"
    assert book.year == 1949
    assert book.read is False

def test_mark_book_as_read():
    collection = BookCollection()
    collection.add_book("Dune", "Frank Herbert", 1965)
    result = collection.mark_as_read("Dune")
    assert result is True
    book = collection.find_book_by_title("Dune")
    assert book.read is True

def test_mark_book_as_read_invalid():
    collection = BookCollection()
    result = collection.mark_as_read("Nonexistent Book")
    assert result is False

def test_remove_book():
    collection = BookCollection()
    collection.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    result = collection.remove_book("The Hobbit")
    assert result is True
    book = collection.find_book_by_title("The Hobbit")
    assert book is None

def test_remove_book_invalid():
    collection = BookCollection()
    result = collection.remove_book("Nonexistent Book")
    assert result is False


# --- Search, filter, and sort tests ---

def _populated_collection():
    """Helper to create a collection with sample books."""
    c = BookCollection()
    c.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
    c.add_book("1984", "George Orwell", 1949)
    c.add_book("Dune", "Frank Herbert", 1965)
    c.add_book("To Kill a Mockingbird", "Harper Lee", 1960)
    c.mark_as_read("1984")
    return c


def test_search_by_keyword_title():
    c = _populated_collection()
    results = c.search_books(query="hobbit")
    assert len(results) == 1
    assert results[0].title == "The Hobbit"


def test_search_by_keyword_author():
    c = _populated_collection()
    results = c.search_books(query="orwell")
    assert len(results) == 1
    assert results[0].title == "1984"


def test_search_case_insensitive():
    c = _populated_collection()
    results = c.search_books(query="DUNE")
    assert len(results) == 1


def test_search_no_match():
    c = _populated_collection()
    results = c.search_books(query="nonexistent")
    assert len(results) == 0


def test_filter_read():
    c = _populated_collection()
    results = c.search_books(read_status=True)
    assert all(b.read for b in results)
    assert len(results) == 1


def test_filter_unread():
    c = _populated_collection()
    results = c.search_books(read_status=False)
    assert all(not b.read for b in results)
    assert len(results) == 3


def test_filter_exact_year():
    c = _populated_collection()
    results = c.search_books(year=1965)
    assert len(results) == 1
    assert results[0].title == "Dune"


def test_filter_year_range():
    c = _populated_collection()
    results = c.search_books(year_from=1940, year_to=1965)
    assert len(results) == 3
    titles = {b.title for b in results}
    assert "The Hobbit" not in titles


def test_sort_by_year():
    c = _populated_collection()
    results = c.search_books(sort_by="year")
    years = [b.year for b in results]
    assert years == sorted(years)


def test_sort_by_title():
    c = _populated_collection()
    results = c.search_books(sort_by="title")
    titles = [b.title for b in results]
    assert titles == sorted(titles)


def test_sort_by_author():
    c = _populated_collection()
    results = c.search_books(sort_by="author")
    authors = [b.author for b in results]
    assert authors == sorted(authors)


def test_combined_search_and_filter():
    c = _populated_collection()
    results = c.search_books(query="the", read_status=False)
    assert all(not b.read for b in results)
    assert all("the" in b.title.lower() or "the" in b.author.lower() for b in results)


def test_search_no_filters_returns_all():
    c = _populated_collection()
    results = c.search_books()
    assert len(results) == 4


# --- get_unread_books tests ---

class TestGetUnreadBooks:
    """Tests for BookCollection.get_unread_books."""

    # -- Happy path --

    def test_returns_only_unread_books(self):
        c = _populated_collection()
        results = c.get_unread_books()
        assert all(not b.read for b in results)

    def test_returns_correct_count(self):
        c = _populated_collection()
        results = c.get_unread_books()
        assert len(results) == 3

    def test_excludes_read_books(self):
        c = _populated_collection()
        titles = {b.title for b in c.get_unread_books()}
        assert "1984" not in titles

    def test_includes_expected_unread_titles(self):
        c = _populated_collection()
        titles = {b.title for b in c.get_unread_books()}
        assert titles == {"The Hobbit", "Dune", "To Kill a Mockingbird"}

    # -- Edge cases --

    def test_empty_collection_returns_empty(self):
        c = BookCollection()
        assert c.get_unread_books() == []

    def test_all_books_read_returns_empty(self):
        c = _populated_collection()
        for book in c.books:
            c.mark_as_read(book.title)
        assert c.get_unread_books() == []

    def test_no_books_read_returns_all(self):
        c = BookCollection()
        c.add_book("Dune", "Frank Herbert", 1965)
        c.add_book("The Hobbit", "J.R.R. Tolkien", 1937)
        assert len(c.get_unread_books()) == 2

    def test_single_unread_book(self):
        c = BookCollection()
        c.add_book("Dune", "Frank Herbert", 1965)
        results = c.get_unread_books()
        assert len(results) == 1
        assert results[0].title == "Dune"

    def test_single_read_book_returns_empty(self):
        c = BookCollection()
        c.add_book("Dune", "Frank Herbert", 1965)
        c.mark_as_read("Dune")
        assert c.get_unread_books() == []

    # -- Return type and data integrity --

    def test_returns_list(self):
        c = _populated_collection()
        assert isinstance(c.get_unread_books(), list)

    def test_returns_book_objects(self):
        c = _populated_collection()
        results = c.get_unread_books()
        assert all(isinstance(b, books.Book) for b in results)

    def test_does_not_mutate_collection(self):
        c = _populated_collection()
        original_count = len(c.books)
        c.get_unread_books()
        assert len(c.books) == original_count

    # -- Integration: interacts correctly with mark_as_read --

    def test_marking_book_read_removes_from_unread(self):
        c = _populated_collection()
        assert "Dune" in {b.title for b in c.get_unread_books()}
        c.mark_as_read("Dune")
        assert "Dune" not in {b.title for b in c.get_unread_books()}

    def test_count_decreases_after_marking_read(self):
        c = _populated_collection()
        before = len(c.get_unread_books())
        c.mark_as_read("Dune")
        assert len(c.get_unread_books()) == before - 1

    # -- Integration: consistent with search_books --

    def test_matches_search_books_unread_filter(self):
        c = _populated_collection()
        unread = c.get_unread_books()
        search = c.search_books(read_status=False)
        assert [b.title for b in unread] == [b.title for b in search]

    # -- Persistence: survives reload --

    def test_unread_persists_after_reload(self):
        c = _populated_collection()
        unread_titles = {b.title for b in c.get_unread_books()}
        reloaded = BookCollection()
        assert {b.title for b in reloaded.get_unread_books()} == unread_titles
