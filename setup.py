from setuptools import setup
setup(name='shatag',
      version = '0.4.1',
      description = 'File checksumming utility',
      author = 'Maxime Augier',
      author_email = 'max@xolus.net',
      url = 'http://bitbucket.org/maugier/shatag',
      packages = ['shatag','shatag.backend','shatag.store'],
      install_requires=['pyyaml','xattr'],
      entry_points={
          'console_scripts': [
              'shatag = shatag.cli.shatag:main',
              'shatag-add = shatag.cli.add:main',
              'shatagd = shatag.cli.shatagd:main'
          ]
      }
)
