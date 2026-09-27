from pathlib import Path
from logic import sort_files

def test_sort_files_creates_extension_folders(tmp_path):

    (tmp_path / "photo.jpg").write_text("fake image data")
    (tmp_path / "notes.txt").write_text("fake text data")

    result = sort_files(tmp_path)

    count, skip, extensions, failed_folders, failed_files = result

    assert count == 2
    assert extensions == {"JPG": 1, "TXT": 1}

def test_sort_files_handles_no_extension(tmp_path):

    (tmp_path / "README").write_text("no extension file")

    result = sort_files(tmp_path)

    count, skip, extensions, failed_folders, failed_files = result

    assert count == 1
    assert extensions == {"NO EXTENSION": 1}

def test_sort_files_skips_duplicates(tmp_path):

    (tmp_path / "JPG").mkdir()
    (tmp_path / "JPG" / "photo.jpg").write_text("already sorted file")
    (tmp_path / "photo.jpg").write_text("new incoming file")

    result = sort_files(tmp_path)
    
    count, skip, extensions, failed_folders, failed_files = result

    assert skip == 1
    assert count == 0

def test_sort_files_empty_folder(tmp_path):

    result = sort_files(tmp_path)

    count, skip, extensions, failed_folders, failed_files = result

    assert skip == 0
    assert count == 0
    assert extensions == {}
    