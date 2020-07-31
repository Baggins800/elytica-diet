from tkinter import *

class DataEntry:
  def __init__(self):
    self.__dataWindow = Tk()

  def show(self):
    self.__dataWindow.update()
    self.__dataWindow.deiconify()
    self.__dataWindow.mainloop()

