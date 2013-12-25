import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid==1.5a1',
    'pyramid_zodbconn',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'waitress',
    'ZODB3',
    'pyramid_mako',
    'pyramid_chameleon',
    'plim',
    'deform',
    'pyramid_deform',
    'pyramid_beaker',
    'deform_bootstrap',
    'tweepy',
    'facebook',
    'pyramid_mailer',
    'venusian',
    'webob',
    #'repoze.folder',
    #'repoze.retry',
    #'repoze.tm2==1.0',
    #'repoze.zodbconn',
    ]

setup(name='projeto',
      version='0.0',
      description='projeto',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      install_requires=requires,
      tests_require=requires,
      test_suite="projeto",
      entry_points="""\
      [paste.app_factory]
      main = projeto:main
      """,
      )
