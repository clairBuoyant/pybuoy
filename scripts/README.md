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

These scripts can be run directly like so:

- `./scripts/<filename>` (e.g., `./scripts/init` or `./scripts/check`)
- Run `. ./aliases` in your terminal to run any script just by `<command_name>` (e.g., `init` or `check`). <sup>1</sup>

#### Note

1. Loads all command names to current shell, so you can call on these scripts by `<command_name>` (e.g., `init` or `check`). This script needs to be re-run every time you start a new terminal session. But, it saves you from prepending the path to script every time! :)

### Attribution

Styled after GitHub's ["Scripts to Rule Them All"](https://github.com/github/scripts-to-rule-them-all).
