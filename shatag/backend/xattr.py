import shatag.base
import xattr

class File(shatag.base.IFile):
    name = "Xattr store" 
    def read(self):

        try:
            self.ts = int(xattr.getxattr(self.filename, 'user.shatag.ts'))
            self.shatag = xattr.getxattr(self.filename, 'user.shatag.sha256').decode('ascii')
        except IOError as e:
            if e.errno == 61:  # xattr support lacking in fs
               raise e

    def write(self):
        xattr.setxattr(self.filename, 'user.shatag.sha256', self.shatag.encode('ascii'))
        xattr.setxattr(self.filename, 'user.shatag.ts', str(self.mtime).encode('ascii'))


class Backend:
    def file(self,filename, db=None):
        return File(filename,db)
