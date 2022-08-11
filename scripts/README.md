# Development Scripts

These scripts are provided for development of [clairBuoyant](https://www.github.com/clairBuoyant). The script names are standardized across all repositories for clairBuoyant to simplify the development experience.

he command to run can be inferred based on the following pattern:

- command: `filename`
  - e.g., `bootstrap`
    - filename: bootstrap
    - subFolderName: n/a

## Available Commands

See below for list of available commands.

- `bootstrap`: resolve all system dependencies the application needs to run.
- `check`: check whether code linting passes.
- `clean`: remove all unnecessary build artifacts.
- `init`: run bootstrap and setup.
- `lint`: run code linting.
- `setup`: install python dependencies and githooks.
- `test`: run test suite.
- `uninstall`: remove python dependencies and build artifacts.

### Usage

These scripts can be used directly or with `poetry` (**recommended**).

1. Run with poetry: `poetry run <command_name>` (e.g., `poetry run init`) <sup>1</sup>
2. Run directly:
   - `./scripts/<filename>` (e.g., `./scripts/init` or `./scripts/check`)
   - Run `. ./aliases` in your terminal to run any script just by `<command_name>` (e.g., `init` or `check`). <sup>2</sup>

#### Note

1. If you've ran `poetry shell` (i.e., if `which python` outputs "path/to/clairBuoyant/server/.venv/bin/python"), you could just run these scripts by `<command_name>` in terminal (e.g., `init` or `check`).

2. Alternatively, you could run `. ./aliases`. This will load all command names to current shell, so you can call on these scripts by `<command_name>` (e.g., `init` or `check`). This script needs to be re-run every time you start a new terminal session. But, it saves you from prepending `poetry run` every time! :)

### Attribution

Styled after GitHub's ["Scripts to Rule Them All"](https://github.com/github/scripts-to-rule-them-all).
