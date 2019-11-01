import os
import xlrd
import pygbif
class Planilha:
    def __init__(self, diretorio):
        #Essas variáveis irão ser atribuídas assim que o objeto for criado, pois dizem respeito somente ao arquivo, então já configuro eles automaticamente.
        self.diretorio = str(os.getcwd())+"/"+diretorio #O comando os.getcwd pega o diretório atual de onde o arquivo python está.
        self.arquivo = xlrd.open_workbook(self.diretorio) #Abre o arquivo com o nome enviado no parâmetro diretorio
        self.lista_de_planilhas = self.arquivo.sheet_names() #Pega o nome das páginas do arquivo
        self.planilha = self.arquivo.sheet_by_index(0) #Pega a página inicial (começa por 0)
        #Aqui já vão ser atribuídas no decorrer do processamento.
        self.total_de_colunas = self.planilha.ncols
        self.total_de_linhas  = self.planilha.nrows

        self.valor_na_celula = str

        self.valores_na_coluna = []
        self.valores_na_linha = []
        self.coluna_latitude = []
        self.coluna_longitude = []

        self.index_planilha = 0

    def set_Planilha (self):
        self.index_planilha = input("Digite o nome ou o index da planilha: ")
        try:
            self.index_planilha = int(self.index_planilha)
            if(self.index_planilha >= len(self.lista_de_planilhas)):
                return print("Index de planilha excede ao limite de planilhas do arquivo.")
            else:
                self.planilha = self.arquivo.sheet_loaded(self.index_planilha)
        except:
            self.index_planilha = self.lista_de_planilhas.index(self.index_planilha)
            self.planilha = self.arquivo.sheet_loaded(self.index_planilha)

    def get_Planilha (self):
        return print(self.lista_de_planilhas[self.index_planilha])

    def get_Lista_de_planilhas (self):
        self.arquivo.sheet_loaded
        self.lista_de_planilhas = self.arquivo.sheet_names()
        return print(self.lista_de_planilhas)

    def get_Total_de_colunas(self):
        return self.total_de_colunas

    def get_Total_de_linhas(self):
        return self.total_de_linhas

    def get_Valor_na_celula(self, linha, coluna):
        if(linha > self.get_Total_de_linhas()):
            return print("Linha excede valor total de linhas do arquivo.")
        if(coluna > self.get_Total_de_colunas()):
            return print("Coluna excede valor total de colunas do arquivo.")
        if(linha <= self.get_Total_de_linhas() and coluna <= self.get_Total_de_colunas()):
            self.valor_na_celula = self.planilha.cell((linha-1), (coluna-1)).value
            return print(self.valor_na_celula)

    def get_Valores_na_coluna(self, coluna):
        self.Resetar_valores()
        try:
            if(type(coluna)==str):
                colunha_length = self.get_Total_de_colunas()
                linha_length   = self.get_Total_de_linhas()

                for coluna_indice in range(0, colunha_length):
                    for linha_indice in range(0, linha_length):
                        if(self.planilha.cell(0, coluna_indice).value == coluna):
                            self.valores_na_coluna.append(self.planilha.cell(linha_indice, coluna_indice).value)

                if(self.valores_na_coluna == []):
                    return print ("Valor não encontrado.")
                else:
                    return print(self.valores_na_coluna)

            elif(type(coluna)==int):
                for linha in range (0, self.total_de_linhas):
                    self.valores_na_coluna.append(self.planilha.cell(linha, (coluna-1)).value)
                return print(self.valores_na_coluna)
        except:
            return print("Valor informado não é válido.")
    
    def get_Valores_na_linha(self, linha):
        if(linha <= self.get_Total_de_linhas()):
            self.Resetar_valores()
            colunha_length = self.get_Total_de_colunas()
            for coluna in range (0, colunha_length):
                self.valores_na_linha.append(self.planilha.cell((linha-1), coluna).value)
            return print(self.valores_na_linha)
        else:
            return print("Linha excede limite de linhas do documento.")
    
    def Resetar_valores(self):
        self.valor_na_celula = str
        self.valores_na_coluna = []
        self.valores_na_linha = []
        self.coluna_latitude = []
        self.coluna_longitude = []