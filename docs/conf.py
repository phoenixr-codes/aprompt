#:==========================================
# Sphinx Documentation Builder Configuration
#:==========================================


#####################
# Project Information

project = 'aprompt'
copyright = '2023, phoenixR'
author = 'phoenixR'
release = '3.0.1'


###############
# Configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.napoleon',

    'myst_parser',
    'sphinx_copybutton',
]


#######################
# Autodoc Configuration

autodoc_default_options = dict.fromkeys('''
    members
    inherited-members
    undoc-members
    '''.split(),
    True
)
autodoc_member_order = 'bysource'
autodoc_typehints = 'both'
autoclass_content = 'both'
autodoc_type_aliases = {"PromptEngine": "aprompt.PromptEngine"}


###########################
# Intersphinx Configuration

intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'click': ('https://click.palletsprojects.com/en/8.1.x/', None),
}


############
# Find Files

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


###########################
# HTML Output Configuration

html_theme = 'furo'
html_static_path = ['_static']
