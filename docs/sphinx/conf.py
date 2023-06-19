# Add the path to project's root directory parent
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Add the path to module(s)
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..',
#                                                'cpu_health_checks')))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'cpu_health_checks'
copyright = '2023, Felipe Santana Rojas'
author = 'Felipe Santana Rojas'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.autosummary', 'sphinx.ext.autosectionlabel']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Specify the new path for the main documentation file
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# Exclude the bcolors class from documentation
def skip_member_handler(app, what, name, obj, skip, options):
    if name == 'bcolors':
        return True
    return None


def setup(app):
    app.connect("autodoc-skip-member", skip_member_handler)


# Include both class docstring and __init__ docstring
autoclass_content = 'both'
