import os
import sys


sys.path.append(os.path.abspath('..'))

project = 'RestAPIz14'
copyright = '2024, Dorota'
author = 'Dorota'


extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


html_theme = 'nature'
html_static_path = ['_static']
