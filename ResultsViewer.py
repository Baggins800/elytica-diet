from tkinter import *
import elytica_dss as edss
from configparser import ConfigParser
import json


class ResultsViewer:
  def __init__(self):
    self.__resultsWindow = Tk()
    config = ConfigParser()
    config.read('config.ini')
    dss = edss.Service(config['elytica']['apiKey'])
    self.__resultsText = Text(self.__resultsWindow)
    self.__quitButton = Button(self.__resultsWindow, text="Close",\
      command=self.__resultsWindow.destroy)
    dss.login()
    if len(list(filter(lambda x : x.name == "DIET",\
      dss.getProjects()))) > 0:
      dss.selectProjectByName("DIET")
      dss.selectJobByName("Basic Job")
    result = None
    for f in dss.getOutputFiles():
      if f.name == "results":
        result = f
    foods = json.loads(dss.downloadFile(result).decode('utf-8'))
    for f in foods:
      if (foods[f] > 0):
        name = f[:10] + (f[10:] and '..')
        self.__resultsText.insert(END, name + '\t\t' + \
          "{:.2f}".format(foods[f]) + "\n")
    self.__resultsText.pack(fill=X) 
    self.__quitButton.pack(fill=X)

      
  def show(self):
    self.__resultsWindow.update()
    self.__resultsWindow.deiconify()
    self.__resultsWindow.mainloop()

  def hide(self):
    self.__resultsWindow.withdraw()
