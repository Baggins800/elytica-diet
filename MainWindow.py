from tkinter import *
from tkinter.ttk import Frame, Label, Entry
from ApiConfig import *
from DataViewer import * 
from ResultsViewer import * 

class MainWindow(Frame):
  def __init__(self):
    super().__init__()
    self.master.title("Main Menu")
    self.__installButton = Button(self.master, text="Set API key",\
      command=self.installApiKey)
    self.__enterDataButton = Button(self.master, text="View Data",\
      command=self.viewData)
    self.__viewResults = Button(self.master, text="View Results",\
      command=self.viewResults)

    self.__displayFrame = None
    self.__installButton.pack(fill=X)
    self.__enterDataButton.pack(fill=X)
    self.__viewResults.pack(fill=X)


  def installApiKey(self):
    ApiConfig().show()

  def viewData(self):
    if self.__displayFrame is not None:
      self.__displayFrame.destroy()
    self.__displayFrame = DataViewer() 
    self.__displayFrame.pack(fill=X)


  def viewResults(self):
    ResultsViewer().show()
    
