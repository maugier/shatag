from setuptools import setup
setup(name='shatag',
      version = '0.2',
      description = 'File checksumming utility',
      author = 'Maxime Augier',
      author_email = 'max@xolus.net',
      url = 'http://bitbucket.org/maugier/shatag',
      packages = ['shatag','shatag.backend','shatag.store'],
      install_requires=['argparse'],
      scripts = ['bin/shatag', 'bin/shatag-add', 'bin/shatag-mkdb', 'bin/shatagd'])
