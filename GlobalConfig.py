import os
import socket
import sys
rdir = os.getcwd()
# sys.stderr = sys.stdout
        
hostname = socket.gethostname()
rootpath = os.getcwd()


logLevel = 'debug'
consoledbg = 'debug'

datapath = rootpath + '/Data/'
resultpath = datapath + 'Results/'
logpath = rootpath + '/Logs/'
templatepath = datapath+'templates/'
tempimg = templatepath+'img/'
tempinfo = templatepath+'info/'

datadir = {'dante-EX58-UD4P':{'db':'diagnostics',
                     'picklepath':'/var/www/iReport/data/',
                     'sqlserver' :'ddproc.cloudapp.net',
                     'debug':True
                     },
        'li614-103':{'db':'Diagnostics', 
                     'picklepath' : '/var/www/remoteProcessor/data/',
                      'sqlserver' :'ddprocessor.cloudapp.net',
                     'user':'test',
                     'pass':'test',
                    'debug':False

                     }
        }

from PyUtils.Files import ensure_dir

ensure_dir(logpath)
