from datetime import UTC, datetime

from pybuoy import __version__

autodoc_member_order = "bysource"
copyright = f"{datetime.now(UTC).year}, Kyle J. Burda"
exclude_patterns = ["_build"]
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
html_static_path = ["_static"]
html_theme = "furo"
htmlhelp_basename = "pybuoy"
project = htmlhelp_basename
release = __version__
root_doc = "index"


def setup(app):
    app.add_css_file("theme_override.css")
