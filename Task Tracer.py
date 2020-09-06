from PyQt5.QtWidgets import*
from PyQt5 import QtGui
from PyQt5.QtCore import *
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, qApp, QApplication
from PyQt5.QtGui import QIcon
import json
import os
import sys
from pathlib import Path
from pathlib import PurePath
import pandas as pd

btn1_txt = 'Tasks'
btn2_txt = 'Queries'
list_path = 'Empty'

global ct
ct = pd.DataFrame(columns = ['task'])

class MainWindow(QMainWindow):
    
    def __init__(self):

        super(MainWindow, self).__init__()
        global list_path
        global deleteStack
        
        #deleteStack = pd.DataFrame()#(columns = ['loc','text'])
        deleteStack = pd.DataFrame(columns = ['loc','text'])
        va = [12,14]
        #deleteStack=deleteStack.append({'loc':123,'text':'new'},ignore_index=True)
        
        self.setGeometry(300, 300, 400, 350)  # x, y, w, h
        self.setWindowTitle("Task Tracer")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep +'Drawing1.png'))
        #self.setStyleSheet("background-color: rgb(234,231,220)")

        self.undoStack = QUndoStack(self)
        #undoView = QUndoView(self.undoStack)
        
        #tasks frame Color1
        f2 = QFrame(self)
        f2.move(1,40)
        f2.resize(397,200)
        f2.setStyleSheet("background-color:rgb(255,255,255);"
                         "border-radius:5px;"
                         "border:0.5px solid rgb(1, 1, 1)")

        label = QLabel('  Tasks', self)
        label.setFont(QtGui.QFont("Open Sans Bold",12))
        label.setStyleSheet("background-color:rgb(255,255,255);"
                            "border-radius:5px;"
                            "border-right:0.5px solid rgb(0, 0, 0);"
                            "border-top:0.5px solid rgb(0, 0, 0);"
                            "border-bottom:0.5px solid rgb(0, 0, 0);"
                            "border-left:0.5px solid rgb(0, 0, 0);")
        label.resize(90,20)
        label.move(5,30)

        #color1
        self.listwidget = QListWidget(self)
        self.listwidget.move(28, 55)
        self.listwidget.resize(300,180)
        self.listwidget.setStyleSheet("background-color:rgb(255,255,255);"
                                      "border-right:0px solid rgb(0, 0, 0);"
                                      "border-top:0px solid rgb(0, 0, 0);"
                                      "border-bottom:0px solid rgb(0, 0, 0);"
                                      "border-left:0px solid rgb(0, 0, 0);")
        #####
        self.listwidget.itemChanged.connect(self.itemChanged)
        self.listwidget.currentItemChanged.connect(self.currentItemChanged)
        #self.textBeforeEdit = ""
        
        #color1
        #vals = '1)','2)','3)','4)','5)','6)','7)','8)','9)','10)'
        self.listwidget1 = QListWidget(self)
        #no = len(vals)
        #for items in vals:
            #listwidget1.addItem(items)
        #for i in range (0,no):
            #listwidget1.addItem(str(i))
        self.listwidget1.move(5, 55)
        self.listwidget1.resize(25,180)
        self.listwidget1.setStyleSheet("background-color:rgb(255,255,255);"
                                  "border-right:0px solid rgb(0, 0, 0);"
                                  "border-top:0px solid rgb(0, 0, 0);"
                                  "border-bottom:0px solid rgb(0, 0, 0);"
                                  "border-left:0px solid rgb(0, 0, 0);")

        f2 = QFrame(self)
        f2.move(1,255)
        f2.resize(397,50)
        f2.setStyleSheet("background-color:rgb(234,231,220);"
                         "border-radius:5px;"
                         "border:0.5px solid rgb(0, 0, 0)")

        label1 = QLabel(' New task', self)
        label1.setFont(QtGui.QFont("Playfair Display",12))
        label1.setStyleSheet("background-color:rgb(255,255,255);"
                             "border-radius:5px;"
                             "border:0.5px solid rgb(0, 0, 0)")
        label1.move(5,247)
        label1.resize(90,20)
        
        #---Menu---------------------------- 
        mainMenu = self.menuBar()
        mainMenu.setStyleSheet("border-radius:0px;"
                               "border:0px solid rgb(0, 0, 0)")
        mainMenu.setFont(QtGui.QFont("Montserrat",10))

        #---Menu1
        Menu1 = mainMenu.addMenu('File')
        Menu1_opt1 = QAction('Save As...', self)
        Menu1_opt1.triggered.connect(self.main_save)
        Menu1.addAction(Menu1_opt1)

        #---Menu3
        Menu3 = mainMenu.addMenu('Edit')
        Menu3_opt1 = QAction('Enable task edit', self)
        Menu3_opt1.triggered.connect(self.setflags)
        Menu3.addAction(Menu3_opt1)

        Menu3_opt2 = QAction('Undo edit', self)
        Menu3_opt2.triggered.connect(self.undoStack.undo)
        Menu3.addAction(Menu3_opt2)

        Menu3_opt3 = QAction('Undo delete', self)
        Menu3_opt3.triggered.connect(self.undo_delete)
        Menu3.addAction(Menu3_opt3)
        
        #---Menu2
        done = 0
        Menu2 = mainMenu.addMenu('Load')
        Menu2_opt1 = QAction('Load task list', self)
        Menu2_opt1.triggered.connect(self.load_file)
        Menu2.addAction(Menu2_opt1)
        
        #---Menu4
        Menu4 = mainMenu.addMenu('Help')
        Menu4_opt1 = QAction('About', self)
        #Menu4_opt1.triggered.connect(self.load_file)
        Menu4.addAction(Menu4_opt1)
        Menu4.addSeparator()
        
        #--- Push buttons
        b1=QPushButton('Move Up', self)
        b1.move(325, 100)
        b1.resize(70,25)
        b1.setStyleSheet("background-color:rgb(101, 204, 184)")
        b1.clicked.connect(self.up)

        b2=QPushButton('Move Down', self)
        b2.move(325, 130)
        b2.resize(70,25)
        b2.setStyleSheet("background-color:rgb(234,231,220)")
        b2.clicked.connect(self.down)

        b3=QPushButton('Complete', self)
        b3.move(325, 160)
        b3.resize(70,25)
        b3.setStyleSheet("background-color:rgb(233,128,116)")
        b3.clicked.connect(self.delete)
        
        b4=QPushButton(chr(8629), self)
        b4.setFont(QtGui.QFont("Open Sans Bold",18))
        b4.move(325, 272)
        b4.resize(70,25)
        b4.setStyleSheet("background-color:rgb(234,231,220)")
        b4.setToolTip('Enter')
        b4.clicked.connect(self.entry)

        self.textbox = QLineEdit(self)
        self.textbox.setStyleSheet("background-color:rgb(255, 255,225)")
        self.textbox.move(20, 272)
        self.textbox.resize(300,25)
        #self.textbox.keyPressEvent = self.keyPressEvent

        btnx = QPushButton('Completed \r\n tasks', self)
        btnx.move(325, 190)
        btnx.resize(70,25)
        btnx.clicked.connect(self.completed)
            

    def keyPressEvent(self,e):
        if e.key() == Qt.Key_Enter:
            print ('event')

    def list_no(self):
        
        self.listwidget1.clear()
        tsks = self.listwidget.count()
        
        for x in range (1,tsks+1):
            #self.listwidget1.addItem(str(x))
            self.listwidget1.insertItem(x-1,str(x))
        
    def undo_delete(self):
        global deleteStack
        global ct
        if deleteStack.empty == False:
            
            lent=(len(deleteStack))
            locat = int((deleteStack.loc[lent-1]['loc']))
            locat1 = deleteStack.loc[lent-1]['text']
     
            self.listwidget.insertItem(locat,locat1)
            deleteStack = deleteStack[:-1]
            ct = ct[:-1]
            self.list_no()
            
    def itemChanged(self, item):
        command = CommandEdit(self.listwidget, item, self.listwidget.row(item),
        self.textBeforeEdit, 
        "Rename item '{0}' to '{1}'".format(self.textBeforeEdit, item.text()))
        self.undoStack.push(command)
        
    def currentItemChanged(self, item):
        self.textBeforeEdit = item.text()
        
    def load_save(self):
        self.SW = FourthWindow()
        self.SW.show()

    def setflags (self):

        for index in range(self.listwidget.count()):
            item = self.listwidget.item(index)
            
            item.setFlags(item.flags() | Qt.ItemIsEditable)
     
    def up (self):
        currentRow = self.listwidget.currentRow()
        currentItem = self.listwidget.takeItem(currentRow)
        self.listwidget.insertItem(currentRow - 1, currentItem)
        save_list=self.save()
        return()

    def down (self):
        currentRow = self.listwidget.currentRow()
        currentItem = self.listwidget.takeItem(currentRow)
        self.listwidget.insertItem(currentRow + 1, currentItem)
        save_list=self.save()
        return()

    def delete (self):
        global deleteStack
        global ct
        
        currentRow = self.listwidget.currentRow()
        currentText = self.listwidget.currentItem().text()
        currentText = 'C' + currentText
        deleteStack = deleteStack.append({'loc':currentRow,'text':currentText},ignore_index=True)
        #self.save
        ct  = ct.append({'task':currentText},ignore_index=True) 
        currentItem = self.listwidget.takeItem(currentRow)
        self.list_no()
        #ct = 'testing'
        save_list=self.save()
    
    def entry (self):
        if self.textbox.text():
            a = self.textbox.text()
            self.listwidget.addItem(a)
            self.textbox.clear()
            
            if list_path == 'Empty':
                save_list=self.main_save()
            else:
                save_list=self.save()
                flags=self.setflags()
        self.list_no()

    def main_save(self):
        global list_path
        items = []
        my_items=[]

        for index in range(self.listwidget.count()):
            items.append(self.listwidget.item(index))
            my_items.append(self.listwidget.item(index).text())

        name,_ = QFileDialog.getSaveFileName(self, 'Save File')
        list_path = (PurePath(name))
        with open(list_path, "w") as f:
            
            f.write(json.dumps(my_items))

    def save(self):
        items = []
        my_items=[]
        
        for index in range(self.listwidget.count()):
            items.append(self.listwidget.item(index))
            my_items.append(self.listwidget.item(index).text())

        no_tasks = len(ct)
        for i in range (0, no_tasks):
            my_items.append(ct.loc[i]['task'])
            

        with open(list_path, "w") as f:
            f.write(json.dumps(my_items))
        return()


    def load_file(self):
        global list_path
        global ct
        
        fname,_ = QFileDialog.getOpenFileName(self, 'Open file')
        
        if not fname: 
            pass
        
        else:
            list_path = (PurePath(fname))
            with open(list_path) as f:
                    json_data = json.load(f)  
                    list_length = len(json_data)
                    for item in json_data:
                        firstChar = item[0]
                        if firstChar is not 'C':
                            self.listwidget.addItem(item)
                        else:
                            ct  = ct.append({'task':item},ignore_index=True)
        
        self.undoStack.clear()
        self.list_no()
        
    def completed(self):
        self.SW = ThirdWindow(ct)
        self.SW.show()
        #self.close()

