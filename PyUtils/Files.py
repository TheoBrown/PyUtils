'''
Created on Aug 22, 2014

@author: TPB
'''


import os
from os import listdir
from os.path import join, isfile, isdir

from PyUtils.DebugLog import TBLogger
import GlobalConfig


#logging
FileRootLog = TBLogger(GlobalConfig.logpath+__name__+'.out','info','Files')

#------------------------------------------------------------------------------ File Type Verification
def verifyFileType(filePath,allowedExtensions = []):
    """
    @param fileNode: directory to search for files in
    @param allowedExtensions: list of acceptable file extensions to return
    """
    if isfile(filePath):
        ext = filePath.split(".")[-1]
        if (ext in allowedExtensions) or len(allowedExtensions) == 0:
    #         self.logger.debug("file %s had ext %s" %(fileName,ext))
            return True
        else: 
    #         self.logger.debug("file %s incorrect extension %s" %(fileName, ext))
            return False
    else: return False
    
def verifiyFileExtension(fileName,allowedExtensions = []):
    ext = fileName.split(".")[-1]
    if (ext in allowedExtensions):
#         self.logger.debug("file %s had ext %s" %(fileName,ext))
        return True
    else: 
#         self.logger.debug("file %s incorrect extension %s" %(fileName, ext))
        return False
    

#------------------------------------------------------------------------------ File Path Extraction/Construction
def getNameFromPath(filePath):
    cleanPath = filePath.strip('/')
    lastNode = cleanPath.split('/')[-1]
    return lastNode

def getRelativeDirectoryName(filePath,rootDirectory):
    relativePath = filePath.split(rootDirectory)[-1]
    return relativePath

def constructFilePathFromKeyList(keyList):
    """
    builds a usable file path from a list of nodes, should start with root node at keyList[0]
    """
    prevKey = None
    filePath = None
    for fileKey in keyList:
        if prevKey == None:
            filePath = join(fileKey)
        filePath = join(prevKey,fileKey)
        prevKey = filePath
    return filePath
#------------------------------------------------------------------------------ File System Modification
def ensure_dir(d):
    if not os.path.exists(d):
        os.makedirs(d)
#------------------------------------------------------------------------------ File System Querys
def getDirectorysAtNode(fileNode):
    retList = [dirID for dirID in listdir(fileNode) if isdir(join(fileNode,dirID))]
    return retList

def getFilesAtNode(fileNode, allowedExtensions = [],fullPath = False):
    """
    @param fileNode: directory to search for files in
    @param allowedExtensions: list of acceptable file extensions to return
    @param fullPath: return full path or just file name
    """
    if fullPath == False:
        retList = [filID for filID in listdir(fileNode) if verifyFileType(join(fileNode,filID),allowedExtensions)]
#         retList = [filID for filID in listdir(fileNode) if isfile(join(fileNode,filID)) and verifiyFileExtension(join(fileNode,filID))]
    else:
        retList = [join(fileNode,filID) for filID in listdir(fileNode) if verifyFileType(join(fileNode,filID),allowedExtensions)]

    return retList

def getFilesInDirectory(dirName, extString= None,absolutePath = True):
    fileList = [f for f in listdir(dirName) if isfile(join(dirName,f)) and checkExtension(f, extString)]
    if absolutePath:
        return [join(dirName,f) for f in fileList]
    else:
        return fileList
        
        
def checkExtension(fileName,extString):
    """
    @param fileName: string
    @param extString: string that should appear at end of file
    @return: true if file contains extension or no extension given
    """
    if extString != None:
        return (fileName[-len(extString)]==extString)
    else:
        return True
    
def filesinpath(path_list):
    log_files = list()
    FileRootLog.rootlog.debug( 'path list:',path_list)
    for path in path_list:
        FileRootLog.rootlog.debug( 'path entry in list :', path)
        for filename in os.listdir(path):
            FileRootLog.rootlog.debug( path, filename)
            log_files.append(filename)
    return log_files


#------------------------------------------------------------------------------ Unicode String Manipulation
def convertString(oldString):
    newstring = oldString.translate(ascii_map())
    return newstring

def ascii_map():
    data={}
    for num in range(256):
        h=num
        filename='x{num:02x}'.format(num=num)
        try:
            mod = __import__('unidecode.'+filename,
                             fromlist=True)
        except ImportError:
            pass
        else:
            for l,val in enumerate(mod.data):
                i=h<<8
                i+=l
                if i >= 0x80:
                    data[i]=unicode(val)
    return data

def string_filter(flist,filterlist):
    """ a simple method to find files containg a string such as .csv or .pickle
    @param flist: a list of file paths
    @param filterlist: a list of strings that should be in the file name  
    """
    filterd_files = list()
    for name in flist:
        for fil in filterlist:
            if fil in name :
                FileRootLog.rootlog.debug( "File Found with %s in name: %s" %(fil, name))
                filterd_files.append(name)
    return filterd_files
