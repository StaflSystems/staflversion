import pytest
import tempfile
from os import system

from staflversion.git import GitWrapper


@pytest.fixture
def sample_repo():
    with tempfile.TemporaryDirectory() as tempdir:
        system(
            f"cd {tempdir} &&\
            git init &&\
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
