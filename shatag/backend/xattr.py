import shatag.base
import xattr

class File(shatag.base.IFile):
    name = "Xattr store" 
    def read(self):

        try:
            self.ts = float(xattr.getxattr(self.filename, 'user.shatag.ts'))
            self.shatag = xattr.getxattr(self.filename, 'user.shatag.sha256').decode('ascii')
        except IOError as e:
            if e.errno != 61:  # no tag present
               raise e

    def write(self):
        xattr.setxattr(self.filename, 'user.shatag.sha256', self.shatag.encode('ascii'))
        xattr.setxattr(self.filename, 'user.shatag.ts', str(self.mtime).encode('ascii'))


class Backend:
    """A backend that stores the tags in POSIX extended attributes"""
    def file(self,filename, db=None):
        return File(filename,db)
