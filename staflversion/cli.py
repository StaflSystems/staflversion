"""CLI interface for staflversion project.
"""

import argparse

from .git import GitWrapper
from .version import StaflVersioner


def main():  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--major",
        help="output only the major component of the version",
        action="store_true",
    )
    parser.add_argument(
        "--minor",
        help="output only the minor component of the version",
        action="store_true",
    )
    parser.add_argument(
        "--patch",
        help="output only the patch component of the version",
        action="store_true",
    )
    parser.add_argument(
        "--build",
        help="output only the build component of the version",
        action="store_true",
    )
    args = parser.parse_args()

    git = GitWrapper()
    versioner = StaflVersioner(git)
    version = versioner.determine_version()

    if args.major:
        print(str(version.major))
    elif args.minor:
        print(str(version.minor))
    elif args.patch:
        print(str(version.patch))
    elif args.build:
        print(str(version.build))
    else:
        print(str(version))
