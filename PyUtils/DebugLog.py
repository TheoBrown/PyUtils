'''
Created on Aug 22, 2014

@author: TPB
'''
import logging
import logging.handlers
import datetime as dt

class TBLogger(logging.Logger):
    """A simple wrapper for the logging class with built in stream handeling and ASCII color formatting
    """

    def __init__(self,moduleName ,log_filename = 'Logs/test.out' ,level = 'debug', module = 'Main' , maxSize = 1500000, maxCount = 5, streamLevel = 'debug',useColor = True ,rotateFiles = False, fileMode= 'a'):
        self.moduleName = moduleName
        self.logLevel = logLevel(level)
        self.fileMode = fileMode
        self.fileName = log_filename
        self.streamLevel = streamLevel
        logging.Logger.__init__(self, self.moduleName, self.logLevel) 

        self.fileformat = logging.Formatter('%(asctime)s ::%(levelname)8s:: %(name)15s:: %(message)s')
        
        if rotateFiles:
            self.fileHandler = logging.handlers.RotatingFileHandler(log_filename,
                                                                    mode = fileMode,
                                                                   maxBytes= maxSize,
                                                                   backupCount= maxCount,
                                                               )
        else:
            self.fileHandler = logging.FileHandler(filename=log_filename,
                                                    mode=self.fileMode)
        self.fileHandler.setFormatter(self.fileformat)
        self.fileHandler.setLevel(self.logLevel)
        self.addHandler(self.fileHandler)
        if streamLevel:
            FORMAT = "[%(asctime)s ][$BOLD%(name)-60s$RESET][%(levelname)-20s] %(message)-100s ($BOLD%(filename)s$RESET:%(lineno)d)"
            COLOR_FORMAT = formatter_message(FORMAT, True)
            self.colorStreamFormatter = ColoredFormatter(COLOR_FORMAT)
            self.consoleHandler = logging.StreamHandler()
            self.consoleHandler.setFormatter(self.colorStreamFormatter)
            self.addHandler(self.consoleHandler)

        self.propagate = False
        return
    
    def MakeChild(self,name = __name__, level_name = 'info',usestream = True,usefile= True):
        '''creates a child of the root log
        '''
        childlog = self.getChild(name)
        childlog.setLevel(logLevel(level_name))
        if usefile:
            childlog.addHandler(self.fileHandler)
        if self.streamLevel and usestream:
            childlog.addHandler(self.consoleHandler)
        childlog.propagate = False
        return childlog
    
    def changeLevel(self,newLevel):
        if self.fileHandler != None:
            self.fileHandler.setLevel(logLevel(newLevel))
        if self.consoleHandler != None:
            self.consoleHandler.setLevel(logLevel(newLevel))

def makeDescendent(rootLogger,descendantName,descendentLevel = 'info'):
    """This is necessary if you are trying to make a child 
    from a child logger (ie a logger that is not the TBLogger type)
    """
    rootType = str(type(rootLogger))
    if 'TBLogger' in rootType:
        return rootLogger.MakeChild(descendantName,descendentLevel)
    else:
        newChild = rootLogger.getChild(descendantName)
        newChild.propage = False
        return newChild
    
def logLevel(level):
    LEVELS = {'debug':logging.DEBUG,
          'info':logging.INFO,
          'warning':logging.WARNING,
          'error':logging.ERROR,
          'critical':logging.CRITICAL,
          }
    loglvl = LEVELS.get(level, logging.NOTSET)
    return loglvl
                                                       


#------------------------------------------------------------------------------ Colro Formatter Setup
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)
#The background is set with 40 plus the number of the color, and the foreground with 30

#These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"

def formatter_message(message, use_color = True):
    if use_color:
        message = message.replace("$RESET", RESET_SEQ).replace("$BOLD", BOLD_SEQ)
    else:
        message = message.replace("$RESET", "").replace("$BOLD", "")
    return message

COLORS = {
    'WARNING': YELLOW,
    'INFO': WHITE,
    'DEBUG': BLUE,
    'CRITICAL': YELLOW,
    'ERROR': RED
}

class ColoredFormatter(logging.Formatter):

    def __init__(self, msg, use_color = True,timeFormat = None):
        logging.Formatter.__init__(self, msg)
        self.use_color = use_color
        self.converter= dt.datetime.fromtimestamp

    def format(self, record):
        levelname = record.levelname
        recordName =  record.name
        if self.use_color and levelname in COLORS:
            levelname_color = COLOR_SEQ % (30 + COLORS[levelname]) + levelname + RESET_SEQ
            recordName_color =  COLOR_SEQ % (30 + CYAN) + recordName + RESET_SEQ
            record.levelname = levelname_color
            record.name = recordName_color
        return logging.Formatter.format(self, record)
    
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%H:%M:%S")
            s = "%s.%03d" % (t, record.msecs)
            color_s = COLOR_SEQ % (30 + GREEN) + s + RESET_SEQ
        return color_s

    
