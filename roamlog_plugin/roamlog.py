import sqlite3
import time
import os
import struct
from PyQt4.QtCore import Qt, QObject, pyqtSignal, QThread, QEvent
from PyQt4.QtGui import *
from PyQt4.uic import loadUiType

import roam.api.utils
from roam.flickwidget import FlickCharm
from roam.api.events import RoamEvents
from roam.api.plugins import Page


from roam.utils import log, debug
import getpass

def resolve(name):
    f = os.path.join(os.path.dirname(__file__), name)
    return f

widget, base = loadUiType(resolve("roamlog.ui"))

# class Example(QWidget):    
    # def __init__(self):
        # super(Example, self).__init__()        
        # self.initUI()
        
    # def initUI(self):
        # self.btn = QPushButton('Dialog', self)
        # self.btn.move(20, 20)
        # self.btn.clicked.connect(self.showDialog)
        
        # self.le = QLineEdit(self)
        # self.le.move(130, 22)
        
        # self.setGeometry(300, 300, 290, 150)
        # self.setWindowTitle('Input dialog')
        # self.show()
        
    # def showDialog(self):        
        # text, ok = QInputDialog.getText(self, 'Input Dialog', 
            # 'Enter your name:')        
        # if ok:
            # self.le.setText(str(text))
            
            
class RoamLogPlugin(widget, base, Page):
    title = "Roam Log"
    icon = resolve("roamlog.svg")

    def __init__(self, api, parent=None):
        super(RoamLogPlugin, self).__init__(parent)
        self.setupUi(self)
        self.api = api
        self.project = None        
        self.refreshLogButton.pressed.connect(self.refreshLog)        

    def project_loaded(self, project):
        self.project = project
        
    def refreshLog(self):   
        try:
            logpath = os.path.join(os.environ['ROAM_APPPATH'], 'log')
        except KeyError:
            logpath = 'log'
            
        LOG_FILENAME = os.path.join(logpath, "{}_roam.log".format(getpass.getuser()))
        projectDir = os.path.dirname(self.project.folder)
        roamDir = os.path.dirname(projectDir)       
        LOG_FILENAME = os.path.join(roamDir, LOG_FILENAME)

        with open(LOG_FILENAME, 'r') as logFile:
            logText = logFile.read()
            
        self.logTextBrowser.setText(logText)
        self.logTextBrowser.moveCursor(QTextCursor.End)
        
        
        




