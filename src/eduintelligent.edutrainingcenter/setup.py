from setuptools import setup, find_packages
import os

version = '0.1'

setup(name='eduintelligent.edutrainingcenter',
      version=version,
      description="eduIntelligent Training center",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
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
      url='http://code.iservices.com.mx',
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
