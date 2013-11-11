from setuptools import setup, find_packages

version = '3.0a1dev'

install_requires = [
    'setuptools',
    'plone.autoform',
    'plone.app.form',
    'plone.app.registry',
    'plone.app.vocabularies',
    'plone.app.workflow',
    'plone.fieldsets',
    'plone.memoize',
    'plone.protect',
    'plone.locking',
    'zope.annotation',
    'zope.app.form',
    'zope.cachedescriptors',
    'zope.component',
    'zope.event',
    'zope.formlib',
    'zope.i18n',
    'zope.interface',
    'zope.ramcache',
    'zope.publisher',
    'zope.schema',
    'zope.site',
    'zope.testing',
    'Acquisition',
    'Products.CMFPlone',
    'Products.Archetypes',
    'Products.CMFCore',
    'Products.CMFDefault',
    'Products.PlonePAS',
    'Products.PortalTransforms',
    'Products.statusmessages',
    'Zope2>=2.13.0',
    'ZODB3',
]

setup(name='plone.app.controlpanel',
      version=version,
      description="Control panels for Plone.",
      long_description=open("README.txt").read() + "\n" +
      open("CHANGES.txt").read(),
      classifiers=[
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Zope2",
          "License :: OSI Approved :: GNU General Public License (GPL)",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
      ],
      keywords='plone controlpanel autoform z3cform registry',
      author='Plone Foundation',
      author_email='plone-developers@lists.sourceforge.net',
      url='http://pypi.python.org/pypi/plone.app.controlpanel',
      license='GPL version 2',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['plone', 'plone.app'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      extras_require={
          'test': [
              'plone.app.testing',
          ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
