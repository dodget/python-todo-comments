from python_todo_comments import __version__
from python_todo_comments.main import main

# TODO: test comment


def test_version():
    assert __version__ == '0.2.0'


def test_main(capsys):
    main(args=["--dir", "./tests/"])
    captured = capsys.readouterr()
    print("HERE")
    print(captured.out)
    assert captured.out == "### tests/test_python_todo_comments.py\n- 4: test comment\n\n"
