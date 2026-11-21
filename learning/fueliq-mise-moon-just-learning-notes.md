# FuelIQ: Beginner's Guide to Setting Up mise, Moon, Just, uv, and FastAPI

A step-by-step guide for someone who is new to mise, Moon, Just, and
Python project tooling.

This guide explains **what each tool does, why it is useful, how to
install it, how to configure it, and how to check that it works**.

> **Target outcome:** Starting with a fresh FuelIQ repository inside a
> VS Code Dev Container, you will create a small FastAPI application and
> be able to install its tools, start the server, run tests, check code
> quality, and format code using simple commands.

------------------------------------------------------------------------

# Part 1 --- Understand what you are setting up

## 1. The problem this setup solves

Imagine a developer clones FuelIQ onto a new laptop.

They need to know:

-   Which Python version does the project use?
-   Which command-line tools must be installed?
-   Which Python packages does the application need?
-   How do they start the application?
-   How do they run tests?
-   How do they check code quality?
-   Will the project behave the same way on another developer's machine
    or in CI?

Without a consistent setup, each developer may install different
versions, use different commands, or miss a dependency. That can lead to
bugs that are difficult to reproduce.

We are going to make these requirements explicit in files committed to
the repository.

## 2. The tools and their responsibilities

There are five main tools in this setup. Each solves a different
problem.

  -----------------------------------------------------------------------
  Tool                    Beginner-friendly       What it manages
                          explanation             
  ----------------------- ----------------------- -----------------------
  **mise**                Installs the            Python, uv, Just, Moon
                          command-line tools and  
                          language runtimes the   
                          project needs           

  **uv**                  Manages Python packages FastAPI, Uvicorn,
                          and the project's       pytest, Ruff
                          virtual environment     

  **Moon**                Organizes and runs      Development, tests,
                          project tasks           linting, formatting

  **Just**                Gives developers short, `just dev`,
                          memorable commands      `just test`,
                                                  `just check`

  **Ruff / pytest**       Perform the actual code Linting, formatting,
                          checks and tests        automated tests
  -----------------------------------------------------------------------

A simple way to remember:

-   **mise:** Which tools and versions do I need?
-   **uv:** Which Python packages does my application need?
-   **Moon:** Which project task should run?
-   **Just:** What short command should I type?
-   **Ruff and pytest:** Do the code checks and tests.

These tools work together; one does not replace the others.

## 3. Why not just use Python directly?

You could start a FastAPI server with a direct command such as:

``` bash
uvicorn app.main:app --reload
```

That is perfectly valid for a very small project.

As a project grows, however, you may want consistent commands for:

-   Installing development tools.
-   Setting up dependencies.
-   Running tests.
-   Running lint and formatting checks.
-   Starting local services.
-   Building or packaging the application.
-   Running the same checks in CI.

The combination in this guide gives each responsibility a clear home. It
also makes it easier to add more projects or tasks later without turning
the README into a long list of shell commands.

------------------------------------------------------------------------

# Part 2 --- Prepare your development environment

## 4. Open the repository in the Dev Container

This walkthrough assumes you are using VS Code with a Dev Container and
that your terminal is inside the container.

Open the VS Code terminal and check your location:

``` bash
pwd
```

For this walkthrough, the repository path is:

``` text
/workspaces/fueliq
```

Check that you are in the repository root:

``` bash
ls -la
```

You should see the Git repository and its README. Run the remaining
repository commands from this directory unless a step says otherwise.

### Important: host machine versus Dev Container

A Dev Container is a separate development environment.

Installing a tool on Windows does not automatically make it available
inside the Linux container. That is why the earlier terminal returned:

``` text
bash: mise: command not found
```

The command was being run inside the container, where mise had not yet
been installed.

------------------------------------------------------------------------

# Part 3 --- Install mise

## 5. What is mise?

mise is a tool-version manager.

A project may require a particular Python version and particular
versions of developer tools. mise reads those requirements from a
configuration file and installs the tools.

For example, one project might require Python 3.13 while another
requires Python 3.12. mise helps keep those versions separate and
predictable.

### Why do we need it?

Without a version manager:

-   Developers may use different Python versions.
-   A tool may work on one laptop but not another.
-   Updating or switching a tool version can become a manual process.
-   CI may use a different version from local development.

