import sys

from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from images_path import create_annotation
from images_copy import create_dataset2, create_annotation2
from images_iterator import Iterator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.initIterator()
        self.createAction()
        self.createMenuBar()
        
    def initUI(self):
                
        self.resize(1200,900)
        self.center()
        self.setWindowTitle('brown_bear and polar_bear')
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        brown_bear_button=QPushButton('Next brown pear',self)
        polar_bear_button=QPushButton('Next polar bear',self)

        
        self.lbl = QLabel(self)
        
        hbox = QHBoxLayout()
        hbox.addSpacing(1)
        hbox.addWidget(brown_bear_button)
        hbox.addWidget(polar_bear_button)

        vbox = QVBoxLayout()
        vbox.addSpacing(1)
        vbox.addWidget(self.lbl)
        vbox.addLayout(hbox)

        self.centralWidget.setLayout(vbox)
        brown_bear_button.clicked.connect(self.next_brown_bear)
        polar_bear_button.clicked.connect(self.next_polar_bear)

        self.folderpath = ' '
        
        self.show()
     
    def initIterator(self):
        self.brown_bear=Iterator('brown_bear','dataset')
        self.polar_bear=Iterator('polar_bear','dataset')
        
    def next_brown_bear(self):
        lbl_size = self.lbl.size()
        next_image = next(self.brown_bear)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:        
            self.initIterator()
            self.next_brown_bear()
                 
    def next_polar_bear(self):
        lbl_size = self.lbl.size()
        next_image = next(self.polar_bear)
        if next_image != None:
            img = QPixmap(next_image).scaled(
                lbl_size, aspectRatioMode=Qt.KeepAspectRatio)
            self.lbl.setPixmap(img)
            self.lbl.setAlignment(Qt.AlignCenter)
        else:        
            self.initIterator()
            self.next_polar_bear()
        
        
    def center(self):
        qr=self.frameGeometry()
        cp=QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        
    
    def createMenuBar(self):
        
        menuBar = self.menuBar()
        
        self.fileMenu = menuBar.addMenu('&File')
        self.fileMenu.addAction(self.exitAction)
        self.fileMenu.addAction(self.changeAction)
        
        self.dataMenu=menuBar.addMenu('&Data')
        self.dataMenu.addAction(self.createData2Action)
        
    def createToolBar(self):
        fileToolBar=self.addToolBar('File')
        fileToolBar.addAction(self.exitAction)
                
    def createAction(self):
        self.exitAction = QAction('&Exit')
        self.exitAction.triggered.connect(qApp.quit)

        self.changeAction = QAction('&Change dataset')
        self.changeAction.triggered.connect(self.changeDataset)

        self.createData2Action = QAction('&Create dataset2')
        self.createData2Action.triggered.connect(self.createDataset2)

        
            
    def createDataset2(self):
        create_dataset2()
        self.dataMenu.addAction(self.createData3Action)
        compleate = QMessageBox()
        compleate.setWindowTitle("Message")
        compleate.setText("Task completed")
        compleate.exec()
        
        
        
    def changeDataset(self):
        reply= QMessageBox.question(self, 'Message', f'Are you sure you want to change current dataset?\nCurrent dataset: {str(self.folderpath)}',
                                     QMessageBox.Yes | QMessageBox.No) 
        if reply == QMessageBox.Yes:
            self.folderpath = QFileDialog.getExistingDirectory(
                self, 'Select Folder')
        else:
            pass  
        
        
    def closeEvent(self,event):
        reply=QMessageBox.question(self,'Message', "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No)
        
        if reply==QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())