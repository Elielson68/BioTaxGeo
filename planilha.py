import os
import openpyxl
import xlrd
import xlwt
import pygbif
import requests
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
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
        #Utilizando outra api de leitura de excel pois a antiga fazia somente leitura e não escrita. Começar a trocar todas as coisas da antiga api para a nova.
        self.OpenPyXl_arquivo = None
        self.OpenPyXl_total_planilhas = None
        self.OpenPyXl_planilha = None
        self.OpenPyXl_total_colunas = None
        self.OpenPyXl_total_linhas = None
    
    def set_Diretorio(self, diretorio):
        self.diretorio = str(os.getcwd())+"/"+diretorio #O comando os.getcwd pega o diretório atual de onde o arquivo python está.
        self.arquivo = xlrd.open_workbook(self.diretorio) #Abre o arquivo com o nome enviado no parâmetro diretorio
        self.lista_de_planilhas = self.arquivo.sheet_names() #Pega o nome das páginas do arquivo
        self.planilha = self.arquivo.sheet_by_index(0) #Pega a página inicial (começa por 0)
        #Aqui já vão ser atribuídas no decorrer do processamento.
        self.total_de_colunas = self.planilha.ncols
        self.total_de_linhas  = self.planilha.nrows
        self.coordenadas = Coordenadas(self.planilha)
        

        self.OpenPyXl_arquivo = openpyxl.load_workbook(diretorio)
        self.OpenPyXl_total_planilhas = self.OpenPyXl_arquivo.get_sheet_names()
        self.OpenPyXl_planilha = self.OpenPyXl_arquivo.get_sheet_by(self.OpenPyXl_total_planilhas[0])
        self.OpenPyXl_total_colunas = self.OpenPyXl_planilha.get_highest_column()
        self.OpenPyXl_total_linhas = self.OpenPyXl_planilha.get_highest_row()

        self.tratamento_de_dados = Tratamento_de_Dados(self.planilha, self.OpenPyXl_planilha)
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

    def Get_Planilha (self):
        return print(self.lista_de_planilhas[self.index_planilha])

    def get_Lista_de_planilhas (self):
        self.lista_de_planilhas = self.arquivo.sheet_names()
        return print(self.lista_de_planilhas)

    def get_Cabecario_Planilha(self):
        return self.planilha.row_values(0)

    def get_Total_de_colunas(self):
        return self.total_de_colunas

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

    def get_Latitude(self):
        return self.coordenadas.get_Latitude_values()

    def get_Longitude(self):
        return self.coordenadas.get_Longitude_values()


    def set_Latitude(self, coluna_lat):
        self.coordenadas.set_Latitude_values(coluna_lat)


    def set_Longitude(self, coluna_lng):
        self.coordenadas.set_Longitude_values(coluna_lng)
    

    def set_ColG_ColNC(self, coluna_G, coluna_NC):
        self.tratamento_de_dados.set_Colunas_para_verificar(coluna_G, coluna_NC)
    
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
    
    def __init__(self, plan, plan2):
        self.ocorrencias_NC = {} #NC = Nomes Científicos
        self.colunas_para_verificar = []
        self.planilha = plan
        self.OpenPyXl_planilha_write = plan2

    def set_Colunas_para_verificar(self, coluna_G, coluna_NC):
        self.colunas_para_verificar = []
        colunas_genus_scientific_name = [[],[]] 
        if(type(coluna_NC) == str and type(coluna_G) == str):
            indice_coluna_G = self.planilha.row_values(0).index(coluna_G)
            indice_coluna_NC = self.planilha.row_values(0).index(coluna_NC)
            colunas_genus_scientific_name[0] = self.planilha.col_values(indice_coluna_G,1)
            colunas_genus_scientific_name[1] = self.planilha.col_values(indice_coluna_NC,1)
            self.colunas_para_verificar = colunas_genus_scientific_name
        elif(type(coluna_NC) == int):
            colunas_genus_scientific_name[0] = self.planilha.col_values(coluna_G,1)
            colunas_genus_scientific_name[1] = self.planilha.col_values(coluna_NC,1)
            self.colunas_para_verificar = colunas_genus_scientific_name
    
    def get_Colunas_para_verificar(self):
        if not self.colunas_para_verificar:
            return "Lista vazia"
        else:
            return self.colunas_para_verificar

    def get_NC_Tratado(self):
        NC_value = self.get_Colunas_para_verificar()
        for nome in range (0,len(NC_value[0])):
            if (NC_value[0][nome]+" "+NC_value[1][nome]) in self.ocorrencias_NC:
                pass
            else:
                Scientific_Name = NC_value[0][nome]+" "+NC_value[1][nome]
                
                #'http://api.gbif.org/v1/species/match?kingdom=''&phylum=''&order=''&family=''&genus=''&name=''Anodorhynchus hyacinthinus
                valores = requests.get('http://api.gbif.org/v1/species/match?name='+Scientific_Name).json()
                if(valores["matchType"] != "NONE"):
                    if(valores["matchType"] == "FUZZY"):
                        self.ocorrencias_NC[Scientific_Name] = {"quantidade": NC_value[0].count(NC_value[0][nome]), "precisão": valores["confidence"], "corretude": valores["matchType"], "Sugestão de Nome": valores["canonicalName"]}
                    else:
                        self.ocorrencias_NC[Scientific_Name] = {"quantidade": NC_value[0].count(NC_value[0][nome]), "precisão": valores["confidence"], "corretude": valores["matchType"], "Sugestão de Nome": None}
                else:
                    self.ocorrencias_NC[Scientific_Name] = {"quantidade": NC_value[0].count(NC_value[0][nome]), "precisão": 0, "corretude": valores["matchType"], "Sugestão de Nome": None}
        for nome_errado in self.ocorrencias_NC:
            Media_Valores = {}
            if self.ocorrencias_NC[nome_errado]["corretude"] == "NONE":
                sugestao_request = requests.get('http://api.gbif.org/v1/species/suggest?q='+nome_errado).json()
                sugestoes = []

                if not sugestao_request:
                    for nome_certo in self.ocorrencias_NC:
                        if self.ocorrencias_NC[nome_certo]["corretude"] == "EXACT":
                            if(self.Comparar_String(nome_certo,nome_errado)>60 and nome_errado != nome_certo):
                                Media_Valores[nome_certo] =  self.Comparar_String(nome_certo,nome_errado)
                    self.ocorrencias_NC[nome_errado]["Sugestão de Nome"] = Media_Valores
                else:
                    self.ocorrencias_NC[nome_errado]["corretude"] = "FUZZY"
                    for indice in range(0,len(sugestao_request)):
                        if "species" in sugestao_request[indice]:
                            if sugestao_request[indice]["species"] not in sugestoes:
                                sugestoes.append(sugestao_request[indice]["species"])
                    if len(sugestoes) > 1:
                        self.ocorrencias_NC[nome_errado]["Sugestão de Nome"] = sugestoes 
                    else:
                        self.ocorrencias_NC[nome_errado]["Sugestão de Nome"] = sugestoes[0]
        return self.ocorrencias_NC


    def Ocorrencia_de_String_na_Coluna(self, coluna):
        tratar_coluna = self.planilha.col_values(coluna,1)
        coluna_tratada = {}
        for nome in tratar_coluna:
            if nome in coluna_tratada:
                pass
            else:
                coluna_tratada[nome] = {"quantidade":tratar_coluna.count(nome)}
        return coluna_tratada

    def Comparar_String(self, String1, String2):
        Ratio_valor = fuzz.ratio(String1.lower(), String2.lower())
        Partial_Ratio_valor = fuzz.partial_ratio(String1.lower(), String2.lower())
        Token_Sort_Ratio_valor = fuzz.token_sort_ratio(String1, String2)
        Token_Set_Ratio_valor = fuzz.token_set_ratio(String1, String2)
        Media = (Ratio_valor+Partial_Ratio_valor+Token_Sort_Ratio_valor+Token_Set_Ratio_valor)/4

        return Media
    
    def Verificar_similaridade_de_string(self, coluna):
        if type(coluna) == int:
            tratar_coluna = self.Ocorrencia_de_String_na_Coluna(coluna)
        elif type(coluna) == str:
            indice_coluna = self.planilha.row_values(0).index(coluna)
            tratar_coluna = self.Ocorrencia_de_String_na_Coluna(indice_coluna)
        for nome1 in tratar_coluna:
            sugestoes = []
            for nome2 in tratar_coluna:
                if self.Comparar_String(nome1, nome2)>60 and nome1 != nome2:
                    sugestoes.append({"Similaridade de": self.Comparar_String(nome1, nome2), "Sugestão de nome": nome2})
            tratar_coluna[nome1]["Sugestões"] = sugestoes
        return tratar_coluna
    def AlterandoDadosPlanilha(self, coluna=None,dado=None):
        print(self.planilha.formula.cellname(0,0))