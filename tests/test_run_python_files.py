import pytest
from functions.run_python_files import run_python_files


@pytest.fixture
def py_dir(tmp_path):
    (tmp_path / "hello.py").write_text('print("hello")', encoding="utf-8")
    (tmp_path / "with_args.py").write_text(
        "import sys\nprint(sys.argv[1])", encoding="utf-8"
    )
    (tmp_path / "exit_one.py").write_text("raise SystemExit(1)", encoding="utf-8")
    (tmp_path / "silent.py").write_text("pass", encoding="utf-8")
    (tmp_path / "not_python.txt").write_text("text", encoding="utf-8")
    return tmp_path


def test_happy_path_no_args(py_dir):
    result = run_python_files(str(py_dir), "hello.py")
    assert "hello" in result


def test_happy_path_with_args(py_dir):
    result = run_python_files(str(py_dir), "with_args.py", ["world"])
    assert "world" in result


def test_non_zero_exit_code(py_dir):
    result = run_python_files(str(py_dir), "exit_one.py")
    assert "Process exited with code" in result


def test_outside_boundary(py_dir):
    result = run_python_files(str(py_dir), "../main.py")
    assert result.startswith("Error:")
    assert "outside the permitted working directory" in result


def test_nonexistent_file(py_dir):
    result = run_python_files(str(py_dir), "no_such.py")
    assert result.startswith("Error:")
    assert "does not exist" in result


def test_no_output(py_dir):
    result = run_python_files(str(py_dir), "silent.py")
    assert result == "No output produced"


def test_non_python_file(py_dir):
    result = run_python_files(str(py_dir), "not_python.txt")
    assert result.startswith("Error:")
    assert "not a Python file" in result
