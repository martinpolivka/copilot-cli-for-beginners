import sys
from books import BookCollection


# Global collection instance
collection = BookCollection()


def show_books(books):
    """Display books in a user-friendly format."""
    if not books:
        print("No books found.")
        return

    print("\nYour Book Collection:\n")

    for index, book in enumerate(books, start=1):
        status = "✓" if book.read else " "
        print(f"{index}. [{status}] {book.title} by {book.author} ({book.year})")

    print()


def handle_list():
    books = collection.list_books()
    show_books(books)


def handle_add():
    print("\nAdd a New Book\n")

    title = input("Title: ").strip()
    author = input("Author: ").strip()
    year_str = input("Year: ").strip()

    try:
        year = int(year_str) if year_str else 0
        collection.add_book(title, author, year)
        print("\nBook added successfully.\n")
    except ValueError as e:
        print(f"\nError: {e}\n")


def handle_remove():
    print("\nRemove a Book\n")

    title = input("Enter the title of the book to remove: ").strip()
    collection.remove_book(title)

    print("\nBook removed if it existed.\n")


def handle_mark_read():
    print("\nMark a Book as Read\n")

    title = input("Enter the title of the book: ").strip()
    result = collection.mark_as_read(title)

    if result:
        print("\nBook marked as read.\n")
    else:
        print("\nBook not found.\n")


def handle_list_unread():
    books = collection.get_unread_books()
    show_books(books)


def handle_find():
    print("\nFind Books by Author\n")

    author = input("Author name: ").strip()
    books = collection.find_by_author(author)

    show_books(books)


def handle_search():
    """Handle the search command with composable flags."""
    args = sys.argv[2:]

    query = None
    read_status = None
    year = None
    year_from = None
    year_to = None
    sort_by = None

    i = 0
    while i < len(args):
        arg = args[i]
        if arg == "--read":
            read_status = True
        elif arg == "--unread":
            read_status = False
        elif arg == "--year" and i + 1 < len(args):
            i += 1
            year = int(args[i])
        elif arg == "--from" and i + 1 < len(args):
            i += 1
            year_from = int(args[i])
        elif arg == "--to" and i + 1 < len(args):
            i += 1
            year_to = int(args[i])
        elif arg == "--sort" and i + 1 < len(args):
            i += 1
            sort_by = args[i]
        elif not arg.startswith("--"):
            query = arg
        i += 1

    books = collection.search_books(
        query=query,
        read_status=read_status,
        year=year,
        year_from=year_from,
        year_to=year_to,
        sort_by=sort_by,
    )
    show_books(books)


def show_help():
    print("""
Book Collection Helper

Commands:
  list         - Show all books
  list-unread  - Show only unread books
  add          - Add a new book
  remove       - Remove a book by title
  find         - Find books by author
  search       - Search, filter, and sort books
  mark-read    - Mark a book as read
  help         - Show this help message

Search options:
  search <keyword>       - Search by title or author
  search --read          - Show only read books
  search --unread        - Show only unread books
  search --year 1965     - Filter by exact year
  search --from 1940     - Filter from year (inclusive)
  search --to 1970       - Filter to year (inclusive)
  search --sort title    - Sort by title, author, or year

  Options can be combined:
  search tolkien --unread --sort year
""")


def main():
    if len(sys.argv) < 2:
        show_help()
        return

    command = sys.argv[1].lower()

    if command == "list":
        handle_list()
    elif command == "list-unread":
        handle_list_unread()
    elif command == "add":
        handle_add()
    elif command == "remove":
        handle_remove()
    elif command == "find":
        handle_find()
    elif command == "search":
        handle_search()
    elif command == "mark-read":
        handle_mark_read()
    elif command == "help":
        show_help()
    else:
        print("Unknown command.\n")
        show_help()


if __name__ == "__main__":
    main()
