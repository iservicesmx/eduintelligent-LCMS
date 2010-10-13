from setuptools import setup, find_packages

version = '1.0'

setup(name='eduintelligent.courses',
      version=version,
      description="Course container for eduIntelligent",
      long_description="""\
eduintelligent.courses provide containers for online courses.
""",
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Erik Rivera Morales',
      author_email='erik@iservices.com.mx',
      url='http://www.iservices.com.mx',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['eduintelligent'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.PloneBoard'
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
