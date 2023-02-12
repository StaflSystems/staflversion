import pytest
import tempfile
from pytest import MonkeyPatch
from os import system, getcwd

from staflversion.git import GitWrapper


@pytest.fixture
def tempdir():
    with tempfile.TemporaryDirectory() as tempdir:
        yield tempdir
        print(f"clean dir: {getcwd()}")


@pytest.fixture
def sample_repo(tempdir: str, monkeypatch: MonkeyPatch):
    # tempdir above must come before monkeypatch so that the directory is changed back before the directory is cleanup up
    monkeypatch.chdir(tempdir)
    system(
        "git init &&\
        git config user.name 'test' &&\
        git config user.email 'test@test.com' &&\
        git commit --allow-empty -m c1 &&\
        git tag 0.0.0+1 &&\
        git commit --allow-empty -m c2 &&\
        git tag invalid_tag &&\
        git commit --allow-empty -m c3 &&\
        git tag 0.0.0+2 &&\
        git commit --allow-empty -m c4 &&\
        git commit --allow-empty -m c5\
    "
    )
    yield GitWrapper(tempdir)


def test_get_tags(sample_repo: GitWrapper):
    tags = sample_repo.get_tags()
    assert tags == ["0.0.0+1", "0.0.0+2", "invalid_tag"]


def test_get_last_commit_message(sample_repo: GitWrapper):
    assert sample_repo.get_head_commit_message() == "c5"


def test_get_commit_messages_since_tag(sample_repo: GitWrapper):
    assert sample_repo.get_commit_messages_since_tag() == ["c5", "c4"]
