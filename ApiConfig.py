from tkinter import *
from configparser import ConfigParser
class ApiConfig:
  def __init__(self):
    self.__setupApiWindow = Tk()
    self.__config = ConfigParser()
    self.__config.read('config.ini')
    self.__setupApiWindow.title("Personal Access Token")
    self.__setupApiWindow.attributes('-type', 'dialog')
    self.__heading = Label(self.__setupApiWindow, text='Personal Access Token')
    self.__apiKeyText = Text(self.__setupApiWindow) 
    if 'elytica' in self.__config.sections():
      if 'apikey' in self.__config['elytica']:
        self.__apiKeyText.insert(END,\
          self.__config['elytica']['apikey'])
    self.__installButton = Button(self.__setupApiWindow, text="Install",\
      command=self.saveConfiguration)
    self.__heading.pack(fill=X) 
    self.__apiKeyText.pack(fill=BOTH) 
    self.__installButton.pack(fill=X)

  def saveConfiguration(self):
    apiKey=self.__apiKeyText.get("1.0", END)
    if not self.__config.has_section('elytica'):
      self.__config.add_section('elytica')
    self.__config.set('elytica', 'apiKey', apiKey)
    with open('config.ini', 'w') as f:
      self.__config.write(f)
    self.__setupApiWindow.quit()
    self.__setupApiWindow.destroy()

  def show(self):
    self.__setupApiWindow.update()
    self.__setupApiWindow.deiconify()
    self.__setupApiWindow.mainloop()

  def hide(self):
    self.__setupApiWindow.withdraw()
