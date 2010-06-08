from setuptools import setup, find_packages
import os

def _textFromPath(*names):
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, *names)
    return open(path, 'r').read().strip()

version = _textFromPath('Products', 'PloneArticle', 'version.txt')

long_description = (
    _textFromPath("Products", "PloneArticle", "README.txt")
    + "\n\n"
    + _textFromPath("Products", "PloneArticle", "CHANGES")
    + "\n")

setup(name='Products.PloneArticle',
      version=version,
      description="A Plone document including images, attachments and links, with a free choice of layout.",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          ],
      keywords='plone',
      author='Ingeniweb',
      author_email='support@ingeniweb.com',
      url='http://plone.org/products/plonearticle',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
