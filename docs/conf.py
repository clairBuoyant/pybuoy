from datetime import datetime

from pybuoy import __version__

copyright = datetime.today().strftime("%Y, Kyle J. Burda")
exclude_patterns = ["_build"]
extensions = ["sphinx.ext.autodoc"]
html_static_path = ["_static"]
html_theme = "furo"
htmlhelp_basename = "pybuoy"
project = htmlhelp_basename
release = __version__
root_doc = "index"
templates_path = ["_templates"]


def skip(app, what, name, obj, skip, options):
    if name in {
        "__call__",
        "__contains__",
        "__getitem__",
        "__init__",
        "__iter__",
        "__len__",
    }:
        return False
    return skip


def setup(app):
    app.connect("autodoc-skip-member", skip)
    app.add_css_file("theme_override.css")