With mise, the project can declare its tool versions in `.mise.toml`.

## 6. Install mise inside the Dev Container

Run:

``` bash
curl https://mise.run | sh
```

This downloads and runs the mise installer.

Make sure Bash can activate mise whenever a new interactive shell
starts:

``` bash
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
```

Load the updated configuration in the current terminal:

``` bash
source ~/.bashrc
```

Verify the installation:

``` bash
mise --version
```

You should see a mise version rather than `command not found`.

### What does shell activation do?

Installing mise puts its executable on disk. Shell activation configures
the terminal so that mise can select the right tool versions and update
the command search path.

The command:

``` bash
source ~/.bashrc
```

reloads the Bash configuration in the current terminal. You do not need
to close and reopen the terminal just to load this change.

### Make the installation persistent

The commands above install mise into the current container user's home
directory. If the Dev Container is deleted and rebuilt, that
installation may be lost.

For a repeatable team setup, add mise installation to the Dev Container
Dockerfile or use an appropriate Dev Container feature. Keep the project
tool versions in `.mise.toml` regardless.

------------------------------------------------------------------------

# Part 4 --- Declare and install project tools

## 7. Create `.mise.toml`

The `.mise.toml` file tells mise which tools the repository needs.

Create or edit `.mise.toml` in the repository root:

``` toml
[tools]
python = "3.13"
uv = "latest"
just = "latest"
"aqua:moonrepo/moon" = "latest"
```

### What does each entry mean?

  -----------------------------------------------------------------------
  Entry                               Why it is needed
  ----------------------------------- -----------------------------------
  `python = "3.13"`                   Selects the Python runtime used by
                                      FuelIQ

  `uv = "latest"`                     Installs uv to manage Python
                                      dependencies

  `just = "latest"`                   Installs the command runner used by
                                      developers

  `aqua:moonrepo/moon = "latest"`     Installs Moon through mise's Aqua
                                      backend
  -----------------------------------------------------------------------

### Why is Moon written differently?

The plain entry:

``` toml
moon = "latest"
```

did not resolve in the mise registry in this setup.

mise suggested the Aqua backend identifier:

``` toml
"aqua:moonrepo/moon" = "latest"
```

Use the backend-qualified identifier and remove any old plain
`moon = "latest"` entry. If both are present, mise will still try to
resolve the invalid entry.

### Install the tools

From the repository root:

``` bash
mise install
```

This reads `.mise.toml` and installs the declared tools.

Verify:

``` bash
mise --version
python --version
uv --version
just --version
moon --version
```

### What has mise installed?

At this point, mise has installed the developer tools and Python
runtime. It has **not** installed FastAPI or the other Python
application packages. That is uv's responsibility.

------------------------------------------------------------------------

# Part 5 --- Understand and use uv

## 8. What is uv?

uv is a Python project and package manager.

A Python application usually depends on packages written by other
developers. For example, FuelIQ will use:

-   FastAPI to create HTTP APIs.
-   Uvicorn to run the API server.
-   pytest to run automated tests.
-   Ruff to lint and format Python code.

uv declares and installs these dependencies and manages the project's
virtual environment.

### Why do we need a virtual environment?

A virtual environment keeps a project's Python packages separate from
other projects and from the system Python installation.

For example:

-   FuelIQ may need one version of FastAPI.
-   Another project may need a different version.
-   Installing everything globally can cause version conflicts.

uv creates a local `.venv/` directory for the project. This directory
should not be committed to Git.

## 9. Initialize the Python project

From the repository root, run:

``` bash
uv init --bare
```

This initializes Python project metadata without generating an example
application.

uv creates or updates `pyproject.toml`.

`pyproject.toml` is an important Python project configuration file. It
describes the project and its dependencies, and can also contain
settings for tools such as pytest and Ruff.

## 10. Install application dependencies

Add FastAPI and Uvicorn:

``` bash
uv add fastapi "uvicorn[standard]"
```

What are these?

-   **FastAPI:** The web framework used to define API endpoints.
-   **Uvicorn:** An ASGI server that runs the FastAPI application.
-   **`[standard]`:** Requests Uvicorn's standard optional dependencies.

Add development dependencies:

``` bash
uv add --dev pytest httpx ruff
```

What are these?

