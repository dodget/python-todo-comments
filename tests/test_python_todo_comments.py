from python_todo_comments import __version__
from python_todo_comments.main import main

# TODO: test comment


def test_version():
    assert __version__ == '0.2.6'


def test_main(capsys):
    main(args=["--dir", "./tests/"])
    captured = capsys.readouterr()
    expected_out = "### tests/test_python_todo_comments.py\n\n- 4: test comment\n\n"
    assert captured.out == expected_out