import re

from functools import total_ordering
from typing import Optional

from .git import GitWrapper


@total_ordering
class StaflVersion:
    VERSION_REGEX = re.compile(
        r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)\+(?P<build>\d+)$"
    )

    def __init__(self, major: int, minor: int, patch: int, build: int):
        self.major = major
        self.minor = minor
        self.patch = patch
        self.build = build

    @classmethod
    def parse(cls, version: str) -> "StaflVersion":
        match = cls.VERSION_REGEX.match(version)
        if not match:
            raise RuntimeError("invalid format")

        return cls.extract(match)

    @classmethod
    def extract(cls, match: re.Match) -> "StaflVersion":
        groupdict = match.groupdict()
        major = int(groupdict["major"])
        minor = int(groupdict["minor"])
        patch = int(groupdict["patch"])
        build = int(groupdict["build"])

        return StaflVersion(major, minor, patch, build)

    @classmethod
    def try_parse(cls, version: str) -> Optional["StaflVersion"]:
        try:
            return cls.parse(version)
        except:  # noqa
            return None

    def __str__(self) -> str:
        return f"{self.major}.{self.minor}.{self.patch}+{self.build}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other: object):
        if not isinstance(other, StaflVersion):
            return NotImplemented

        return (
            self.major == other.major
            and self.minor == other.minor
            and self.patch == other.patch
            and self.build == other.build
        )

    def __lt__(self, other: "StaflVersion"):
        return (self.major, self.minor, self.patch, self.build) < (
            other.major,
            other.minor,
            other.patch,
            other.build,
        )

    def increment_major(self) -> "StaflVersion":
        return StaflVersion(self.major + 1, 0, 0, 0)

    def increment_minor(self) -> "StaflVersion":
        return StaflVersion(self.major, self.minor + 1, 0, 0)

    def increment_patch(self) -> "StaflVersion":
        return StaflVersion(self.major, self.minor, self.patch + 1, 0)

    def increment_build(self) -> "StaflVersion":
        return StaflVersion(self.major, self.minor, self.patch, self.build + 1)


class StaflVersioner:
    _INCREMENT_MAJOR = "+semver:major"
    _INCREMENT_MINOR = "+semver:minor"
    _INCREMENT_PATCH = "+semver:patch"
    _SET_VERSION = re.compile(r"\+semver-set:" + StaflVersion.VERSION_REGEX.pattern[1:])

    def __init__(self, git: GitWrapper):
        self._git = git

    def determine_version(self) -> StaflVersion:
        new_commit_messages = self._git.get_commit_messages_since_tag()

        set_version_matches = [
            self._SET_VERSION.match(message)
            for message in new_commit_messages
            if not None
        ]
        set_version = set_version_matches[0] if set_version_matches else None
        increment_major = any([self._INCREMENT_MAJOR in m for m in new_commit_messages])
        increment_minor = any([self._INCREMENT_MINOR in m for m in new_commit_messages])
        increment_patch = any([self._INCREMENT_PATCH in m for m in new_commit_messages])

        versions = [
            StaflVersion.parse(t)
            for t in self._git.get_tags()
            if StaflVersion.try_parse(t) is not None
        ]
        versions.sort(reverse=True)
        last_version = versions[0] if versions else StaflVersion(0, 0, 0, 0)

        if set_version:
            version = StaflVersion.extract(set_version)
        elif increment_major:
            version = last_version.increment_major()
        elif increment_minor:
            version = last_version.increment_minor()
        elif increment_patch:
            version = last_version.increment_patch()
        else:
            version = last_version.increment_build()

        return version
