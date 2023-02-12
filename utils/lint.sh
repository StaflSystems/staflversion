flake8 staflversion/ tests/ --count --show-source --statistics
black --check staflversion/ tests/
mypy --ignore-missing-imports staflversion/ tests/