-   **pytest:** Runs automated tests.
-   **httpx:** Provides the HTTP client dependency used by FastAPI's
    test client.
-   **Ruff:** Checks Python code quality and formatting.

The `--dev` option marks these as development dependencies rather than
runtime dependencies.

Synchronize the environment:

``` bash
uv sync
```

uv creates or updates `.venv/` and installs the dependencies described
by the project metadata and lockfile.

### Understand the generated files

  -----------------------------------------------------------------------
  File or directory                   Purpose
  ----------------------------------- -----------------------------------
  `pyproject.toml`                    Project metadata, dependency
                                      declarations, and tool settings

  `uv.lock`                           Exact resolved dependency versions
                                      for reproducible installs

  `.venv/`                            Local Python virtual environment;
                                      do not commit it
  -----------------------------------------------------------------------

### How should dependencies be changed later?

To add a runtime package:

``` bash
uv add package-name
```

To add a development-only package:

``` bash
uv add --dev package-name
```

To synchronize the environment with the project configuration:

``` bash
uv sync
```

Prefer these commands over manually installing packages into `.venv/`.
The project configuration and lockfile should describe what the
application needs.

------------------------------------------------------------------------

# Part 6 --- Create a small FastAPI application

## 11. Create the application directories

Run:

``` bash
mkdir -p app tests
```

The `app/` directory will contain the API code. The `tests/` directory
will contain automated tests.

## 12. Create `app/main.py`

Create a file named `app/main.py`:

``` python
from fastapi import FastAPI

app = FastAPI(
    title="FuelIQ API",
    description="Fuel tracking and analytics platform",
    version="0.1.0",
)


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.get("/")
async def root():
    return {"message": "Welcome to FuelIQ"}
```

### What does this code do?

-   `FastAPI(...)` creates the API application.
-   `@app.get("/health")` defines an HTTP GET endpoint at `/health`.
-   `@app.get("/")` defines an HTTP GET endpoint at the root path.
-   The functions return Python dictionaries, which FastAPI serializes
    into JSON responses.

This is a small starting point, not the complete FuelIQ application.

## 13. Create `app/__init__.py`

Run:

``` bash
touch app/__init__.py
```

This marks `app` as a regular Python package and makes imports such as
`from app.main import app` straightforward.

## 14. Create a test file

Create `tests/test_main.py`:

``` python
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_root():
    response = client.get("/")

    assert response.status_code == 200
```

The tests call the API in-process using FastAPI's test client. They do
not require you to start a separate Uvicorn server.

## 15. Configure pytest imports

Add this section to `pyproject.toml`:

``` toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

### Why is this required?

The first test run failed with:

``` text
ModuleNotFoundError: No module named 'app'
```

Python could not resolve the `app.main` import during pytest collection.

The two changes that fixed it were:

1.  Creating `app/__init__.py`.
2.  Setting `pythonpath = ["."]` so the repository root is on pytest's
    import path.

Run the tests directly to verify:

``` bash
uv run pytest
```

You should see two tests pass.

------------------------------------------------------------------------

# Part 7 --- Understand Moon and configure tasks

## 16. What is Moon?

Moon is a project and task orchestration tool.

It lets a repository define tasks in configuration files instead of
requiring every developer to remember long commands.

For example, the task named `test` can be configured to run:

``` bash
uv run pytest
```

A developer can then invoke the task through Moon:

``` bash
moon run root:test
```

Moon becomes especially useful as a repository grows to contain multiple
projects, shared task conventions, dependencies between tasks, and
caching.

### Why use Moon in FuelIQ?

Today FuelIQ has one FastAPI application. Moon may seem like an extra
layer for such a small project, but it establishes a consistent task
model that can grow with the repository.

For example, the repository could later contain:

-   An API project.
-   A background worker.
-   A shared Python package.
-   A frontend application.
-   Integration test projects.

Moon can organize tasks across these projects.

## 17. Understand Moon's two configuration files

Moon uses different files for workspace-level and project-level
configuration.

  File                    What it configures
  ----------------------- ----------------------------------------------
  `.moon/workspace.yml`   The workspace and project discovery
  `moon.yml`              Tasks and settings for an individual project

Do not confuse `moon.yml` with `justfile`. They use different formats
and serve different purposes.

### Create `.moon/workspace.yml`

Create the directory:

``` bash
mkdir -p .moon
```

Create `.moon/workspace.yml`:

``` yaml
$schema: 'https://moonrepo.dev/schemas/workspace.json'

