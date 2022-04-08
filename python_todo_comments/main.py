#!/usr/bin/env python

import argparse
import io
import os
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


def parse_args(args):
    parser = argparse.ArgumentParser(description='A command to get the todos out of python modules')
    parser.add_argument('--dir', nargs='?', default=os.getcwd(), help='The directory to search for todos')
    return parser.parse_args(args)


def main(args=sys.argv[1:]) -> int:
    arguments = parse_args(args)
    try:
        todo_list(arguments.dir)
    except Exception as e:
        sys.stderr.write(str(e))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
