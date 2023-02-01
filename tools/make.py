#!/usr/bin/env python3

# Script to create a single file_server.py from all the files in src directory

import os
import sys

from pathlib import Path

current_filepath = Path(__file__)
current_dirpath = current_filepath.parent
src_dirpath = current_dirpath.parent.joinpath("src")

sys.path.insert(0, str(src_dirpath))

import bottle


def report_and_abort_on_missing_file(filepath: Path):
    if not filepath.exists():
        print(f"File missing: {filepath}. Aborting!", file=sys.stderr)
        sys.exit(1)


report_and_abort_on_missing_file(html_file := src_dirpath.joinpath("index.html"))
report_and_abort_on_missing_file(bottle_py_file := src_dirpath.joinpath("bottle.py"))
report_and_abort_on_missing_file(css_file := src_dirpath.joinpath("index.css"))
report_and_abort_on_missing_file(js_file := src_dirpath.joinpath("index.js"))
report_and_abort_on_missing_file(main_py_file := src_dirpath.joinpath("main.py"))


def _read_as_comment(filepath: Path):
    content = filepath.read_text()
    return os.linesep.join([f"# {line}" for line in content.splitlines()])


# main
def make():
    arguments = dict(
        noescape=True,
        js=_read_as_comment(js_file),
        css=_read_as_comment(css_file),
        html_page=html_file.read_text(),
        bottlepy=_read_as_comment(bottle_py_file),
    )
    consolidated_file = bottle.template(main_py_file.read_text(), **arguments)
    new_file = current_dirpath.parent.joinpath("new_file_server.py")
    new_file.write_text(consolidated_file)


if __name__ == "__main__":
    make()
