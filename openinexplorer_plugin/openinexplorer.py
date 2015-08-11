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
import subprocess

from PyQt4.QtGui import QDesktopServices
from PyQt4.QtCore import QUrl


def resolve(name):
    f = os.path.join(os.path.dirname(__file__), name)
    return f

widget, base = loadUiType(resolve("dialogOkCancel.ui"))

class Example(QWidget):    
    def __init__(self):
        super(Example, self).__init__()        
        self.initUI()
        
    def initUI(self):
        self.btn = QPushButton('Dialog', self)
        self.btn.move(20, 20)
        self.btn.clicked.connect(self.showDialog)
        
        self.le = QLineEdit(self)
        self.le.move(130, 22)
        
        self.setGeometry(300, 300, 290, 150)
        self.setWindowTitle('Input dialog')
        self.show()
        
    def showDialog(self):        
        text, ok = QInputDialog.getText(self, 'Input Dialog', 
            'Enter your name:')        
        if ok:
            self.le.setText(str(text))
            
            
class SearchPlugin(widget, base, Page):
    title = "Open In Explorer"
    icon = resolve("search.svg")

    def __init__(self, api, parent=None):
        super(SearchPlugin, self).__init__(parent)
        self.setupUi(self)
        self.api = api
        self.project = None
        self.dbpath = None
        self.OpenInExplorerButton.pressed.connect(self.OpenInExplorer)        

    def project_loaded(self, project):
        self.project = project
        
    def OpenInExplorer(self):        
        #QDesktopServices.openUrl(QUrl.fromLocalFile(self.project.basefolder))
        #ex = Example() 
        #dlg = QDialog()
        #dlg.setTooltip (self.project.basefolder)
        #dlg.exec_()             
        explorerCommand = "explorer \"" + os.path.normpath(self.project.folder) + "\""        
        self.debugLabel.setText(explorerCommand)
        subprocess.call(explorerCommand, shell=True)
        
        