projects:
  root: '.'
```

This tells Moon that the repository root is a project named `root`.

### Create root `moon.yml`

Create or replace `moon.yml` in the repository root:

``` yaml
$schema: 'https://moonrepo.dev/schemas/project.json'

tasks:
  install:
    command: 'uv'
    args: ['sync']
    toolchains: ['system']
    inputs:
      - 'pyproject.toml'
      - 'uv.lock'

  dev:
    command: 'uv'
    args:
      - 'run'
      - 'uvicorn'
      - 'app.main:app'
      - '--reload'
      - '--host'
      - '0.0.0.0'
    toolchains: ['system']
    options:
      cache: false

  test:
    command: 'uv'
    args: ['run', 'pytest']
    toolchains: ['system']
    inputs:
      - 'app/**/*.py'
      - 'tests/**/*.py'
      - 'pyproject.toml'
      - 'uv.lock'

  lint:
    command: 'uv'
    args: ['run', 'ruff', 'check', '.']
    toolchains: ['system']
    inputs:
      - 'app/**/*.py'
      - 'tests/**/*.py'
      - 'pyproject.toml'
      - 'uv.lock'

  format:
    command: 'uv'
    args: ['run', 'ruff', 'format', '.']
    toolchains: ['system']
    inputs:
      - 'app/**/*.py'
      - 'tests/**/*.py'
      - 'pyproject.toml'

  format-check:
    command: 'uv'
    args: ['run', 'ruff', 'format', '--check', '.']
    toolchains: ['system']
    inputs:
      - 'app/**/*.py'
      - 'tests/**/*.py'
      - 'pyproject.toml'
```

### Understand the task configuration

Each task has a name, such as `test`, `lint`, or `dev`.

A task can define:

-   `command`: The executable Moon should run.
-   `args`: The arguments passed to that executable.
-   `toolchains`: The tools Moon should make available.
-   `inputs`: The files that affect the task and its cache key.
-   `options`: Additional task behavior, such as disabling caching.

For example:

``` yaml
test:
  command: 'uv'
  args: ['run', 'pytest']
  toolchains: ['system']
```

This tells Moon to execute:

``` bash
uv run pytest
```

### Why use `toolchains: ['system']`?

In this setup, mise manages Python and uv. We are not asking Moon to
install another Python runtime.

The system toolchain tells Moon to use the executables available on the
environment's PATH. The mise activation configured earlier makes the
selected tools available in the shell environment.

This keeps runtime installation with mise and task execution with Moon.

### Why define `inputs`?

Moon uses task inputs when determining whether a task's previous result
can be reused from its cache.

For example, a test task should be affected by changes to application
code, tests, and relevant dependency files.

Explicit inputs also avoid treating generated virtual-environment
contents such as `.venv/` as ordinary source files to hash.

### Why is `dev` caching disabled?

A development server is a long-running process. It is not a completed
output that should be reused from a task cache.

That is why the `dev` task has:

``` yaml
options:
  cache: false
```

## 18. Understand the `root:task` syntax

Consider:

``` bash
moon run root:format-check
```

The part before the colon is the project name:

``` text
root
```

The part after the colon is the task name:

``` text
format-check
```

So `root:format-check` means: run the `format-check` task in the `root`
project.

Other examples:

``` bash
moon run root:dev
moon run root:test
moon run root:lint
moon run root:format
```

## 19. Run Moon setup and verify project discovery

Run:

``` bash
moon setup
```

In this design, Moon may report:

``` text
Unable to setup, no toolchains are configured!
```

This is expected and is not a failure. We deliberately use mise to
install Python and uv, and Moon's tasks use the system toolchain. There
are no Moon-managed language toolchains to install.

Check that Moon recognizes the project:

``` bash
moon project root
```

Then run an individual task:

``` bash
moon run root:test
```

------------------------------------------------------------------------

# Part 8 --- Understand Just and create developer commands

## 20. What is Just?

Just is a command runner. It lets you create named recipes in a file
called `justfile`.

A recipe is a named sequence of shell commands.

For example, instead of remembering:

``` bash
moon run root:test
```

a developer can run:

``` bash
just test
```

Just does not install Python packages or orchestrate the task graph
itself. In this setup, it provides a friendly command interface and
invokes Moon or other tools.

### Why do we need Just if Moon already runs tasks?

Moon can run the tasks directly. Just is optional.

We are using Just because it gives developers a simple, stable
interface. The underlying implementation can change while the everyday
commands remain familiar.

For example, developers can keep using:

``` bash
just test
```

even if the internal task implementation changes later.

## 21. Create the root `justfile`

Create a file named exactly `justfile` in the repository root.

Do not name it `justfile.txt`.

Add:

``` makefile
default:
    @just --list

