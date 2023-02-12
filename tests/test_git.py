import pytest
from os import system

from staflversion.git import GitWrapper

@pytest.fixture
def sample_repo():
    system(
        "rm -rf sample_repo;\
        mkdir sample_repo &&\
        cd sample_repo &&\
        git init &&\
        git commit --allow-empty -m c1 &&\
        git tag 0.0.0+1 &&\
        git commit --allow-empty -m c2 &&\
        git tag invalid_tag &&\
        git commit --allow-empty -m c3 &&\
        git tag 0.0.0+2\
    "
    )
    yield GitWrapper("sample_repo")
    system("rm -rf sample_repo")


def test_get_tags(sample_repo):
    tags = sample_repo.get_tags()
    assert tags == ["0.0.0+1", "0.0.0+2", "invalid_tag"]


def test_get_last_commit_message(sample_repo):
    assert sample_repo.get_head_commit_message() == "c3"
