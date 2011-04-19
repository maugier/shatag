from distutils.core import setup
setup(name='shatag',
      version = '0.1',
      description = 'File checksumming utility',
      author = 'Maxime Augier',
      author_email = 'max@xolus.net',
      url = 'http://bitbucket.org/maugier/shatag',
      packages = ['shatag'],
      scripts = ['bin/shatag', 'bin/shatag-add', 'bin/shatag-mkdb'])