install:
    mise install
    uv sync

versions:
    mise ls
    python --version
    uv --version
    moon --version

setup:
    moon setup

dev:
    moon run root:dev

test:
    moon run root:test

lint:
    moon run root:lint

format:
    moon run root:format

format-check:
    moon run root:format-check

check:
    just lint
    just format-check
    just test
```

### Understand the recipes

  -----------------------------------------------------------------------
  Recipe                              What it does
  ----------------------------------- -----------------------------------
  `default`                           Displays available Just commands

  `install`                           Installs mise-managed tools and
                                      synchronizes Python dependencies

  `versions`                          Shows installed tool versions

  `setup`                             Runs Moon setup

  `dev`                               Starts the FastAPI development
                                      server through Moon

  `test`                              Runs pytest through Moon

  `lint`                              Runs Ruff lint checks through Moon

  `format`                            Formats Python files

  `format-check`                      Checks formatting without changing
                                      files

  `check`                             Runs lint, formatting validation,
                                      and tests
  -----------------------------------------------------------------------

### Important: Just recipe indentation

Just recipes use indentation before their shell commands. Use spaces
consistently.

The file is not YAML or TOML. Do not put Just recipes in `moon.yml` or
`.mise.toml`.

Run:

``` bash
just
```

This should list the available recipes.

------------------------------------------------------------------------

# Part 9 --- Add Git ignore rules

## 22. Create `.gitignore`

Generated files and local secrets should not be committed.

Add these entries to `.gitignore`:

``` gitignore
.venv/
__pycache__/
*.py[cod]
.pytest_cache/
.ruff_cache/
.env
.env.*
!.env.example
dist/
build/
```

### Why ignore these files?

-   `.venv/` contains locally installed Python packages.
-   `__pycache__/` and `*.pyc` are generated Python bytecode.
-   `.pytest_cache/` and `.ruff_cache/` are local tool caches.
-   `.env` may contain secrets or machine-specific configuration.
-   `dist/` and `build/` contain generated build output.

Commit the dependency declarations and lockfile, not the local virtual
environment.

------------------------------------------------------------------------

# Part 10 --- Run the complete setup

## 23. Install everything

Once all configuration and application files are in place, run:

``` bash
just install
```

This runs:

``` text
just install
   |
   +----> mise install
   |        Installs Python, uv, Just, and Moon
   |
   +----> uv sync
            Creates/updates .venv
            Installs Python project dependencies
```

## 24. Start the API

Run:

``` bash
just dev
```

Moon executes the `root:dev` task, which runs Uvicorn through uv.

The server binds to:

``` text
0.0.0.0:8000
```

In VS Code, forward port `8000` if it is not forwarded automatically.

Open:

-   API root: `http://localhost:8000/`
-   Health check: `http://localhost:8000/health`
-   Interactive API documentation: `http://localhost:8000/docs`

Stop the development server with `Ctrl+C`.

## 25. Run tests

``` bash
just test
```

Expected result: pytest collects and passes the two starter tests.

## 26. Run lint checks

``` bash
just lint
```

This runs:

``` bash
uv run ruff check .
```

Linting checks code for issues such as unused imports, undefined names,
and other rule violations.

## 27. Format Python files

``` bash
just format
```

This runs Ruff's formatter. It may change files.

## 28. Check formatting without changing files

``` bash
just format-check
```

This runs Ruff with `--check`. It reports whether files need formatting
but does not modify them.

Remember:

-   `just format` changes files when necessary.
-   `just format-check` only validates them.

## 29. Run all checks

``` bash
just check
```

This runs the following sequence:

