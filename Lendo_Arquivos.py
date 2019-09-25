import os
import xlrd

path = str(os.getcwd())+"/testar.xls"
wb = xlrd.open_workbook(path)
Latitude = []
Longitude = []
sheets = wb.sheet_names()
sheet = wb.sheet_by_name(sheets[0])
linhas = sheet.nrows
colunas = sheet.ncols
coluna_lng = ""
coluna_lat = ""
armazenar = False

for coluna in range(colunas):
    for linha in range(linhas):

        if(armazenar and coluna_lat == coluna):
            Latitude.append(sheet.cell(linha, coluna).value)
            sheet.cell(linha, coluna).value = "Abacate"
            wb.save('testar.xls')
        if(sheet.cell(linha,coluna).value == "Latitude"):
            armazenar = True
            coluna_lat = coluna

        if(armazenar and coluna_lng == coluna):
            Longitude.append(sheet.cell(linha, coluna).value)
        if(sheet.cell(linha,coluna).value == "Longitude"):
            armazenar = True
            coluna_lng = coluna
print(Latitude)
print(Longitude)

#print(sheet.cell(linhas-1,colunas-3).value)
