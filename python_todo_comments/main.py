#!/usr/bin/env python

import argparse
from contextlib import contextmanager, redirect_stdout
from dataclasses import dataclass, field
from datetime import datetime
import io
from pathlib import Path, PosixPath
import time
import tokenize
from typing import List
import sys


class Color:
    CYAN = '\033[1;36;48m'
    GREEN = '\033[1;32;48m'
    YELLOW = '\033[1;33;48m'
    RED = '\033[1;31;48m'
    END = '\033[1;37;0m'


@dataclass
class ToDoDirectory:
    name: str
    todos: List[str] = field(default_factory=list)


@contextmanager
def directory_writer(dir: str):
    try:
        todo_dir = ToDoDirectory(name=dir)
        yield todo_dir
    finally:
        if len(todo_dir.todos) > 0:
            sys.stdout.write(f"## {todo_dir.name} ({len(todo_dir.todos)})\n")
            for idx, comment in enumerate(todo_dir.todos):
                sys.stdout.write(f"{idx+1}. {comment}\n")
            sys.stdout.write("\n")


class ToDoParser:

    def __init__(self, search_dir: str, output_file: str = None):
        self.start: int = time.monotonic_ns()
        self.output_file = output_file
        self.search_dir = search_dir
        self.module_count: int = len(list(Path(self.search_dir).rglob("*.py")))
        self.todo_count: int = 0

    def process(self):
        if self.output_file:
            with open(self.output_file, "w") as f:
                with redirect_stdout(f):
                    self.iterate_paths()
        else:
            self.iterate_paths()

        sys.stdout.write(f"{Color.GREEN}Found {self.todo_count} todos while parsing {self.module_count} python modules in {self.processing_time()} seconds{Color.END}\n")
        if self.output_file:
            sys.stdout.write(f"{Color.CYAN}Output written to {self.output_file}{Color.END}\n")
        return None

    def iterate_paths(self) -> None:
        self.write_header()
        for path in Path(self.search_dir).rglob("*.py"):
            self.find_todos(path)
        return None

    def find_todos(self, path: PosixPath) -> None:
        directory, _, file_name = str(path).rpartition("/")
        with directory_writer(directory) as writer:
            with open(path, "r", encoding="utf-8") as f:
                contents = f.read()
                tokens = tokenize.tokenize(io.BytesIO(contents.encode()).readline)
                for toknum, tokstring, tokloc, _, _ in tokens:
                    if toknum is tokenize.COMMENT:
                        if tokstring.startswith("# TODO: "):
                            comment_content = tokstring.replace("# TODO: ", "")
                            writer.todos.append(f"{file_name}:{tokloc[0]}    {comment_content}")
                            self.todo_count += 1
        return None

    def processing_time(self) -> float:
        return round((time.monotonic_ns() - self.start)/1000000000, 4)

    @staticmethod
    def write_header() -> None:
        sys.stdout.write("# Python # TODO: comments\n\n")
        today = datetime.utcfromtimestamp(time.time()).strftime('%A, %b %d %H:%M')
        sys.stdout.write(f"{today}\n\n")


def parse_args(args):
    parser = argparse.ArgumentParser(description="A command to get the todos out of python modules")
    parser.add_argument("-d", "--dir", nargs="?", default=".", help="The directory to search for todos")
    parser.add_argument("-o", "--output", help="The name of the file to output to")
    return parser.parse_args(args)


def main(args=sys.argv[1:]) -> int:
    arguments = parse_args(args)
    try:
        parser = ToDoParser(arguments.dir, output_file=arguments.output)
        parser.process()
    except Exception as e:
        sys.stderr.write(str(e))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