``` text
just check
   |
   +----> just lint
   |
   +----> just format-check
   |
   +----> just test
```

If any recipe fails, Just stops and reports the failure. Fix the
reported issue and run the command again.

------------------------------------------------------------------------

# Part 11 --- Understand the errors encountered and how to fix them

This section explains the real setup problems encountered during the
FuelIQ configuration.

## 30. `mise: command not found`

Error:

``` text
bash: mise: command not found
```

**Why it happened:** mise was not installed inside the Dev Container, or
the shell had not loaded its activation configuration.

**Fix:**

``` bash
curl https://mise.run | sh
echo 'eval "$(~/.local/bin/mise activate bash)"' >> ~/.bashrc
source ~/.bashrc
```

Verify:

``` bash
mise --version
```

## 31. `moon not found in mise tool registry`

Error:

``` text
moon not found in mise tool registry
```

**Why it happened:** The plain `moon` tool identifier did not resolve in
the default mise registry in this setup.

**Fix:** Use the Aqua backend identifier:

``` toml
"aqua:moonrepo/moon" = "latest"
```

Remove the invalid `moon = "latest"` entry and run:

``` bash
mise install
```

## 32. `just: error: no justfile found`

Error:

``` text
error: no justfile found
```

**Why it happened:** The Just executable was installed, but the
repository did not yet have a file named `justfile`.

**Fix:**

``` bash
touch justfile
```

Then add the recipes to it.

## 33. Moon tried to parse Just syntax as YAML

Error:

``` text
Failed to parse moon.yml
found character that cannot start any token
```

The offending line looked like:

``` makefile
default:
    @just --list
```

**Why it happened:** Justfile syntax was accidentally placed in
`moon.yml`.

**Fix:** Keep each tool's configuration in its own file:

  File                    Format        Purpose
  ----------------------- ------------- ----------------------------------
  `.mise.toml`            TOML          Tool versions
  `.moon/workspace.yml`   YAML          Moon workspace
  `moon.yml`              YAML          Moon project tasks
  `justfile`              Just syntax   Developer commands
  `pyproject.toml`        TOML          Python project and tool settings

## 34. Moon reported no toolchains configured

Message:

``` text
Unable to setup, no toolchains are configured!
```

**Why it happened:** No Moon-managed language toolchain was configured.

**Resolution:** This is expected in this architecture. mise manages
Python and uv; Moon runs tasks using the system toolchain.

You do not need to configure a second Python installation just to remove
this informational message.

## 35. Moon rejected `tasks.inputs`

Error:

``` text
tasks.inputs: invalid type: sequence, expected struct PartialTaskConfig
```

**Why it happened:** The `inputs` list was placed at the wrong YAML
level.

Incorrect shape:

``` yaml
tasks:
  inputs:
    - 'app/**/*.py'
```

Correct shape:

``` yaml
tasks:
  lint:
    command: 'uv'
    args: ['run', 'ruff', 'check', '.']
    toolchains: ['system']
    inputs:
      - 'app/**/*.py'
      - 'tests/**/*.py'
```

Each task owns its own `inputs` configuration.

## 36. Ruff reported that files would be reformatted

Output:

``` text
2 files would be reformatted
```

**Why it happened:** The source files did not yet match Ruff's
formatting rules.

**Fix:**

``` bash
just format
```

Then validate:

``` bash
just format-check
```

Do not use the check-only command when your intention is to modify
files.

## 37. pytest could not import `app`

Error:

``` text
ModuleNotFoundError: No module named 'app'
```

**Why it happened:** Python could not resolve `app.main` during pytest
collection.

**Fix:**

``` bash
touch app/__init__.py
```

Add this to `pyproject.toml`:

``` toml
[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]
```

Then run:

``` bash
just test
```

## 38. Starlette/httpx deprecation warning

A test run also displayed a warning about using `httpx` with Starlette's
test client.

This warning was separate from the Python import failure. It did not
cause the test collection error.

If it remains after the tests pass, review the FastAPI, Starlette, and
HTTP client compatibility before changing dependency versions. Do not
confuse a deprecation warning with a failed test.

------------------------------------------------------------------------

# Part 12 --- Daily developer workflow

## 39. Starting work on an existing checkout

When you clone the repository or open it in a fresh Dev Container:

``` bash
just install
```

