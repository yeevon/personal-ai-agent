import pytest
from src.config import MAX_CHARS


@pytest.fixture
def work_dir(tmp_path):
    (tmp_path / "hello.txt").write_text("hello world", encoding="utf-8")
    (tmp_path / "large.txt").write_text("x" * (MAX_CHARS + 100), encoding="utf-8")
    sub = tmp_path / "sub"
    sub.mkdir()
    (sub / "nested.py").write_text('print("nested")', encoding="utf-8")
    return tmp_path
