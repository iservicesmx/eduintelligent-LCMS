import logging
import os
import os.path
import zipfile


logger = logging.getLogger('eduintelligent.zipcontent')


def LOG(message, summary='',severity=logging.INFO):
    logger.log(severity, '%s \n%s', summary, message)
    
def removeDirectory(path):
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
            #print 'removing file', os.path.join(root, name)
        for name in dirs:
            os.rmdir(os.path.join(root, name))
            #print 'removing directory', os.path.join(root, name)
    os.rmdir(path)

def createDirectory(path):
    #os.makedirs(path, 0774)
    os.makedirs(path)


def walker(directory):
    for name in os.listdir(directory):
        path = os.path.join(directory,name)
        if os.path.isdir(path):
            f = open(os.path.join(path,'robots.txt'))
            f.write(""" """)
            f.close()
            f = open(os.path.join(path,'.htaccess'))
            f.write(""" """)
            f.close()
            
            walker(path)

def listdir(startDir):
    files = []
    directories = [startDir]
    while len(directories)>0:
        directory = directories.pop()
        for name in os.listdir(directory):
            fullpath = os.path.join(directory,name)
            if os.path.isfile(fullpath):
                files.append(fullpath.replace(startDir+"/",""))
            elif os.path.isdir(fullpath):
                files.append(fullpath.replace(startDir+"/",""))
                directories.append(fullpath)
    return files

class unzip:
    """ unzip
        Version: 1.1

        Extract a zipfile to the directory provided
        It first creates the directory structure to house the files
        then it extracts the files to it.

        python class
        import unzip
        un = unzip.unzip()
        un.extract(r'c:\testfile.zip', 'c:\testoutput')

        By Doug Tolton
    """
    def __init__(self, verbose = False, percent = 10):
        self.verbose = verbose
        self.percent = percent

    def extract(self, file, directory):
        zf = zipfile.ZipFile(file)

        # create directory structure to house files
        self._createstructure(file, directory)

        # extract files to directory structure
        for i, name in enumerate(zf.namelist()):
            if not name.endswith('/'):
                outfile = open(os.path.join(directory, name), 'wb')
                outfile.write(zf.read(name))
                outfile.flush()
                outfile.close()

    def _createstructure(self, file, dir):
        self._makedirs(self._listdirs(file), dir)


    def _makedirs(self, directories, basedir):
        """ Create any directories that don't currently exist """
        for dir in directories:
            curdir = os.path.join(basedir, dir)
            if not os.path.exists(curdir):
                os.mkdir(curdir)

    def _listdirs(self, file):
        """ Grabs all the directories in the zip structure
        This is necessary to create the structure before trying
        to extract the file to it. """
        zf = zipfile.ZipFile(file)

        dirs = []

        for name in zf.namelist():
            if name.endswith('/'):
                dirs.append(name)

        dirs.sort()
        return dirs


def patchXmlNsDeclaration(src):
    """ Workaround for strict handling or xml namespace by minidom.
    """
    xmlNsDeclaration = 'xmlns:xml="http://www.w3.org/1998/namespace"'
    if src.find(xmlNsDeclaration) == -1:
        return src.replace('xmlns:xsi', '%s xmlns:xsi' % xmlNsDeclaration)
    else:
        return src