class CommandEdit(QUndoCommand):
    def __init__(self, listWidget, item, row, textBeforeEdit, description):
        super(CommandEdit, self).__init__(description)
        self.listWidget = listWidget
        self.textBeforeEdit = textBeforeEdit
        self.textAfterEdit = item.text()
        self.row = row

    def redo(self):
        self.listWidget.blockSignals(True)
        self.listWidget.item(self.row).setText(self.textAfterEdit)
        self.listWidget.blockSignals(False)

    def undo(self):
        self.listWidget.blockSignals(True)
        self.listWidget.item(self.row).setText(self.textBeforeEdit)
        self.listWidget.blockSignals(False)

class ThirdWindow(QMainWindow):#(QMainWindow):#completed tasks
    def __init__(self,ct,parent = None ):

        super(ThirdWindow, self).__init__(parent)
    
        self.setGeometry(300, 300, 400, 350)  # x, y, w, h
        self.setWindowTitle("Edit")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep +'Drawing1.png'))

        self.listwidget = QListWidget(self)
        self.listwidget.move(28, 55)
        self.listwidget.resize(300,180)
        self.listwidget.setStyleSheet("background-color:rgb(255,255,255);"
                                      "border-right:0px solid rgb(0, 0, 0);"
                                      "border-top:0px solid rgb(0, 0, 0);"
                                      "border-bottom:0px solid rgb(0, 0, 0);"
                                      "border-left:0px solid rgb(0, 0, 0);")


        #self.listwidget.addItem('test item')
        no_tasks = len(ct)
        
        for i in range (0, no_tasks):
            
            #txt = (ct.loc[i]['task'])
            self.listwidget.addItem(ct.loc[i]['task'])
        
        b1=QPushButton('test', self)
        b1.move(325, 130)
        b1.resize(70,25)
        b1.clicked.connect(self.listname)

        b1=QPushButton('Back', self)
        b1.move(325, 315)
        b1.resize(70,25)
        b1.setToolTip('Back to home page')
        #b1.setIcon(
        b1.clicked.connect(self.home)
        
    def listname(self):
        global list_path
        fname,_ = QFileDialog.getOpenFileName(self, 'Open file')
        
        list_path = (PurePath(fname))

    def home(self):
        #self.pat = 'C:/Users/mchirjf3/Dropbox/Python/Task lists/thesis_list.json'
        #self.SW = MainWindow()
        #self.SW.show()
        self.close()

class FourthWindow(QMainWindow):
    def __init__(self):

        #print('here %s' %pat)
        super(FourthWindow, self).__init__()
        #self.pat= pat
        self.setGeometry(300, 300, 400, 350)  # x, y, w, h
        self.setWindowTitle("Edit")
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep +'Drawing1.png'))

        b1=QPushButton('Load', self)
        b1.move(325, 130)
        b1.resize(70,25)
        b2=QPushButton('Load', self)
        b2.move(225, 130)
        b2.resize(70,25)
        #print (btn1_txt)
        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    MW = MainWindow()
    MW.show()
    sys.exit(app.exec_())


