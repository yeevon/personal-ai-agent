from functions.get_file_content import get_file_content
from src.config import MAX_CHARS


def test_reads_file(work_dir):
    result = get_file_content(str(work_dir), "hello.txt")
    assert result == "hello world"


def test_truncates_large_file(work_dir):
    result = get_file_content(str(work_dir), "large.txt")
    assert len(result) > MAX_CHARS
    assert "truncated" in result


def test_outside_boundary(work_dir):
    result = get_file_content(str(work_dir), "/etc/passwd")
    assert result.startswith("Error:")
    assert "outside the permitted working directory" in result


def test_parent_traversal(work_dir):
    result = get_file_content(str(work_dir), "../../etc/passwd")
    assert result.startswith("Error:")
    assert "outside the permitted working directory" in result


def test_not_a_file(work_dir):
    result = get_file_content(str(work_dir), "sub")
    assert result.startswith("Error:")
    assert "is not a file" in result


def test_nonexistent_file(work_dir):
    result = get_file_content(str(work_dir), "does_not_exist.txt")
    assert result.startswith("Error:")
