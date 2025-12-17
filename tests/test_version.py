from typing import List
from staflversion.version import StaflVersion, StaflVersioner


def test_version_construction_from_ints():
    version = StaflVersion(1, 2, 3, 4)
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert version.build == 4


def test_version_parse():
    version = StaflVersion.parse("1.2.3+4")
    assert version.major == 1
    assert version.minor == 2
    assert version.patch == 3
    assert version.build == 4


def test_version_str():
    v_str = "1.2.3+4"
    version = StaflVersion.parse(v_str)
    assert str(version) == v_str


def test_version_compare_build():
    v1 = StaflVersion.parse("1.0.0+0")
    v2 = StaflVersion.parse("1.0.0+1")
    assert v2 > v1


def test_version_compare_patch():
    v1 = StaflVersion.parse("1.0.0+1")
    v2 = StaflVersion.parse("1.0.1+0")
    assert v2 > v1


def test_version_compare_minor():
    v1 = StaflVersion.parse("1.0.1+1")
    v2 = StaflVersion.parse("1.1.0+0")
    assert v2 > v1


def test_version_compare_major():
    v1 = StaflVersion.parse("1.2.1+1")
    v2 = StaflVersion.parse("2.0.0+0")
    assert v2 > v1


def test_version_increment_major():
    v1 = StaflVersion.parse("1.1.1+1")
    v2 = v1.increment_major()
    assert v1.major + 1 == v2.major
    assert v2.minor == 0
    assert v2.patch == 0
    assert v2.build == 0


def test_version_increment_minor():
    v1 = StaflVersion.parse("1.0.0+0")
    v2 = v1.increment_minor()
    assert v2.major == v1.major
    assert v2.minor == v1.minor + 1
    assert v2.patch == 0
    assert v2.build == 0


def test_version_increment_patch():
    v1 = StaflVersion.parse("1.0.0+0")
    v2 = v1.increment_patch()
    assert v2.major == v1.major
    assert v2.minor == v1.minor
    assert v2.patch == v1.patch + 1
    assert v2.build == 0


def test_version_increment_build():
    v1 = StaflVersion.parse("1.0.0+0")
    v2 = v1.increment_build()
    assert v2.major == v1.major
    assert v2.minor == v1.minor
    assert v2.patch == v1.patch
    assert v2.build == v1.build + 1


class MockGitWrapper:
    def __init__(self, commit_messages_since_tag: List[str], tags: List[str]) -> None:
        self.commit_messages_since_tag = commit_messages_since_tag
        self.tags = tags

    def get_commit_messages_since_tag(self):
        return self.commit_messages_since_tag

    def get_tags(self):
        return self.tags


def test_version_determine_simple_build():
    git = MockGitWrapper(["kjlj"], ["0.0.0+1", "0.0.0+2", "invalid"])
    versioner = StaflVersioner(git)
    assert versioner.determine_version() == StaflVersion(0, 0, 0, 3)


def test_version_determine_first_build():
    git = MockGitWrapper(["kjlj"], [])
    versioner = StaflVersioner(git)
    assert versioner.determine_version() == StaflVersion(0, 0, 0, 1)


def test_version_determine_increment_patch():
    git = MockGitWrapper(["some m", "new thing +semver:patch"], ["0.0.0+1", "0.0.0+2"])
    versioner = StaflVersioner(git)
    assert versioner.determine_version() == StaflVersion(0, 0, 1, 0)


def test_version_determine_increment_minor():
    git = MockGitWrapper(["some m", "new thing +semver:minor"], ["0.0.0+1", "0.0.0+2"])
    versioner = StaflVersioner(git)
    assert versioner.determine_version() == StaflVersion(0, 1, 0, 0)


def test_version_determine_increment_major():
    git = MockGitWrapper(["some m", "new thing +semver:major"], ["0.0.0+1", "0.0.0+2"])
    versioner = StaflVersioner(git)
    assert versioner.determine_version() == StaflVersion(1, 0, 0, 0)


def test_version_determine_set_version():
    git = MockGitWrapper(
        ["+semver-set:1.2.3+4", "new thing +semver:major"], ["0.0.0+1", "0.0.0+2"]
    )
    versioner = StaflVersioner(git)
    assert versioner.determine_version() == StaflVersion(1, 2, 3, 4)


def test_version_patch_release():
    git = MockGitWrapper(
        ["Fix critical bug +semver:patch"], ["1.2.3+4-dev/patch", "1.2.2+0"]
    )
    versioner = StaflVersioner(git)
    assert versioner.determine_version() == StaflVersion(1, 2, 4, 0)
