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

#regular expression module
import re

def resolve(name):
    f = os.path.join(os.path.dirname(__file__), name)
    return f

widget, base = loadUiType(resolve("syncclientlog.ui"))

            
class SyncClientLogPlugin(widget, base, Page):
    title = "SyncClient Log"
    icon = resolve("syncclientlog.svg")

    def __init__(self, api, parent=None):
        super(SyncClientLogPlugin, self).__init__(parent)
        self.setupUi(self)
        self.api = api
        self.project = None        
        self.refreshLogButton.pressed.connect(self.refreshLog)        
        self.truncateLogFileButton.pressed.connect(self.truncateLogFile)

    def project_loaded(self, project):
        self.project = project
        
    def refreshLog(self):
        syncClientLogRelativePath = 'SyncClient/logs/Log.current.log'
        projectDir = os.path.dirname(self.project.folder)        
        roamDir = os.path.dirname(projectDir)       
        LOG_FILENAME = os.path.join(roamDir, syncClientLogRelativePath)

        wholeFileAsHtml = ''
        with open(LOG_FILENAME, 'r') as logFile:
            for line in logFile:
                lineHtml = re.sub(r"^(.*)ERROR(.*)$", "<span style='color:red'>\g<1>ERROR\g<2></span>", line)
                lineHtml = lineHtml.replace("\n", "<br/>")
                wholeFileAsHtml = wholeFileAsHtml + lineHtml

        self.logTextBrowser.setHtml(wholeFileAsHtml)
        self.logTextBrowser.moveCursor(QTextCursor.End)
        
    def truncateLogFile(self):
        syncClientLogRelativePath = 'SyncClient/logs/Log.current.log'
        projectDir = os.path.dirname(self.project.folder)        
        roamDir = os.path.dirname(projectDir)       
        LOG_FILENAME = os.path.join(roamDir, syncClientLogRelativePath)
        file_handler = open(LOG_FILENAME, "w+")
        file_handler.truncate()
        self.refreshLog()
        
        
        
        
        




