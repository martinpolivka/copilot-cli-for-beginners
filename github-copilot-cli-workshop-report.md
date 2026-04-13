# GitHub Copilot CLI: Workshop Preparation Guide for Eurowag

## Executive Summary

GitHub Copilot CLI is a standalone, terminal-native AI coding assistant that brings the full power of GitHub Copilot's agentic capabilities directly to the command line. It replaced the older `gh copilot` extension (deprecated October 2025) and reached general availability in February 2026. Available on all Copilot plans -- including the free tier for personal accounts -- it enables developers to write, debug, review, and refactor code through natural language conversations without leaving the terminal. For .NET developers, it is especially powerful for automating `dotnet` CLI workflows, managing NuGet packages, running EF Core migrations, containerizing applications, and modernizing legacy .NET Framework projects.

This document covers everything needed to build a 2-hour workshop presentation: what Copilot CLI is and how it works, its benefits, how it compares to IDE-based Copilot, practical .NET demo scenarios, a step-by-step getting started guide, and best practices.

---

## Table of Contents

1. [What is GitHub Copilot CLI](#1-what-is-github-copilot-cli)
2. [Benefits of GitHub Copilot CLI](#2-benefits-of-github-copilot-cli)
3. [CLI vs IDE Copilot Comparison](#3-cli-vs-ide-copilot-comparison)
4. [.NET-Specific Demo Scenarios](#4-net-specific-demo-scenarios)
5. [Getting Started Guide](#5-getting-started-guide)
6. [Best Practices and Tips](#6-best-practices-and-tips)
7. [Sources](#7-sources)

---

## 1. What is GitHub Copilot CLI

### Overview

GitHub Copilot CLI is a **terminal-native AI coding assistant** that runs directly in your shell. Unlike the older `gh copilot` extension (which only offered single-shot `suggest` and `explain` commands), the new Copilot CLI is a full **agentic assistant** that can:

- Hold multi-turn conversations with context memory
- Read, analyze, and edit files in your project
- Execute shell commands on your behalf (with permission)
- Generate implementation plans and execute them
- Work with GitHub issues, pull requests, and branches natively via MCP
- Run tasks autonomously in autopilot mode
- Delegate work to cloud-based coding agents

[GitHub Copilot CLI 101](https://github.blog/ai-and-ml/github-copilot-cli-101-how-to-use-github-copilot-from-the-command-line/) | [GitHub Docs](https://docs.github.com/en/copilot/how-tos/copilot-cli)

### Historical Context: The Two Copilot CLIs

**Confidence: HIGH**

It is important to understand the evolution because some older documentation still references the legacy tool:

| Aspect | Legacy `gh copilot` Extension | New Copilot CLI (Current) |
|--------|-------------------------------|---------------------------|
| **Status** | Deprecated October 25, 2025 | GA February 25, 2026 |
| **Install** | `gh extension install github/gh-copilot` | `npm install -g @github/copilot` or `brew install copilot-cli` or `winget install GitHub.Copilot` |
| **Launch** | `gh copilot suggest` / `gh copilot explain` | `copilot` (interactive session) |
| **Interaction** | Single command, single response | Full conversation with persistent context |
| **Code editing** | Not supported | Can read, analyze, and edit files |
| **Shell commands** | Suggests commands only | Can execute commands (with permission) |
| **Model selection** | Fixed model | `/model` to switch between Claude Sonnet 4.5, Opus 4.5, GPT-5.2, and others |
| **MCP support** | None | Full MCP server integration |
| **GitHub integration** | Basic | Native PRs, issues, actions, coding agent |

As of January 2026, running `gh copilot` via the GitHub CLI automatically installs and launches the new Copilot CLI, so the transition is seamless for existing `gh` users.

[Deprecation announcement](https://github.blog/changelog/2025-09-25-upcoming-deprecation-of-gh-copilot-cli-extension/) | [gh copilot now launches new CLI](https://github.blog/changelog/2026-01-21-install-and-use-github-copilot-cli-directly-from-the-github-cli/)

### Key Commands and Interactions

**Confidence: HIGH**

**Command-line commands (before entering interactive mode):**

| Command | Purpose |
|---------|---------|
| `copilot` | Launch the interactive user interface |
| `copilot -p "prompt"` | One-shot mode: send a prompt directly |
| `copilot --continue` | Resume the most recent session |
| `copilot --resume` | Browse and select a previous session |
| `copilot init` | Initialize custom instructions for a repository |
| `copilot login` | Authenticate with GitHub via OAuth device flow |
| `copilot update` | Download and install the latest version |
| `copilot version` | Display version information |

[CLI Command Reference](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)

**Slash commands (inside interactive mode):**

| Command | Purpose |
|---------|---------|
| `/plan` | Create a structured implementation plan before coding |
| `/model` | Switch between available AI models |
| `/review` | Run code review on current changes |
| `/clear` or `/new` | Clear conversation history and start fresh |
| `/delegate` | Offload work to run in the cloud via Copilot coding agent |
| `/fleet` | Break a task into parallel subtasks run by subagents |
| `/agent` | Browse and select from available agents |
| `/add-dir PATH` | Add a directory to the allowed list for file access |
| `/context` | Visualize current context usage |
| `/session` | View current session info |
| `/compact` | Manually trigger context compaction |
| `/experimental` | Access preview features (e.g., Rubber Duck) |
| `/plugin` | Manage plugins and marketplaces |
| `/login` | Authenticate with GitHub |
| `/help` | Display help information |

[Slash Commands Cheat Sheet](https://github.blog/ai-and-ml/github-copilot/a-cheat-sheet-to-slash-commands-in-github-copilot-cli/)

**Key keyboard shortcuts:**

| Shortcut | Purpose |
|----------|---------|
| `Shift + Tab` | Cycle between standard, plan, and autopilot mode |
| `@ FILENAME` | Include file contents in context |
| `Ctrl + C` | Cancel operation / clear input (press twice to exit) |
| `Ctrl + D` | Shutdown |
| `Ctrl + L` | Clear the screen |
| `Ctrl + G` | Edit the prompt in an external editor |

### Three Interaction Modes

**Confidence: HIGH**

1. **Standard Mode** -- Copilot responds to prompts and asks for permission before taking actions. This is the default and recommended starting mode.

2. **Plan Mode** -- Copilot creates a structured implementation plan with checkboxes before writing any code. Activated by pressing `Shift+Tab` or using `/plan`. Best for complex, multi-file changes.

3. **Autopilot Mode** -- Copilot works autonomously on a task, carrying out multiple steps until the task is complete. Activated by pressing `Shift+Tab` twice from standard mode. Best for well-defined, lower-risk tasks.

[Microsoft DevBlog: Get started with Copilot CLI](https://developer.microsoft.com/blog/get-started-with-github-copilot-cli-a-free-hands-on-course)

### Supported Shells and Platforms

**Confidence: HIGH**

| Platform | Compatible Shells | Notes |
|----------|-------------------|-------|
| **Windows** | PowerShell Core (pwsh.exe), Windows PowerShell 5.1 (powershell.exe) | PowerShell v6+ recommended; cmd.exe and Git Bash have limited compatibility |
| **macOS** | Bash, Zsh | Both fully supported |
| **Linux** | Bash, Zsh | Both fully supported |
| **WSL** | Bash, Zsh | Recommended for best Windows experience |

[Installing GitHub Copilot CLI](https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli) | [Shell Compatibility](https://deepwiki.com/doggy8088/github-copilot-configs/5.1-shell-environment-configuration)

### Authentication Requirements

**Confidence: HIGH**

- An active **GitHub Copilot subscription** is required (Free, Pro, Pro+, Business, or Enterprise)
- Authentication is done via **OAuth device flow** -- on first launch, Copilot CLI prompts you to use `/login` and follow browser-based authentication
- For organization/enterprise users, the **Copilot CLI policy** must be enabled by the admin in organization settings
- No API keys need to be managed manually

[GitHub Docs: Authentication](https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli)

---

## 2. Benefits of GitHub Copilot CLI

### Speed of Complex CLI Operations

**Confidence: HIGH**

Copilot CLI eliminates the need to remember exact syntax for complex commands. Instead of searching Stack Overflow or documentation, developers describe what they want in natural language and get the correct command immediately.

**Example:** Instead of researching the exact flags for finding large files in a git repository, a developer types:
```
Find all files larger than 10MB that were changed in the last week
```
Copilot generates the appropriate `find` or `git log` command with the correct flags and syntax.

One developer reported cutting terminal workflow time by 40% after three months of daily use [Mastering GitHub Copilot CLI](https://www.promptfu.com/blog/github-copilot-cli-mastery-guide/). GitHub's own research found that developers using Copilot complete coding tasks up to 55% faster [GitHub Research](https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/).

### Learning New Tools

**Confidence: HIGH**

Copilot CLI acts as a contextual learning companion. When encountering unfamiliar tools or command-line utilities, developers can ask for explanations alongside suggestions. The `@` file reference feature lets you point Copilot at configuration files or scripts and ask it to explain what they do.

- "Explain the Dockerfile in this project" -- Copilot reads the file and provides a line-by-line breakdown
- "What does this CI pipeline do?" -- Copilot analyzes `.github/workflows/*.yml` and explains each step
- Every command suggestion includes explanations of what it does before execution

[GitHub Copilot CLI 101](https://github.blog/ai-and-ml/github-copilot-cli-101-how-to-use-github-copilot-from-the-command-line/)

### DevOps and CI/CD Pipeline Workflows

**Confidence: HIGH**

Copilot CLI supports programmatic/one-shot mode (`copilot -p "prompt"`) which enables automation in CI/CD pipelines, background jobs, and scripts. This extends AI-powered assistance beyond interactive development into operational workflows.

Use cases include:
- Generating deployment scripts
- Troubleshooting build failures
- Creating GitHub Actions workflows
- Managing Azure/AWS/GCP resources from the terminal
- Automating repetitive DevOps tasks

[LPains Blog: Copilot CLI Productivity](https://blog.lpains.net/posts/2025-11-24-github-copilot-cli/)

### No Context-Switching from Terminal

**Confidence: HIGH**

This is the foundational value proposition. Developers who work primarily in the terminal -- running builds, managing git, deploying services, inspecting logs -- no longer need to switch to a browser, IDE, or chat interface for AI assistance. The workflow stays in one place:

1. Clone a repository
2. Launch `copilot` in the project directory
3. Ask Copilot to explain the project layout
4. Have it set up your environment
5. Work through issues and features
6. Create a pull request

All without leaving the terminal.

[GitHub Blog: How to get started](https://github.blog/ai-and-ml/github-copilot/github-copilot-cli-how-to-get-started/)

### Discoverability of Flags and Options

**Confidence: HIGH**

Rather than reading through `man` pages or `--help` output to find the right flag combination, developers describe the desired behavior and Copilot suggests the exact command with appropriate flags. This is particularly valuable for:

- Complex `git` operations (rebase, cherry-pick, bisect)
- `docker` commands with numerous flags
- `dotnet` CLI commands with many options
- `kubectl` for Kubernetes management
- `az` / `aws` / `gcloud` CLI tools

### Natural Language to Shell Commands

**Confidence: HIGH**

The core interaction pattern is describing what you want in plain English and getting executable shell commands. Copilot CLI shows the command, explains what it does, and asks for confirmation before executing. This is fundamentally different from a chat interface -- the commands run in your actual shell environment with your actual files and state.

```
> Create a bash script to check for uncommitted changes and push if clean
```

Copilot writes the script, explains what it does, and offers to execute it.

[GitHub Copilot CLI 101](https://github.blog/ai-and-ml/github-copilot-cli-101-how-to-use-github-copilot-from-the-command-line/)

---

## 3. CLI vs IDE Copilot Comparison

### When CLI is Better

**Confidence: HIGH**

| Scenario | Why CLI Wins |
|----------|-------------|
| **Terminal-heavy workflows** | No context switching; you are already in the terminal running builds, git commands, and scripts |
| **CI/CD pipeline work** | One-shot mode (`copilot -p`) integrates into automation; IDE cannot run in pipelines |
| **Scripting and automation** | CLI can generate, explain, and execute shell scripts in their native environment |
| **Server administration / SSH** | When working on remote servers via SSH, there is no IDE -- CLI is the only option |
| **Quick one-off commands** | Asking "how do I find all files modified in the last 24 hours" is faster than opening an IDE |
| **Multi-repository work** | `/add-dir` lets you work across multiple repos simultaneously |
| **Codebase onboarding** | Quick exploration: "explain the layout of this project" without setting up an IDE |
| **Cloud/infrastructure work** | Managing Azure, AWS, Kubernetes directly from the terminal where `az`, `aws`, `kubectl` run |
| **Git operations** | Complex git workflows (rebasing, cherry-picking, conflict resolution) are terminal-native |
| **Delegating to cloud agents** | `/delegate` sends tasks to run asynchronously in the cloud |

### When IDE Copilot is Better

**Confidence: HIGH**

| Scenario | Why IDE Wins |
|----------|-------------|
| **Real-time code completion** | Ghost-text suggestions as you type -- sub-second latency, seamless in-editor experience |
| **Inline refactoring** | Selecting code and asking Copilot to refactor it in-place within the file |
| **Code navigation** | IDE provides go-to-definition, find references alongside Copilot suggestions |
| **Visual debugging** | Breakpoints, variable inspection, call stack -- IDE Copilot understands debugging context |
| **UI/frontend development** | Visual preview alongside code completion is irreplaceable |
| **Language-specific IntelliSense** | IDE combines Copilot with language server protocol for richer suggestions |
| **Project-wide refactoring** | IDE tools for rename, move, extract method are mature and deterministic |

### Complementary Use Cases: The Hybrid Workflow

**Confidence: HIGH**

The most effective approach is using both together. This is the most common pattern among experienced developers in 2026 [NxCode Comparison](https://www.nxcode.io/resources/news/cursor-vs-claude-code-vs-github-copilot-2026-ultimate-comparison).

**The recommended workflow for Eurowag's .NET teams:**

1. **Start in the CLI** -- Use `copilot` to explore a new codebase, create a `/plan`, set up the project structure
2. **Move to the IDE** -- Open VS Code or Visual Studio for active development with inline completions and refactoring
3. **Return to the CLI** -- Run tests, build, containerize, manage git, create PRs
4. **Delegate** -- Use `/delegate` for async tasks like documentation or refactoring separate modules

The CLI even has built-in IDE handoff: "Start in the CLI with a `/plan`, then open the work in VS Code to refine code directly" [GitHub Copilot CLI Features](https://github.com/features/copilot/cli/).

**Key differentiator:** Copilot CLI has **agentic capabilities** that IDE Copilot Chat does not fully replicate -- it can plan multi-step tasks, execute commands, work across multiple repositories, and delegate to cloud agents. IDE Copilot excels at the **moment-to-moment coding experience** with instant completions and contextual suggestions.

---

## 4. .NET-Specific Demo Scenarios

Below are 8 realistic developer scenarios using the `dotnet` CLI through Copilot CLI. Each includes the natural language prompt and the expected behavior.

### Scenario 1: Creating New Projects and Solutions

**Natural language prompt:**
```
Create a new .NET 9 Web API project called "Eurowag.FleetApi" with a solution file,
add a class library project "Eurowag.FleetApi.Core" for domain logic,
and a xUnit test project "Eurowag.FleetApi.Tests".
Wire them all up in the solution with appropriate project references.
```

**Expected Copilot CLI behavior:**

Copilot generates and executes a sequence of commands:
```bash
dotnet new sln -n Eurowag.FleetApi
dotnet new webapi -n Eurowag.FleetApi -o src/Eurowag.FleetApi
dotnet new classlib -n Eurowag.FleetApi.Core -o src/Eurowag.FleetApi.Core
dotnet new xunit -n Eurowag.FleetApi.Tests -o tests/Eurowag.FleetApi.Tests
dotnet sln add src/Eurowag.FleetApi/Eurowag.FleetApi.csproj
dotnet sln add src/Eurowag.FleetApi.Core/Eurowag.FleetApi.Core.csproj
dotnet sln add tests/Eurowag.FleetApi.Tests/Eurowag.FleetApi.Tests.csproj
dotnet add src/Eurowag.FleetApi/Eurowag.FleetApi.csproj reference src/Eurowag.FleetApi.Core/Eurowag.FleetApi.Core.csproj
dotnet add tests/Eurowag.FleetApi.Tests/Eurowag.FleetApi.Tests.csproj reference src/Eurowag.FleetApi/Eurowag.FleetApi.csproj
dotnet add tests/Eurowag.FleetApi.Tests/Eurowag.FleetApi.Tests.csproj reference src/Eurowag.FleetApi.Core/Eurowag.FleetApi.Core.csproj
```

**Workshop talking point:** This entire setup which normally takes 5-10 minutes of typing and remembering flags is done in seconds with a single natural language prompt.

### Scenario 2: Running Tests and Interpreting Failures

**Natural language prompt:**
```
Run all the tests in this solution. If any fail, explain what went wrong
and suggest a fix.
```

**Expected Copilot CLI behavior:**

Copilot runs:
```bash
dotnet test --verbosity normal
```

If tests fail, Copilot reads the output, identifies the failing test(s), reads the relevant test and source files using `@` references, and provides:
- An explanation of why each test failed
- A suggested code fix
- An offer to apply the fix directly

**Follow-up prompt:**
```
Run only the failed tests again to verify the fix worked.
```

Copilot generates:
```bash
dotnet test --filter "FullyQualifiedName~NameOfFailingTest"
```

**Workshop talking point:** Copilot CLI can read test output, correlate it with source code, and propose fixes -- a tight feedback loop without leaving the terminal.

### Scenario 3: Managing NuGet Packages

**Natural language prompt:**
```
Add Serilog with the console and file sinks to the Eurowag.FleetApi project.
Also add FluentValidation for the Core project.
```

**Expected Copilot CLI behavior:**
```bash
dotnet add src/Eurowag.FleetApi/Eurowag.FleetApi.csproj package Serilog
dotnet add src/Eurowag.FleetApi/Eurowag.FleetApi.csproj package Serilog.Sinks.Console
dotnet add src/Eurowag.FleetApi/Eurowag.FleetApi.csproj package Serilog.Sinks.File
dotnet add src/Eurowag.FleetApi.Core/Eurowag.FleetApi.Core.csproj package FluentValidation
```

**Additional prompt:**
```
Check all NuGet packages in the solution for known vulnerabilities
and outdated versions. Show me which ones need updating.
```

Expected behavior:
```bash
dotnet list package --vulnerable
dotnet list package --outdated
```

Copilot then reads the output and provides a summary table of packages that need attention.

**Workshop talking point:** Package management across a multi-project solution becomes conversational. No need to remember which package goes to which project or the exact package names.

### Scenario 4: Entity Framework Core Migrations

**Natural language prompt:**
```
I've added a new "Vehicle" entity to my DbContext. Create an EF Core migration
called "AddVehicleTable", show me what SQL it would generate, and then apply it
to my local database.
```

**Expected Copilot CLI behavior:**
```bash
dotnet ef migrations add AddVehicleTable --project src/Eurowag.FleetApi
dotnet ef migrations script --project src/Eurowag.FleetApi --idempotent
dotnet ef database update --project src/Eurowag.FleetApi
```

**Follow-up scenario:**
```
The last migration was wrong. Remove it and let me fix the entity first.
```

Expected:
```bash
dotnet ef migrations remove --project src/Eurowag.FleetApi
```

**Advanced follow-up:**
```
Scaffold the DbContext and entity classes from our existing SQL Server database
at "Server=localhost;Database=FleetDb;Trusted_Connection=true"
```

Expected:
```bash
dotnet ef dbcontext scaffold "Server=localhost;Database=FleetDb;Trusted_Connection=true" Microsoft.EntityFrameworkCore.SqlServer -o Models --context-dir Data -c FleetDbContext --project src/Eurowag.FleetApi
```

**Workshop talking point:** EF Core CLI commands have many flags that are hard to remember. Copilot translates intent ("scaffold from my database") into the exact command with the right flags.

[EF Core CLI Reference](https://learn.microsoft.com/en-us/ef/core/cli/dotnet)

### Scenario 5: Building and Publishing

**Natural language prompt:**
```
Build the solution in Release mode, then publish the API project as a
self-contained Linux x64 application to the ./publish directory.
Use trimming to minimize the output size.
```

**Expected Copilot CLI behavior:**
```bash
dotnet build Eurowag.FleetApi.sln --configuration Release
dotnet publish src/Eurowag.FleetApi/Eurowag.FleetApi.csproj \
  --configuration Release \
  --runtime linux-x64 \
  --self-contained true \
  -p:PublishTrimmed=true \
  --output ./publish
```

**Follow-up:**
```
Show me the size of the published output and list the largest files.
```

Copilot generates shell commands to analyze the output directory.

**Workshop talking point:** The `dotnet publish` command has dozens of options for runtime identifiers, self-contained vs framework-dependent, trimming, AOT, etc. Copilot CLI turns complex publish scenarios into plain English.

### Scenario 6: Docker Containerization

**Natural language prompt:**
```
Create a multi-stage Dockerfile for the Eurowag.FleetApi project.
Use the .NET 9 SDK for building and the ASP.NET runtime image for the final stage.
Expose port 8080, run as non-root user, and include a .dockerignore file.
```

**Expected Copilot CLI behavior:**

Copilot creates two files:

**Dockerfile:**
```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:9.0 AS build
WORKDIR /source
COPY . .
RUN dotnet restore
RUN dotnet publish src/Eurowag.FleetApi/Eurowag.FleetApi.csproj \
    -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:9.0
WORKDIR /app
COPY --from=build /app/publish .
USER $APP_UID
EXPOSE 8080
ENTRYPOINT ["dotnet", "Eurowag.FleetApi.dll"]
```

**.dockerignore:**
```
**/bin/
**/obj/
**/.git/
**/node_modules/
```

**Follow-up prompt:**
```
Build this Docker image, tag it as eurowag/fleet-api:latest,
and run it locally mapping port 8080.
```

Expected:
```bash
docker build -t eurowag/fleet-api:latest .
docker run -d -p 8080:8080 eurowag/fleet-api:latest
```

**Alternative prompt (using .NET SDK container publishing):**
```
Publish this project directly as a container image using the .NET SDK
without a Dockerfile.
```

Expected:
```bash
dotnet publish src/Eurowag.FleetApi/Eurowag.FleetApi.csproj \
  --os linux --arch x64 \
  -p:PublishProfile=DefaultContainer \
  -p:ContainerImageName=eurowag/fleet-api \
  -p:ContainerImageTag=latest
```

**Workshop talking point:** Copilot CLI knows both the traditional Dockerfile approach and the modern .NET SDK container publishing approach. It can help teams adopt whichever fits their workflow, and even the `containerize-aspnetcore` Copilot Skill is available as a plugin.

[Containerize .NET with dotnet publish](https://learn.microsoft.com/en-us/dotnet/core/containers/sdk-publish) | [containerize-aspnetcore Copilot Skill](https://explainx.ai/skills/github/awesome-copilot/containerize-aspnetcore)

### Scenario 7: Performance Profiling and Diagnostics

**Natural language prompt:**
```
My API endpoint /api/vehicles is slow. Help me diagnose the issue.
Start by collecting a CPU trace for 30 seconds while I send requests.
```

**Expected Copilot CLI behavior:**
```bash
dotnet tool install --global dotnet-trace
dotnet tool install --global dotnet-counters
dotnet-counters monitor --process-id <PID> --counters System.Runtime
```

Or for tracing:
```bash
dotnet-trace collect --process-id <PID> --duration 00:00:30 --output trace.nettrace
```

**Follow-up prompt:**
```
Show me the memory allocation profile. I suspect there's a memory leak
in the vehicle search endpoint.
```

Expected:
```bash
dotnet tool install --global dotnet-dump
dotnet-dump collect --process-id <PID> --output dump.dmp
dotnet-dump analyze dump.dmp
```

Or using `dotnet-gcdump`:
```bash
dotnet tool install --global dotnet-gcdump
dotnet-gcdump collect --process-id <PID> --output gc.gcdump
```

**Workshop talking point:** The .NET diagnostic tools (`dotnet-trace`, `dotnet-counters`, `dotnet-dump`, `dotnet-gcdump`) are powerful but have complex command-line interfaces. Copilot CLI translates "my endpoint is slow" into the appropriate diagnostic workflow.

### Scenario 8: .NET Modernization (Bonus)

**Natural language prompt (using the modernize-dotnet plugin):**
```
Upgrade my solution to .NET 10
```

**Expected Copilot CLI behavior (with the modernize-dotnet agent):**

1. **Assessment** -- Copilot analyzes the solution, identifies breaking changes, compatibility issues, and deprecated patterns. Generates `assessment.md`.
2. **Planning** -- Creates a detailed upgrade plan with sequenced tasks. Generates `plan.md`.
3. **Execution** -- Applies code transformations task by task.

Plugin setup:
```
/plugin marketplace add dotnet/modernize-dotnet
/plugin install modernize-dotnet@modernize-dotnet-plugins
/agent    (select modernize-dotnet)
```

Supported upgrade paths include: older .NET to latest, .NET Framework to modern .NET, and modernization of ASP.NET Core, Blazor, Azure Functions, WPF, Windows Forms, class libraries, and console apps.

**Workshop talking point:** This is a game-changer for teams maintaining legacy .NET Framework applications. The entire upgrade assessment and execution can be done from the terminal.

[Modernize .NET Anywhere with GitHub Copilot](https://devblogs.microsoft.com/dotnet/modernize-dotnet-anywhere-with-ghcp/) | [Microsoft Learn: Copilot Modernization](https://learn.microsoft.com/en-us/dotnet/core/porting/github-copilot-app-modernization/overview)

---

## 5. Getting Started Guide

### Prerequisites

| Prerequisite | Details |
|-------------|---------|
| **GitHub account** | Personal or organization account |
| **Copilot subscription** | Any plan: Free (personal), Pro ($10/mo), Pro+ ($39/mo), Business ($19/user/mo), Enterprise ($39/user/mo) |
| **Node.js 22+** | Required only for npm installation method |
| **PowerShell v6+** | Required only on Windows (native) |
| **Organization policy** | For Business/Enterprise, admin must enable "Copilot CLI" policy |

[GitHub Docs: Prerequisites](https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli)

### Step-by-Step Setup

#### Windows

**Option A: WinGet (Recommended for native Windows)**
```powershell
# Install Copilot CLI
winget install GitHub.Copilot

# Launch Copilot CLI in your project directory
cd C:\Projects\MyDotNetApp
copilot

# Authenticate when prompted
/login
```

**Option B: WSL (Recommended for best experience)**
```bash
# Install WSL if not already installed
wsl --install

# Inside WSL, install via script
curl -fsSL https://gh.io/copilot-install | bash

# Launch
cd /mnt/c/Projects/MyDotNetApp
copilot
```

**Option C: npm**
```powershell
# Requires Node.js 22+
npm install -g @github/copilot
copilot
```

#### macOS

**Option A: Homebrew (Recommended)**
```bash
brew install copilot-cli
cd ~/Projects/MyDotNetApp
copilot
```

**Option B: Install script**
```bash
curl -fsSL https://gh.io/copilot-install | bash
copilot
```

**Option C: npm**
```bash
npm install -g @github/copilot
copilot
```

#### Linux

**Option A: Homebrew**
```bash
brew install copilot-cli
copilot
```

**Option B: Install script**
```bash
curl -fsSL https://gh.io/copilot-install | bash
copilot
```

**Option C: npm**
```bash
npm install -g @github/copilot
copilot
```

### First Launch Walkthrough

1. **Navigate to your project directory** -- Copilot CLI reads files from the current directory and below
2. **Run `copilot`** -- The interactive interface starts
3. **Trust the folder** -- On first launch in a new directory, Copilot asks you to confirm you trust the files (since it may read, modify, and execute files)
4. **Authenticate** -- If not logged in, type `/login` and follow the browser-based OAuth flow
5. **Start interacting** -- Type a natural language prompt or use `/help` to see available commands

### Updating

```bash
# npm
npm update -g @github/copilot

# Homebrew
brew upgrade copilot-cli

# WinGet
winget upgrade GitHub.Copilot

# From within Copilot CLI
copilot update
```

[GitHub Docs: Installation](https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli) | [Codecademy Guide](https://www.codecademy.com/article/how-to-install-and-use-github-copilot-cli) | [InventiveHQ Guide](https://inventivehq.com/knowledge-base/copilot/how-to-install-github-copilot-cli)

---

## 6. Best Practices and Tips

### 1. Customize Your Environment with Instructions Files

**Confidence: HIGH**

Create a `.github/copilot-instructions.md` file in your repository to provide Copilot with project-specific context. This is especially important for .NET projects.

**Example for a .NET project:**
```markdown
## Build Commands
- `dotnet build` - Build the solution
- `dotnet test` - Run all tests
- `dotnet ef database update` - Apply pending EF migrations

## Code Style
- Use C# 12 features (primary constructors, collection expressions)
- Follow Microsoft naming conventions
- Use nullable reference types

## Architecture
- Clean Architecture: Core -> Infrastructure -> API
- Use MediatR for CQRS
- Use FluentValidation for input validation

## Workflow
- Run `dotnet format && dotnet test` after making changes
- Commit messages follow conventional commits format
```

Repository instructions always take precedence over global instructions, which allows teams to enforce conventions per project.

[GitHub Docs: Best Practices](https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices)

### 2. Use Plan Mode for Complex Tasks

**Confidence: HIGH**

Press `Shift+Tab` to enter plan mode before tackling multi-file changes, new features, or refactoring. Copilot will:
1. Analyze your request and codebase
2. Ask clarifying questions
3. Create a structured plan with checkboxes
4. Save the plan to `plan.md`
5. Wait for your approval before implementing

This produces dramatically better results than jumping straight to code, especially for tasks spanning 3+ files.

**The recommended workflow:**
```
Explore -> Plan -> Code -> Commit
```

### 3. Choose the Right Model for the Task

**Confidence: HIGH**

Use `/model` to switch models based on task complexity:

| Model | Best For |
|-------|---------|
| Claude Opus 4.5 | Complex architecture, difficult debugging, nuanced refactoring |
| Claude Sonnet 4.5 | Day-to-day coding, routine tasks (default, most cost-effective) |
| GPT-5.2 Codex | Code generation, code review, second opinions |

Switch mid-session as task complexity changes.

### 4. Leverage File References with @

**Confidence: HIGH**

Use the `@` operator to include specific files in your context:
```
Review @src/Eurowag.FleetApi/Controllers/VehicleController.cs for potential issues
```

This gives Copilot targeted context rather than relying on it to search the entire project.

### 5. Start Focused, Stay Focused

**Confidence: HIGH**

Use `/clear` or `/new` between unrelated tasks. While Copilot CLI supports infinite sessions with automatic compaction, focused sessions produce better results. Think of it as starting a fresh conversation with a colleague for each new topic.

### 6. Configure Tool Permissions Deliberately

**Confidence: HIGH**

Use permission flags to control what Copilot can do:
```bash
copilot --allow-tool='shell(dotnet:*)' --allow-tool='shell(git:*)' --deny-tool='shell(rm:*)'
```

For workshops and demos, `/allow-all` (alias `/yolo`) enables all permissions, but in production environments, use fine-grained permissions.

### 7. Use /delegate for Async Work

**Confidence: MODERATE** (requires Copilot cloud agent availability)

Offload non-critical tasks to run in the cloud while you continue working locally:
```
/delegate Add XML documentation comments to all public methods in the Core project
```

The cloud agent creates a pull request with the changes. Best for tangential work, documentation updates, and refactoring separate modules.

### 8. Leverage the Rubber Duck Experimental Feature

**Confidence: MODERATE** (experimental feature as of April 2026)

Use `/experimental` to enable Rubber Duck mode, which employs a second model from a different AI family to review the primary agent's work. Evaluations show Claude Sonnet + Rubber Duck (GPT-5.4) closes 74.7% of the performance gap between Sonnet and Opus, especially on complex multi-file tasks.

[GitHub Blog: Rubber Duck](https://github.blog/ai-and-ml/github-copilot/github-copilot-cli-combines-model-families-for-a-second-opinion/)

### 9. Use Multi-Repository Workflows

**Confidence: HIGH**

For microservices architectures, start Copilot from a parent directory or use `/add-dir`:
```
copilot
/add-dir /path/to/backend-service
/add-dir /path/to/shared-libs
```

This enables cross-cutting changes across multiple repositories in a single session.

### 10. Always Review Before Accepting

**Confidence: HIGH**

AI output is non-deterministic. Always review generated commands before letting Copilot execute them. Copilot CLI requires explicit approval for potentially destructive operations, but vigilance is still important.

Key review checklist:
- Does the command do what I expect?
- Are there any destructive operations (rm, DROP, force push)?
- Are connection strings or secrets being handled safely?
- Is the generated code following our team's patterns?

---

## Conclusion

GitHub Copilot CLI represents a significant evolution in how .NET developers can leverage AI assistance. It is not just a command suggestion tool -- it is a full agentic assistant that can plan, execute, and iterate on complex development tasks directly from the terminal.

For Eurowag's .NET teams, the key value drivers are:

1. **Reduced context switching** -- developers stay in the terminal for builds, tests, git, deployments, and now AI assistance
2. **Faster onboarding** -- new team members can explore codebases and understand project structures through natural language
3. **Complex command automation** -- EF migrations, NuGet management, Docker containerization, and publishing no longer require memorizing flags
4. **.NET modernization** -- the modernize-dotnet plugin provides an AI-guided path from .NET Framework to modern .NET
5. **Complementary to IDE Copilot** -- CLI for terminal workflows, IDE for code editing -- together they cover the full development lifecycle

The workshop should emphasize hands-on demo time, letting developers experience the flow of natural language to executed commands. The .NET scenarios in Section 4 are designed to be run live, building on each other from project creation through containerization.

---

## 7. Sources

1. GitHub Docs. "GitHub Copilot CLI Command Reference." https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference
2. Carroll, Jacklyn. "A cheat sheet to slash commands in GitHub Copilot CLI." GitHub Blog, January 21, 2026. https://github.blog/ai-and-ml/github-copilot/a-cheat-sheet-to-slash-commands-in-github-copilot-cli/
3. Wahlin, Dan. "Get started with GitHub Copilot CLI: A free, hands-on course." Microsoft Developer Blog, March 3, 2026. https://developer.microsoft.com/blog/get-started-with-github-copilot-cli-a-free-hands-on-course
4. Guzey, Vladislav. "GitHub Copilot CLI: The Complete Guide to Every Slash Command." proflead.dev, April 1, 2026. https://proflead.dev/posts/github-copilot-cli-tutorial-101/
5. Lietzke, Alexandra. "GitHub Copilot CLI 101: How to use GitHub Copilot from the command line." GitHub Blog, November 6, 2025. https://github.blog/ai-and-ml/github-copilot-cli-101-how-to-use-github-copilot-from-the-command-line/
6. GitHub Docs. "GitHub Copilot CLI How-tos." https://docs.github.com/en/copilot/how-tos/copilot-cli
7. GitHub Docs. "Installing GitHub Copilot CLI." https://docs.github.com/copilot/how-tos/set-up/install-copilot-cli
8. Griffiths, Andrea. "GitHub Copilot CLI: How to get started." GitHub Blog, October 13, 2025. https://github.blog/ai-and-ml/github-copilot/github-copilot-cli-how-to-get-started/
9. GitHub. "GitHub Copilot CLI Features Page." https://github.com/features/copilot/cli/
10. GitHub Docs. "Best practices for GitHub Copilot CLI." https://docs.github.com/en/copilot/how-tos/copilot-cli/cli-best-practices
11. GitHub Blog. "Upcoming deprecation of gh-copilot CLI extension." GitHub Changelog, September 25, 2025. https://github.blog/changelog/2025-09-25-upcoming-deprecation-of-gh-copilot-cli-extension/
12. GitHub Blog. "Install and Use GitHub Copilot CLI directly from the GitHub CLI." GitHub Changelog, January 21, 2026. https://github.blog/changelog/2026-01-21-install-and-use-github-copilot-cli-directly-from-the-github-cli/
13. Dumont, Mika. "Modernize .NET Anywhere with GitHub Copilot." .NET Blog, March 12, 2026. https://devblogs.microsoft.com/dotnet/modernize-dotnet-anywhere-with-ghcp/
14. McKenna, Nick and Perz, Bartek. "GitHub Copilot CLI combines model families for a second opinion." GitHub Blog, April 6, 2026. https://github.blog/ai-and-ml/github-copilot/github-copilot-cli-combines-model-families-for-a-second-opinion/
15. LPains. "GitHub Copilot CLI: Boost Developer Productivity in the Terminal." November 24, 2025. https://blog.lpains.net/posts/2025-11-24-github-copilot-cli/
16. PromptFu. "Mastering GitHub Copilot CLI: From Beginner to Power User." November 21, 2025. https://www.promptfu.com/blog/github-copilot-cli-mastery-guide/
17. Inventive HQ. "How to Migrate from Deprecated gh-copilot Extension to GitHub Copilot CLI." January 2026. https://inventivehq.com/knowledge-base/copilot/how-to-migrate-from-gh-copilot
18. Microsoft Learn. "Containerize an app with dotnet publish." https://learn.microsoft.com/en-us/dotnet/core/containers/sdk-publish
19. Microsoft Learn. "EF Core tools reference (.NET CLI)." https://learn.microsoft.com/en-us/ef/core/cli/dotnet
20. Codecademy. "How to Install and Use GitHub Copilot CLI [Complete Guide]." https://www.codecademy.com/article/how-to-install-and-use-github-copilot-cli
21. GitHub. "Research: quantifying GitHub Copilot's impact on developer productivity and happiness." September 7, 2022. https://github.blog/news-insights/research/research-quantifying-github-copilots-impact-on-developer-productivity-and-happiness/
22. Savage, Katie. "GitHub Copilot Dev Days." Microsoft Developer Blog, March 2, 2026. https://developer.microsoft.com/blog/github-copilot-dev-days
