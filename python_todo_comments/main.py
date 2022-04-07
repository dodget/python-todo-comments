#!/usr/bin/env python

import io
from pathlib import Path
import tokenize
import sys


def search_file_for_todos(path):
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()
        tokens = tokenize.tokenize(io.BytesIO(contents.encode()).readline)
        todos = []
        for toknum, tokstring, tokloc, _, _ in tokens:
            if toknum is tokenize.COMMENT:
                if tokstring.startswith("# TODO: "):
                    comment_content = tokstring.replace("# TODO: ", "")
                    line_number = tokloc[0]
                    todos.append((comment_content, line_number))
        if len(todos) > 0:
            print(f"### {path}")
            for todo in todos:
                print(f"- {todo[1]}: {todo[0]}")
            print()


def todo_list(directory):
    for path in Path(directory).rglob("*.py"):
        search_file_for_todos(path)


def main(args=sys.argv) -> int:
    for dir in args:
        try:
            todo_list(dir)
        except Exception as e:
            sys.stderr.write(str(e))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
