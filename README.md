# Python # TODO:  


This project provides a cli that takes a directory as an argument, and returns the `# TODO:` comments from all the python modules under that directory.

It will output in a markdown-friendly way, and is meant as a repeatable way to keep on top of all of the little todos that are peppered throughout a project.


## Installation

`pip install python-todo-comments`



## Usage

The basic command is `py-todos` combined with the following arguments:

- No argument: will search and parse the current working directory
- `-d` or `--dir` will search and parse the directory provided
- `-o` or `--output` will write the output to the provided filename
- `-h` or `--help` will provide the command's help context