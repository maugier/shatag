from distutils.core import setup
setup(name='shatag',
      version = '0.1',
      description = 'File checksumming utility',
      author = 'Maxime Augier',
      author_email = 'max@xolus.net',
      url = 'http://bitbucket.org/maugier/shatag',
      py_modules = ['shatag'],
      scripts = ['shatag', 'shatag-add', 'shatag-mkdb'])
