from importlib.metadata import PackageNotFoundError, version as _version

project = "fqdn"
author = "ypcrts"
copyright = "2017, ypcrts"

try:
    release = _version("fqdn")
except PackageNotFoundError:
    release = "0.0.0"
version = release

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
]

source_suffix = {".rst": "restructuredtext", ".md": "markdown"}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# The README is included verbatim and uses GitHub-style anchor links.
suppress_warnings = ["myst.xref_missing"]

html_theme = "alabaster"
html_theme_options = {"nosidebar": True}
