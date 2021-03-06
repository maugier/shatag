from os import fsencode
import shatag.base
import xattr
import errno

class File(shatag.base.IFile):
    name = "Xattr store" 
    def read(self):

        try:
            self.ts = xattr.getxattr(fsencode(self.filename), 'user.shatag.ts').decode('ascii')
            self.shatag = xattr.getxattr(fsencode(self.filename), 'user.shatag.sha256').decode('ascii')
        except IOError as e:
            if e.errno != errno.ENODATA:  # no tag present
               raise e

    def write(self):
        xattr.setxattr(fsencode(self.filename), 'user.shatag.sha256', self.shatag.encode('ascii'))
        xattr.setxattr(fsencode(self.filename), 'user.shatag.ts', self.mtime.encode('ascii'))


class Backend:
    """A backend that stores the tags in POSIX extended attributes"""
    def file(self,filename, db=None):
        return File(filename,db)
