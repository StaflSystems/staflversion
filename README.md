# stafl-python-template
Stafl python template for modules and pyinstaller .exe

## Sources

### Files in this template were cherry picked and modified from:

- https://github.com/rochacbruno/python-project-template
- https://github.com/scottclowe/python-template-repo

### Pyinstaller Configuration From:

- https://stackoverflow.com/questions/48884766/pyinstaller-on-a-setuptools-package
- https://github.com/pyinstaller/pyinstaller/wiki/Recipe-Setuptools-Entry-Point

## Structure

```text
├── .github                        # Github metadata for repository
│   ├── pull_request_template.md   # template used for PRs
│   └── workflows                  # The CI pipeline for Github Actions. one to run tests and lint checks, and another which runs the lint check and builds a stand-alone exe.
├── .vscode                        # Contains launch configurations and tasks for the repo. Note that pre-commit is also configured in this template and can be used for formatting
├── .gitignore                     # A list of files to ignore when pushing to Github
├── .flake8                        # Configuration for the linter
├── .coveragerc                    # Configuration for coverage reporting (coverage reports currently go nowhere from CI; codecov would be a nice improvement)
├── .pre-commit-config.yml         # Configuration for [pre-commit](https://pre-commit.com/)
├── project_name                   # The main python package for the project
│   ├── base.py                    # The base module for the project
│   ├── __init__.py                # This tells Python that this is a package
│   ├── __main__.py                # The entry point for the project
│   └── VERSION                    # The version for the project is kept in a static file
├── README.md                      # The main readme for the project
├── setup.py                       # The setup.py file for installing and packaging the project
├── requirements.txt               # An empty file to hold the requirements for the project
├── requirements-dev.txt           # List of requirements for testing and devlopment
├── setup.py                       # The setup.py file for installing and packaging the project
└── tests                          # Unit tests for the project (add mote tests files here)
    ├── conftest.py                # Configuration, hooks and fixtures for pytest
    ├── __init__.py                # This tells Python that this is a test package
    └── test_base.py               # The base test case for the project
```

## Use of the template

Several things are named `project_name` in:
- .github/workflows
- .vscode/launch.json
- .vscode/tasks.json
- the pyinstaller spec
- the `project_name` module
- setup.py

All of those things should be renamed, along with file and folder names, to match the name of the application being developed.