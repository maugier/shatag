import shatag.base

class File(shatag.base.IFile):

    def read(self):
        self.ts = None
        self.shatag = None

    def write(self):
        pass


class Backend:
    """A stub backend that does not store tags and recomputes them each time."""
    def file(self,filename, db=None):
        return File(filename,db)
