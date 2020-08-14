from tkinter import *
from tkinter.ttk import *
from pandastable import Table, TableModel
import pandas as pd
import xlsxwriter
import os.path
import elytica_dss as edss
from configparser import ConfigParser
import io
import base64
import threading
from os import listdir
from os.path import isfile, join

class Sheets:
  USER=1
  FOOD=2
class DataViewer(Frame):
  def __init__(self, parent=None, filename='Diet.xlsx', modelDir="model/"):
    self.parent = parent
    self.__filename = filename
    self.__modelDirectory = modelDir
    Frame.__init__(self)
    self.main = self.master
    self.main.title('Diet Editor')
    if not os.path.isfile(filename):
      self.createInitialExcelFile(filename)

    self.df = pd.read_excel(filename, sheet_name="data")
    self.uf = pd.read_excel(filename, sheet_name="bounds")
    self.table = Table(self, dataframe=self.df)
    self.table.show()

    buttonsFrame = Frame(self)
    buttonsFrame.grid(column=0, columnspan=2)
    self.__progress=Progressbar(buttonsFrame, orient=HORIZONTAL, length=100,\
      mode='determinate')
    self.__saveButton = Button(buttonsFrame, text="Save",\
      command=self.saveData)
    self.__runButton = Button(buttonsFrame, text="Run",\
      command=self.runModel)
    self.__userButton = Button(buttonsFrame, text="User",\
      command=self.userData)
    self.__foodButton = Button(buttonsFrame, text="Food",\
      command=self.foodData)
    self.__closeButton = Button(buttonsFrame, text="Close",\
      command=self.destroy)

    self.__progress.pack(side=BOTTOM, fill=X)
    self.__saveButton.pack(fill=X, side=LEFT)
    self.__runButton.pack(fill=X, side=LEFT)
    self.__userButton.pack(fill=X, side=LEFT)
    self.__foodButton.pack(fill=X, side=LEFT)
    self.__closeButton.pack(fill=X, side=LEFT)
    self.__foodButton['state'] = DISABLED
    self.__selectedState = Sheets.FOOD

    return

  def createInitialExcelFile(self, filename):
    workbook = xlsxwriter.Workbook(filename)
    datasheet = workbook.add_worksheet('data')
    boundssheet = workbook.add_worksheet('bounds')
    # food entry
    datasheet.write('A1', 'Name')
    datasheet.write('B1', 'Price')
    datasheet.write('C1', 'Energy (kcal)')
    datasheet.write('D1', 'Protien (g)')
    datasheet.write('E1', 'Sodium (mg)')
    datasheet.write('F1', 'Carbohydrates (g)')
    datasheet.write('G1', 'Saturated Fat (g)')
    datasheet.write('H1', 'Fibre (g)')
    datasheet.write('I1', 'Vitamin A (ug)')
    datasheet.write('J1', 'Vitamin C (mg)')
    datasheet.write('K1', 'Calcium (mg)')
    datasheet.write('L1', 'Iron (mg)')
    datasheet.write('A2', 'Cake')
    datasheet.write('B2', '25')
    datasheet.write('C2', '59')
    datasheet.write('D2', '1')
    datasheet.write('E2', '110')
    datasheet.write('F2', '9.4')
    datasheet.write('G2', '2.2')
    datasheet.write('H2', '0.3')
    datasheet.write('I2', '0')
    datasheet.write('J2', '0')
    datasheet.write('K2', '20')
    datasheet.write('L2', '0.2')

    # user entry
    boundssheet.write('B1', 'Energy (kcal)')
    boundssheet.write('C1', 'Protien (g)')
    boundssheet.write('D1', 'Sodium (mg)')
    boundssheet.write('E1', 'Carbohydrates (g)')
    boundssheet.write('F1', 'Saturated Fat (g)')
    boundssheet.write('G1', 'Fibre (g)')
    boundssheet.write('H1', 'Vitamin A (ug)')
    boundssheet.write('I1', 'Vitamin C (mg)')
    boundssheet.write('J1', 'Calcium (mg)')
    boundssheet.write('K1', 'Iron (mg)')
    boundssheet.write('A2', 'LowerBound')
    boundssheet.write('B2', '1')
    boundssheet.write('C2', '1')
    boundssheet.write('D2', '1')
    boundssheet.write('E2', '1')
    boundssheet.write('F2', '1')
    boundssheet.write('G2', '1')
    boundssheet.write('H2', '1')
    boundssheet.write('I2', '1')
    boundssheet.write('J2', '1')
    boundssheet.write('K2', '1')
    boundssheet.write('A3', 'UpperBound')
    boundssheet.write('B3', '1')
    boundssheet.write('C3', '1')
    boundssheet.write('D3', '1')
    boundssheet.write('E3', '1')
    boundssheet.write('F3', '1')
    boundssheet.write('G3', '1')
    boundssheet.write('H3', '1')
    boundssheet.write('I3', '1')
    boundssheet.write('J3', '1')
    boundssheet.write('K3', '1')
    workbook.close()

  def foodData(self):
    self.__foodButton['state'] = DISABLED
    self.__userButton['state'] = NORMAL
    self.__selectedState = Sheets.FOOD
    self.uf = self.table.model.df
    self.table.updateModel(TableModel(self.df))
    self.table.redraw()

  def userData(self):
    self.__foodButton['state'] = NORMAL
    self.__userButton['state'] = DISABLED
    self.__selectedState = Sheets.USER
    self.df = self.table.model.df
    self.table.updateModel(TableModel(self.uf))
    self.table.redraw()

  def charRange(self, c1, c2):
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)

  def saveData(self):
    if self.__selectedState == Sheets.FOOD:
      self.df = self.table.model.df

    if self.__selectedState == Sheets.USER:
      self.uf = self.table.model.df
    indices = len(self.df.index)
    setData=[]
    for v in self.charRange('A', 'L'):
      setData.append(v + '2:' + v + str(indices + 1))
    modelSets=pd.DataFrame(setData)
    writer = pd.ExcelWriter(self.__filename, engine='xlsxwriter')
    self.df.to_excel(writer, sheet_name='data', index=False)
    self.uf.to_excel(writer, sheet_name='bounds', index=False)
    modelSets.to_excel(writer, sheet_name='metadata', index=False, header=False)
    saved = writer.save()

  def runModel(self):
    firstRun = True
    config = ConfigParser()
    config.read('config.ini')
    dss = edss.Service(config['elytica']['apiKey'])
    dss.login()

    self.__progress['value']=20
    self.update_idletasks()

    if len(list(filter(lambda x : x.name == "DIET",\
      dss.getProjects()))) > 0:
      dss.selectProjectByName("DIET")
      dss.selectJobByName("Basic Job")
      firstRun=False
    else:
      app = dss.selectApplicationByName("MIP Interpreter with Python")
      dss.createProject("DIET", "The diet problem.", app)
      dss.createJob("Basic Job", 100)

    self.__progress['value']=40
    self.update_idletasks()

    md = self.__modelDirectory
    libDir = self.__modelDirectory + '/libraries/'
    modelFiles = [f for f in listdir(md) if isfile(join(md, f))]
    libraries = [f for f in listdir(libDir) if isfile(join(libDir, f))]

    firstRun = True
    if firstRun:
      for f in modelFiles:
        modelFile = open(md + f,  "rb", buffering=0)
        uf = dss.uploadFileContents(f, modelFile);
        dss.assignFile(uf, 1)
      arg = 2
      for f in libraries:
        libraryFile = open(libDir + f,  "rb", buffering=0)
        uf = dss.uploadFileContents(f, libraryFile);
        dss.assignFile(uf, arg)
        arg += 1

    self.__progress['value']=60
    self.update_idletasks()

    countInputFiles = len(dss.getInputFiles())
    excelData = open(self.__filename,  "rb", buffering=0)
    dataFile = dss.uploadFileContents(self.__filename, excelData)
    dss.assignFile(dataFile, countInputFiles)

    self.__progress['value']=80
    self.update_idletasks()

    dss.queueJob()

    self.__progress['value']=100
    self.update_idletasks()
