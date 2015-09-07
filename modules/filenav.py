from twisted.python.filepath import FilePath
import Logger

def similarChild(c, newdir):
    print("calling similarChild")
    s = sorted(newdir.children(), reverse=True, key=lambda a: a.getModificationTime())
    return FileNav(s[0])


class FileNav(object):
    """
    Provides a next, previous, current file interface.  Just
    initialize it with a starting file and then you can do stuff like
    this:
    >>> a = FileNav(FilePath('a'))
    >>> a.next()
    >>> a.previous()
    >>> a.current()
    """

    def __init__(self, fp, sortbyname=False):
        self.logger = Logger.Logger(self.__class__.__name__).get()
        self.logger.debug("initilizing filenav with " + str(fp) + " and sortbyname="+str(sortbyname))
        self._current = fp
        self.sortbyname = sortbyname

    def setCurrent(self, current):
        self.logger.debug("setting current file to " + str(current))
        if not isinstance(current, FilePath):
            raise RuntimeError("%r is not a FilePath object" % current)
        self._current = current

    def getCurrent(self):
        self.logger.debug("returning current as " + str(self._current))
        return self._current

    current = property(getCurrent, setCurrent)

    def _sortall(self):
        self.logger.debug("calling _sortall")
        if self.sortbyname:
            res = sorted(self.current.parent().children(), key=lambda a: (a, a.getModificationTime()))
        else:
            res = sorted(self.current.parent().children(), key=lambda a: a.getModificationTime())
        return res

    def getPrevious(self):
        self.logger.debug("calling getPrevious")
        all = self._sortall()
        z = all.index(self.current)
        self._current = all[z-1]
        return all[z-1]

    previous = property(getPrevious)

    def getNext(self):
        self.logger.debug("calling getNext")
        all = self._sortall()
        z = all.index(self.current)
        z = (z+1) % len(all)
        self._current = all[z]
        return all[z]

    next = property(getNext)

if __name__ == '__main__':
    print "filenav.py is NOT intended to be started from command line  ... "
