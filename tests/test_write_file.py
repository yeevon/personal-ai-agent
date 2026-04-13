from functions.write_to_file import write_file


def test_writes_file(work_dir):
    result = write_file(str(work_dir), "output.txt", "some content")
    assert "Successfully wrote" in result
    assert "12 characters written" in result
    assert (work_dir / "output.txt").read_text() == "some content"


def test_creates_nested_dirs(work_dir):
    result = write_file(str(work_dir), "new/deep/file.txt", "data")
    assert "Successfully wrote" in result
    assert (work_dir / "new" / "deep" / "file.txt").read_text() == "data"


def test_overwrites_existing_file(work_dir):
    write_file(str(work_dir), "hello.txt", "first")
    result = write_file(str(work_dir), "hello.txt", "second")
    assert "Successfully wrote" in result
    assert (work_dir / "hello.txt").read_text() == "second"


def test_outside_boundary(work_dir):
    result = write_file(str(work_dir), "/tmp/evil.txt", "bad")
    assert result.startswith("Error:")
    assert "outside the permitted working directory" in result


def test_target_is_directory(work_dir):
    result = write_file(str(work_dir), "sub", "content")
    assert result.startswith("Error:")
    assert "is a directory" in result
