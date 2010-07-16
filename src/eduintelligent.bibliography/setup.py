from setuptools import setup, find_packages

version = '0.1'

setup(name='eduintelligent.bibliography',
      version=version,
      description="Bilbiography container for books, magazines and publications.",
      long_description="""\
This is a bilbiography container. Can contain references to books, publications
and magazines.

It was an experiment.
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Intended Audience :: Education",
        "Topic :: Education :: Computer Aided Instruction (CAI)",
        ],
      keywords='',
      author='Erik Rivera Morales',
      author_email='erik@iservices.com.mx',
      url='http://iservices.com.mx',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eduintelligent'],
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
