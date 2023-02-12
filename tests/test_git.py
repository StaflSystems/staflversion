import pytest
from os import system
from pathlib import Path
from shutil import rmtree

from staflversion.git import GitWrapper


@pytest.fixture
def sample_repo():
    rmtree("sample_repo", ignore_errors=True)
    Path.mkdir("sample_repo")
    system(
        "cd sample_repo &&\
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
    yield GitWrapper("sample_repo")
    rmtree("sample_repo")


def test_get_tags(sample_repo: GitWrapper):
    tags = sample_repo.get_tags()
    assert tags == ["0.0.0+1", "0.0.0+2", "invalid_tag"]


def test_get_last_commit_message(sample_repo: GitWrapper):
    assert sample_repo.get_head_commit_message() == "c5"


def test_get_commit_messages_since_tag(sample_repo: GitWrapper):
    assert sample_repo.get_commit_messages_since_tag() == ["c5", "c4"]
