# -- Project information -----------------------------------------------------

from avfilters import __version__

project = "avfilters"
copyright = "2024, Jérome Eertmans"
author = "Jérome Eertmans"
version = __version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # Built-in
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.githubpages",
    "sphinx.ext.mathjax",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    # Additional
    "sphinxext.opengraph",
    "sphinx_autodoc_typehints",
    "sphinx_copybutton",
]

templates_path = ["_templates"]
exclude_patterns = []

add_module_names = False
add_function_parentheses = False

# -- Intersphinx mapping

intersphinx_mapping = {
    "av": ("https://pyav.org/docs/stable/", None),
    "python": ("https://docs.python.org/3", None),
}

# -- OpenGraph settings

ogp_site_url = "https://avfilters.readthedocs.org"
ogp_use_first_image = True

# -- Sphinx autodoc typehints settings

always_document_param_types = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"
html_static_path = []

html_theme_options = {
    "show_toc_level": 2,
    "path_to_docs": "docs/source",
    "repository_url": "https://github.com/jeertmans/avfilters",
    "repository_branch": "main",
    "use_edit_page_button": True,
    "use_source_button": True,
    "use_issues_button": True,
    "use_repository_button": True,
    "navigation_with_keys": False,
}

autosummary_generate = False
napolean_use_rtype = False
