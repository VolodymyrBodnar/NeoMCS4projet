
## 1. Install Sphinx
pip install sphinx

## 2. Create Documentation Structure
sphinx-quickstart

## 3. Build HTML Documentation
make html

## 4. Add Docstrings in Code (Example)
"""This is an example docstring."""

## 5. Auto-Generate Documentation
sphinx-apidoc -o docs/source your_project

## 6. Configure `conf.py`
Modify extensions:
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']

## 7. Serve Locally
python -m http.server -d build/html