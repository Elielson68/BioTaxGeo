import os
import xlrd
import pygbif
import requests

class Planilha:
    def __init__(self):
        #Essas variáveis irão ser atribuídas assim que o objeto for criado, pois dizem respeito somente ao arquivo, então já configuro eles automaticamente.
        self.diretorio = None 
        self.arquivo = None 
        self.lista_de_planilhas = None 
        self.planilha = None 
        self.coordenadas = None
        self.tratamento_de_dados = None
        self.total_de_colunas = int
        self.total_de_linhas  = int
        self.valor_na_celula = str
        self.valores_na_coluna = []
        self.valores_na_linha = []
        self.index_planilha = 0
    
    @Diretorio.setter
    def set_Diretorio(self, diretorio):
        self.diretorio = str(os.getcwd())+"/"+diretorio #O comando os.getcwd pega o diretório atual de onde o arquivo python está.
        self.arquivo = xlrd.open_workbook(self.diretorio) #Abre o arquivo com o nome enviado no parâmetro diretorio
        self.lista_de_planilhas = self.arquivo.sheet_names() #Pega o nome das páginas do arquivo
        self.planilha = self.arquivo.sheet_by_index(0) #Pega a página inicial (começa por 0)
        #Aqui já vão ser atribuídas no decorrer do processamento.
        self.total_de_colunas = self.planilha.ncols
        self.total_de_linhas  = self.planilha.nrows
        self.coordenadas = Coordenadas(self.planilha)
        self.tratamento_de_dados = Tratamento_de_Dados(self.planilha)
    
    def Escolher_planilha (self):
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

    @property
    def get_Planilha (self):
        return print(self.lista_de_planilhas[self.index_planilha])

    @property
    def get_Lista_de_planilhas (self):
        self.lista_de_planilhas = self.arquivo.sheet_names()
        return print(self.lista_de_planilhas)

    @property
    def get_Cabecario_Planilha(self):
        return self.planilha.row_values(0)

    @property
    def get_Total_de_colunas(self):
        return self.total_de_colunas

    @property
    def get_Total_de_linhas(self):
        return self.total_de_linhas

    def pegar_Valor_na_celula(self, linha, coluna):
        if(linha > self.get_Total_de_linhas()):
            return print("Linha excede valor total de linhas do arquivo.")
        if(coluna > self.get_Total_de_colunas()):
            return print("Coluna excede valor total de colunas do arquivo.")
        if(linha <= self.get_Total_de_linhas() and coluna <= self.get_Total_de_colunas()):
            self.valor_na_celula = self.planilha.cell((linha-1), (coluna-1)).value
            return print(self.valor_na_celula)

    def pegar_Valores_da_coluna(self, coluna):
        self.Resetar_valores()
        try:
            if(type(coluna)==str):
                coluna_indice = self.planilha.row_values(0).index(coluna)
                self.valores_na_coluna = self.planilha.col_values(coluna_indice,1)
                if(self.valores_na_coluna == []):
                    return print ("Valor não encontrado.")
                else:
                    return print(self.valores_na_coluna)
            elif(type(coluna)==int):
                self.valores_na_coluna = self.planilha.col_values(coluna,1)
                return print(self.valores_na_coluna)
        except:
            return print("Coluna não encontrada.")

    def pegar_Valores_da_linha(self, linha):
        if(linha <= self.get_Total_de_linhas() and linha > 0):
            self.Resetar_valores()
            self.valores_na_linha = self.planilha.row_values((linha-1))
            return print(self.valores_na_linha)
        else:
            return print("Linha excede limite de linhas do documento.")
    
    def Resetar_valores(self):
        self.valor_na_celula = str
        self.valores_na_coluna = []
        self.valores_na_linha = []

    @property
    def get_Latitude(self):
        return self.coordenadas.get_Latitude_values()

    @property
    def get_Longitude(self):
        return self.coordenadas.get_Longitude_values()

    @latitude.setter
    def set_Latitude(self, coluna_lat):
        self.coordenadas.set_Latitude_values(coluna_lat)

    @longitude.setter
    def set_Longitude(self, coluna_lng):
        self.coordenadas.set_Longitude_values(coluna_lng)
    
    @col_NC.setter
    def set_Col_NC(self, coluna_NC):
        self.tratamento_de_dados.set_Col_NC(coluna_NC)
    
    @property
    def get_NC_Tratado(self):
        return self.tratamento_de_dados.get_NC_Tratado()

class Coordenadas:
    def __init__(self, Plan):
        self.coluna_latitude = None
        self.coluna_longitude = None
        self.planilha = Plan
    def set_Latitude_values(self, coluna_lat):
        self.coluna_latitude = []
        if(type(coluna_lat) == str):
            indice_coluna = self.planilha.row_values(0).index(coluna_lat)
            self.coluna_latitude = self.planilha.col_values(indice_coluna,1)
        elif(type(coluna_lat) == int):
            self.coluna_latitude = self.planilha.col_values(coluna_lat,1)

    def set_Longitude_values(self, coluna_lng):
        self.coluna_longitude = []
        if(type(coluna_lng) == str):
            indice_coluna = self.planilha.row_values(0).index(coluna_lng)
            self.coluna_longitude = self.planilha.col_values(indice_coluna,1)
        elif(type(coluna_lng) == int):
            self.coluna_longitude = self.planilha.col_values(coluna_lng,1)
    
    def get_Latitude_values(self):
        if(self.coluna_latitude == []):
            return "Coluna vazia."
        else:    
            return self.coluna_latitude

    def get_Longitude_values(self):
        if(self.coluna_longitude == []):
            return "Coluna vazia."
        else:
            return self.coluna_longitude

class Tratamento_de_Dados:
    def __init__(self, plan):
        self.ocorrencias_NC = {} #NC = Nomes Científicos
        self.coluna_nomes_cientificos = []
        self.planilha = plan
    def set_Col_NC(self, coluna_NC):
        self.ocorrencias_NC = {} #NC = Nomes Científicos
        self.coluna_nomes_cientificos = []
        if(type(coluna_NC) == str):
            indice_coluna = self.planilha.row_values(0).index(coluna_NC)
            self.coluna_nomes_cientificos = self.planilha.col_values(indice_coluna,1)
        elif(type(coluna_NC) == int):
            self.coluna_nomes_cientificos = self.planilha.col_values(coluna_NC,1)
    
    def get_Nomes_Cient_values(self):
        if not self.coluna_nomes_cientificos:
            return "Lista vazia"
        else:
            return self.coluna_nomes_cientificos

    def get_NC_Tratado(self):
        NC_value = self.get_Nomes_Cient_values()
        for nome in NC_value:
            if nome in self.ocorrencias_NC:
                pass
            else:
                valores = requests.get('http://api.gbif.org/v1/species/match?name='+nome).json()
                if(valores["matchType"] != "NONE"):
                    if(valores["matchType"] == "FUZZY"):
                        self.ocorrencias_NC[nome] = {"quantidade": NC_value.count(nome), "precisão": valores["confidence"], "corretude": valores["matchType"], "sugerirCorrecao": valores["canonicalName"]}
                    else:
                        self.ocorrencias_NC[nome] = {"quantidade": NC_value.count(nome), "precisão": valores["confidence"], "corretude": valores["matchType"], "sugerirCorrecao": None}
                else:
                        self.ocorrencias_NC[nome] = {"quantidade": NC_value.count(nome), "precisão": 0, "corretude": valores["matchType"], "sugerirCorrecao": "Não encontrado"}
        return self.ocorrencias_NC