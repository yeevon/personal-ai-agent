from functions.get_files_info import get_files_info


def test_lists_current_dir(work_dir):
    result = get_files_info(str(work_dir), ".")
    assert "hello.txt" in result
    assert "large.txt" in result
    assert "sub" in result


def test_lists_subdirectory(work_dir):
    result = get_files_info(str(work_dir), "sub")
    assert "nested.py" in result
    assert "hello.txt" not in result


def test_outside_boundary(work_dir):
    result = get_files_info(str(work_dir), "/bin")
    assert result.startswith("Error:")
    assert "outside the permitted working directory" in result


def test_parent_traversal(work_dir):
    result = get_files_info(str(work_dir), "../")
    assert result.startswith("Error:")
    assert "outside the permitted working directory" in result


def test_not_a_directory(work_dir):
    result = get_files_info(str(work_dir), "hello.txt")
    assert result.startswith("Error:")
    assert "is not a directory" in result


def test_empty_directory(tmp_path):
    empty = tmp_path / "empty"
    empty.mkdir()
    result = get_files_info(str(tmp_path), "empty")
    assert result == ""
