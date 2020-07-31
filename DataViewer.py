from tkinter import *
from pandastable import Table, TableModel
import pandas as pd
import xlsxwriter
import os.path
#from elytica_dss import *
import elytica_dss as edss
from configparser import ConfigParser
import io
import base64
from os import listdir
from os.path import isfile, join



class DataViewer(Frame):
  def __init__(self, parent=None, filename='Diet.xlsx', modelDir="models/"):
    self.parent = parent
    self.__filename = filename
    self.__modelDirectory = modelDir
    Frame.__init__(self)
    self.main = self.master
    self.main.title('Diet Editor')
    if not os.path.isfile(filename):
      self.createInitialExcelFile(filename)

    df = pd.read_excel(filename, sheet_name="data")
    self.table = Table(self, dataframe=df)
    self.table.show()

    buttonsFrame = Frame(self)
    buttonsFrame.grid(column=0, columnspan=2)
    self.__saveButton = Button(buttonsFrame, text="Save",\
      command=self.saveData).pack(fill=X, side=LEFT)
    self.__runButton = Button(buttonsFrame, text="Run",\
      command=self.runModel).pack(fill=X, side=LEFT)
    self.__closeButton = Button(buttonsFrame, text="Close",\
      command=self.destroy).pack(fill=X, side=LEFT)


    return

  def createInitialExcelFile(self, filename):
    workbook = xlsxwriter.Workbook(filename)
    worksheet = workbook.add_worksheet('data')
    worksheet.write('A1', 'Name')
    worksheet.write('B1', 'Price')
    worksheet.write('C1', 'Energy (kcal)')
    worksheet.write('D1', 'Protien (g)')
    worksheet.write('E1', 'Sodium (mg)')
    worksheet.write('F1', 'Carbohydrates (g)')
    worksheet.write('G1', 'Saturated Fat (g)')
    worksheet.write('H1', 'Fibre (g)')
    worksheet.write('I1', 'Vitamin A (ug)')
    worksheet.write('J1', 'Vitamin C (mg)')
    worksheet.write('K1', 'Calcium (mg)')
    worksheet.write('L1', 'Iron (mg)')
    worksheet.write('A2', 'Cake')
    worksheet.write('B2', '25')
    worksheet.write('C2', '59')
    worksheet.write('D2', '1')
    worksheet.write('E2', '110')
    worksheet.write('F2', '9.4')
    worksheet.write('G2', '2.2')
    worksheet.write('H2', '0.3')
    worksheet.write('I2', '0')
    worksheet.write('J2', '0')
    worksheet.write('K2', '20')
    worksheet.write('L2', '0.2')
    workbook.close()

  def char_range(self, c1, c2):
    for c in range(ord(c1), ord(c2) + 1):
        yield chr(c)

  def saveData(self):
    indices = len(self.table.model.df.index)
    setData=[]
    for v in self.char_range('A', 'L'):
      setData.append(v + '2:' + v + str(indices + 1))
    modelSets=pd.DataFrame(setData)
    writer = pd.ExcelWriter(self.__filename, engine = 'xlsxwriter')
    self.table.model.df.to_excel(writer, sheet_name='data', index=False)
    modelSets.to_excel(writer, sheet_name = 'metadata', index=False, header=False)
    saved=writer.save()

  def runModel(self):
    firstRun=True
    config = ConfigParser()
    config.read('config.ini')
    dss = edss.Service(config['elytica']['apiKey'])
    dss.login()

    if len(list(filter(lambda x : x.name == "DIET",\
      dss.getProjects()))) > 0:
      dss.selectProjectByName("DIET")
      dss.selectJobByName("Basic Job")
      firstRun=False
    else:
      app = dss.selectApplicationByName("MIP Interpreter with Python")
      dss.createProject("DIET", "The diet problem.", app) 
      dss.createJob("Basic Job", 100)

    md = self.__modelDirectory
    modelFiles = [f for f in listdir(md) if isfile(join(md, f))]

    firstRun = True 
    if firstRun:
      for f in modelFiles:
        modelFile = open(md + f,  "rb", buffering=0)
        uf = dss.uploadFileContents(f, modelFile)[0];
        dss.assignFile(uf, 2)

    inputFiles = dss.getInputFiles()
    excelData = open(self.__filename,  "rb", buffering=0)
    dataFile = dss.uploadFileContents(self.__filename, excelData)[0]
    print(dataFile)
   # dss.assignFile(dataFile, 3)
    


        
        
