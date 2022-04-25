#!/usr/bin/env python

import argparse
from contextlib import redirect_stdout
import io
from pathlib import Path
import tokenize
import sys


def search_file_for_todos(path):
    with open(path, "r", encoding="utf-8") as f:
        contents = f.read()
        tokens = tokenize.tokenize(io.BytesIO(contents.encode()).readline)
        todos = [f"### {path}\n\n", ]
        for toknum, tokstring, tokloc, _, _ in tokens:
            if toknum is tokenize.COMMENT:
                if tokstring.startswith("# TODO: "):
                    comment_content = tokstring.replace("# TODO: ", "")
                    todos.append(f"- {tokloc[0]}: {comment_content}\n")
        if len(todos) > 1:
            todos.append("\n")
            return todos
        return None


def write_todos(todos):
    if len(todos) > 0:
        for todo in todos:
            sys.stdout.write(todo)
    else:
        sys.stdout.write("No # TODO: comments found :)\n")


def todo_list(directory, output_file_name):
    all_todos = []
    for path in Path(directory).rglob("*.py"):
        todos = search_file_for_todos(path)
        if todos:
            all_todos.extend(todos)
    if output_file_name:
        with open(output_file_name, "w") as f:
            with redirect_stdout(f):
                write_todos(all_todos)
    else:
        write_todos(all_todos)


def parse_args(args):
    parser = argparse.ArgumentParser(description="A command to get the todos out of python modules")
    parser.add_argument("-d", "--dir", nargs="?", default=".", help="The directory to search for todos")
    parser.add_argument("-o", "--output", help="The name of the file to output to")
    return parser.parse_args(args)


def main(args=sys.argv[1:]) -> int:
    arguments = parse_args(args)
    try:
        todo_list(arguments.dir, arguments.output)
    except Exception as e:
        sys.stderr.write(str(e))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