This installs the mise-managed tools and synchronizes the Python
dependencies.

Then run:

``` bash
just check
```

This verifies linting, formatting, and tests before you start making
changes.

## 40. During development

Start the server:

``` bash
just dev
```

In another terminal, run tests:

``` bash
just test
```

When you change dependencies, use uv:

``` bash
uv add package-name
```

When you finish a code change:

``` bash
just format
just check
```

## 41. Before committing

A useful sequence is:

``` bash
just format
just check
git status
git diff --check
```

Review the changes, then commit them.

The `.venv/` directory should not appear as a new Git change if
`.gitignore` is configured correctly.

------------------------------------------------------------------------

# Part 13 --- Final repository structure

After completing this walkthrough, the repository should look broadly
like this:

``` text
fueliq/
├── .moon/
│   └── workspace.yml
├── app/
│   ├── __init__.py
│   └── main.py
├── tests/
│   └── test_main.py
├── .devcontainer.json
├── .gitignore
├── .mise.toml
├── justfile
├── moon.yml
├── pyproject.toml
├── uv.lock
└── README.md
```

The `.venv/` directory will also exist locally, but it should be ignored
by Git.

------------------------------------------------------------------------

# Part 14 --- Command reference

## Tool and dependency management

  Command                 Meaning
  ----------------------- ------------------------------------------------------
  `mise install`          Install tools declared in `.mise.toml`
  `mise ls`               List installed mise tools
  `uv add fastapi`        Add a runtime Python dependency
  `uv add --dev pytest`   Add a development dependency
  `uv sync`               Synchronize the virtual environment with the project
  `python --version`      Display the selected Python version

## Moon

  Command                        Meaning
  ------------------------------ -----------------------------------------
  `moon setup`                   Set up configured Moon toolchains
  `moon project root`            Inspect the root project
  `moon run root:dev`            Run the root project's development task
  `moon run root:test`           Run the root project's test task
  `moon run root:lint`           Run the root project's lint task
  `moon run root:format`         Run the root project's formatting task
  `moon run root:format-check`   Check formatting through Moon

## Just

  Command               Meaning
  --------------------- ---------------------------------------
  `just`                List available recipes
  `just install`        Install tools and Python dependencies
  `just versions`       Display tool versions
  `just setup`          Run Moon setup
  `just dev`            Start the API
  `just test`           Run tests
  `just lint`           Run lint checks
  `just format`         Format source files
  `just format-check`   Check formatting
  `just check`          Run the complete validation sequence

------------------------------------------------------------------------

# Part 15 --- Final verification checklist

Run these commands from the repository root.

### Verify tools

``` bash
mise --version
python --version
uv --version
just --version
moon --version
```

### Verify dependencies

``` bash
uv sync
```

### Verify Moon project discovery

``` bash
moon project root
```

### Verify the application

``` bash
just dev
```

Open the health endpoint and API documentation in your browser.

### Verify code quality and tests

``` bash
just format
just check
```

A successful `just check` should complete all three stages:

1.  Ruff lint checks pass.
2.  Ruff formatting validation passes.
3.  pytest collects and passes the tests.

------------------------------------------------------------------------

# Final mental model

Keep this diagram in mind:

``` text
                 DEVELOPER
                     |
                     v
                   JUST
          "just dev", "just check"
                     |
                     v
                   MOON
          Project tasks and execution
                     |
                     v
                    UV
        Python environment and packages
                     |
                     v
             PYTHON / FASTAPI
```

mise supports the environment alongside this flow:

``` text
                  MISE
          Tool and runtime versions
             /    |    |    \
          Python  uv  Just  Moon
```

And the quality tools are invoked by Moon through uv:

``` text
Moon task
   |
   +----> uv run ruff check .
   |
   +----> uv run ruff format --check .
   |
   +----> uv run pytest
```

The most important thing to remember is that **each tool has one clear
responsibility**:

-   mise installs and selects developer tools.
-   uv manages Python packages and the virtual environment.
-   Moon organizes and runs project tasks.
-   Just gives developers easy commands.
-   Ruff and pytest perform code quality checks and tests.

Once this setup is in place, a new developer can open FuelIQ in the
configured Dev Container, run `just install`, and use `just dev` or
`just check` without having to remember the underlying command
sequences.
