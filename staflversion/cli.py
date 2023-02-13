"""CLI interface for staflversion project.
"""

from .git import GitWrapper
from .version import StaflVersioner


def main():  # pragma: no cover
    git = GitWrapper()
    versioner = StaflVersioner(git)
    print(versioner.determine_version())
