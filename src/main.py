#!/usr/bin/env python
import sys
import re
import types
from pathlib import Path
from itertools import dropwhile, takewhile


class PathDecorator:
    def __init__(self, path):
        self.path = path

    @property
    def name(self):
        name = self.path.name
        if self.path.is_dir():
            name = name + "/"

        return name

    def is_hidden(self):
        return self.path.name.startswith(".")


def _content_between_delimiter(delimiter):
    comment_prefix = re.compile(r"^#\s?")
    with open(__file__, "r") as f:
        framework_code = dropwhile(lambda l: l.strip() != delimiter, f)
        # Skip the delimiter line
        next(framework_code)
        framework_code = "".join(
            [
                # Remove all the preceding comments
                comment_prefix.sub("", l)
                for l in takewhile(lambda l: l.strip() != delimiter, framework_code)
            ]
        )
        return framework_code


def get_css():
    return _content_between_delimiter("# CSS")


def get_js():
    return _content_between_delimiter("# JS")


def get_bottle_module():
    framework_code = _content_between_delimiter("# BOTTLEPY")
    bottle_module = types.ModuleType("bottle")
    bottle_module.__file__ = __file__
    exec(framework_code, bottle_module.__dict__)
    return bottle_module


bottle = get_bottle_module()


INDEX_PAGE = """
{{!html_page}}
"""
CSS = get_css()
JS = get_js()
# Use the passed in argument for path if not use the current working directory
ROOT_PATH = (
    Path(sys.argv[1]).absolute().resolve() if 1 < len(sys.argv) else Path().resolve()
)

fallback_upload_path = Path(ROOT_PATH).joinpath("uploads")
fallback_upload_path.mkdir(parents=True, exist_ok=True)
UPLOAD_PATH = sys.argv[2] if len(sys.argv) >= 3 else str(fallback_upload_path)

print(f"\nServing from {ROOT_PATH}\n")
print(f"\nUploads will be received to {UPLOAD_PATH}\n")


def _root_layout(**contents):
    arguments = dict(CSS=CSS, JS=JS, **contents)
    return bottle.template(INDEX_PAGE, **arguments)


def _render_directory_listing(path: Path):
    files = []
    dirs = []
    # To split the dirs and files
    for node in path.iterdir():
        if node.is_dir():
            dirs.append(node)
        else:
            files.append(node)

    # Dirs come before files in the list
    files_and_directories_in_path = [PathDecorator(p) for p in [*dirs, *files]]
    files_and_directories_in_path = filter(
        lambda n: not n.is_hidden(), files_and_directories_in_path
    )
    return _root_layout(contents=files_and_directories_in_path)


@bottle.post("/upload")
def upload():
    target_directory = bottle.request.params.get('target_directory')
    upload = bottle.request.files.get("upload")
    upload_path = UPLOAD_PATH
    if target_directory:
        upload_path = Path(UPLOAD_PATH).joinpath(target_directory)
        upload_path.mkdir(parents=True, exist_ok=True)
    # Read as 4MB chunks
    upload.save(str(upload_path), chunk_size=(1024 * 1024 * 4))
    return "OK"


@bottle.get("/")
@bottle.get("<path:path>")
def root(path=ROOT_PATH):
    requested_path = Path(path)
    if requested_path.name == "favicon.ico":
        bottle.abort(404)
    elif requested_path.is_dir():
        print(f"Serving directory {requested_path}")
        return _render_directory_listing(requested_path)
    else:
        filename = requested_path.name
        print(f"Serving file {filename}")
        return bottle.static_file(
            str(requested_path.relative_to(ROOT_PATH)),
            root=ROOT_PATH,
            download=filename,
        )


def main():
    bottle.run(host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()

# FRAMEWORK EMBEDDED IN THE SAME FILE TO KEEP IT IN A SINGLE FILE
# BOTTLEPY
{{!bottlepy}}
# BOTTLEPY
#
# CSS
{{!css}}
# CSS
#
# JS
{{!js}}
# JS
