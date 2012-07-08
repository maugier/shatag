from setuptools import setup
setup(name='shatag',
      version = '0.4',
      description = 'File checksumming utility',
      author = 'Maxime Augier',
      author_email = 'max@xolus.net',
      url = 'http://bitbucket.org/maugier/shatag',
      packages = ['shatag','shatag.backend','shatag.store'],
      #install_requires=['argparse'],
      scripts = ['bin/shatag', 'bin/shatag-add', 'bin/shatagd'])
