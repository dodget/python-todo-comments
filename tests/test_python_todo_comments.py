from python_todo_comments import __version__
from python_todo_comments.main import main

# TODO: test comment


def test_version():
    assert __version__ == '0.3.0'


def test_main(capsys):
    main(args=["--dir", "./tests/"])
    captured = capsys.readouterr()
    expected_out = "## tests (1)\n1. test_python_todo_comments.py:4    test comment\n\n"
    assert expected_out in captured.out
