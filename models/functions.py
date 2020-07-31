import xlrd
import re
import json
import os

def get_col_idx(xls_ref):
  col_ref = re.sub(r'\d+', '', xls_ref)
  col = ord(col_ref.lower()) - 96
  return col

def get_row_idx(xls_ref):
  row_ref = re.sub(r'\D+', '', xls_ref)
  return int(row_ref)


def read_set(fname, sname, ref):
  iset = list()
  wb = xlrd.open_workbook(fname)
  ws = wb.sheet_by_name(sname)
  start_ref = ref.partition(':')[0]
  end_ref = ref.partition(':')[2]
  if get_col_idx(start_ref) != get_col_idx(end_ref) :
    print("Error - reading set across multiple columns")
    return "[]"
  col = get_col_idx(start_ref) - 1
  start_row = get_row_idx(start_ref) - 1
  end_row = get_row_idx(end_ref)
  max_v = ws.cell_value(start_row, col)
  s = '[' + str(int(max_v)) + ','
  for r in range(start_row+1, end_row):
    v = ws.cell_value(r, col)
    if v > max_v:
      max_v = v
      s = s + str(int(ws.cell_value(r, col))) + ','
  s = s[:-1]
  s = s + ']'
  return s, int(max_v)

def read_1d_array(fname, sname, start_ref, dim_size):
  wb = xlrd.open_workbook(fname)
  ws = wb.sheet_by_name(sname)
  col = get_col_idx(start_ref) - 1
  start_row = get_row_idx(start_ref) - 1
  s = '['
  for r in range(start_row, start_row+dim_size):
    s = s + str(ws.cell_value(r, col)) + ','
  s = s[:-1]
  s = s + ']'
  return s

def read_2d_array(fname, sname, start_ref, dim1_size, dim2_size):
  wb = xlrd.open_workbook(fname)
  ws = wb.sheet_by_name(sname)
  col = get_col_idx(start_ref) - 1
  row = get_row_idx(start_ref) - 1
  s = '['
  for i in range(0, dim1_size):
    s = s + '['
    for j in range(0, dim2_size):
      s = s + str(ws.cell_value(row, col)) + ','
      row += 1
    s = s[:-1]
    s = s + ']'+','
  s = s[:-1]
  s = s + ']'
  return s


def read_3d_array(fname, sname, start_ref, dim1_size, dim2_size, dim3_size):
  wb = xlrd.open_workbook(fname)
  ws = wb.sheet_by_name(sname)
  col = get_col_idx(start_ref) - 1
  row = get_row_idx(start_ref) - 1
  s = '['
  for i in range(0, dim1_size):
    s = s + '['
    for j in range(0, dim2_size):
      s = s + '['
      for k in range(0, dim3_size):
        s = s + str(ws.cell_value(row, col)) + ','
        row += 1
      s = s[:-1]
      s = s + ']' + ','
    s = s[:-1]
    s = s + ']'+','
  s = s[:-1]
  s = s + ']'
  return s



def save_results(results):
  if not os.path.exists("output"):
    os.mkdir("output")
  f = open("output/results", "w")
  f.write(json.dumps({"excel": results}))
  f.close()


#set = read_col("data.xlsx", "nodes", "A2", 5)
#set, setMax = read_set("data.xlsx", "activities", "A2:A7")
#set = read_1d_array("data.xlsx", "1d_array", "B2", 6)
#set = read_3d_array("data.xlsx", "3d_array", "D2", 2, 6, 3)
#print(set)
#print(setMax)


