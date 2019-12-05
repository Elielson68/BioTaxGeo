import os
import xlrd
import xlwt
from xlutils.copy import copy
import requests
from fuzzywuzzy import fuzz

class Planilha:
    def __init__(self):
        #Essas variáveis irão ser atribuídas assim que o objeto for criado, pois dizem respeito somente ao arquivo, então já configuro eles automaticamente.
        self.diretorio = None 
        self.arquivo = None
        self.arquivo_escrita = None
        self.lista_de_planilhas = None 
        self.planilha = None
        self.planilha_formatada = None
        self.coordenadas = None
        self.tratamento_de_dados = None
        self.total_de_colunas = int
        self.total_de_linhas  = int
        self.valor_na_celula = str
        self.valores_na_coluna = []
        self.valores_na_linha = []
        self.index_planilha = 0

    def set_Diretorio(self, diretorio):
        self.diretorio = str(os.getcwd())+"/"+diretorio #O comando os.getcwd pega o diretório atual de onde o arquivo python está.

        try:
            self.arquivo = xlrd.open_workbook(self.diretorio, formatting_info=True) #Abre o arquivo com o nome enviado no parâmetro diretorio
        except:
            self.arquivo = xlrd.open_workbook(self.diretorio)  # Abre o arquivo com o nome enviado no parâmetro diretorio
        self.arquivo_escrita = copy(self.arquivo)
        self.lista_de_planilhas = self.arquivo.sheet_names() #Pega o nome das páginas do arquivo
        self.planilha = self.arquivo.sheet_by_index(0) #Pega a página inicial (começa por 0)
        self.planilha_formatada = self.arquivo_escrita.get_sheet(0)
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
            return "Linha excede valor total de linhas do arquivo."
        if(coluna > self.get_Total_de_colunas()):
            return "Coluna excede valor total de colunas do arquivo."
        if(linha <= self.get_Total_de_linhas() and coluna <= self.get_Total_de_colunas()):
            self.valor_na_celula = self.planilha.cell(linha, coluna).value
            return self.valor_na_celula

    def pegar_Valores_da_coluna(self, coluna):
        self.Resetar_valores()
        try:
            if(type(coluna)==str):
                coluna_indice = self.planilha.row_values(0).index(coluna)
                self.valores_na_coluna = self.planilha.col_values(coluna_indice,1)
                if(self.valores_na_coluna == []):
                    return "Valor não encontrado."
                else:
                    return self.valores_na_coluna
            elif(type(coluna)==int):
                self.valores_na_coluna = self.planilha.col_values(coluna,1)
                return self.valores_na_coluna
        except:
            return print("Coluna não encontrada.")

    def pegar_Valores_da_linha(self, linha):
        if(linha <= self.get_Total_de_linhas() and linha > 0):
            self.Resetar_valores()
            self.valores_na_linha = self.planilha.row_values((linha-1))
            return self.valores_na_linha
        else:
            return print("Linha excede limite de linhas do documento.")
    
    def Resetar_valores(self):
        self.valor_na_celula = str
        self.valores_na_coluna = []
        self.valores_na_linha = []

    def set_Colunas_para_verificar(self, titulos):
        for coluna in titulos:
            if titulos[coluna] != None:
                valores_em_coluna = self.pegar_Valores_da_coluna(titulos[coluna])
                self.tratamento_de_dados.set_Titulos_Originais(titulos[coluna])
                self.tratamento_de_dados.set_Colunas_para_verificar(coluna, valores_em_coluna)

    def get_Colunas_para_verificar(self):
        return self.tratamento_de_dados.get_Colunas_para_verificar()

    def AlterandoDadosPlanilha(self, dados_para_alterar):
        for valores in dados_para_alterar:
            key1 = valores
            for dado in dados_para_alterar[valores]:
                nivel = dados_para_alterar[valores][dado]["nivel"][0]
                index_coluna = self.planilha.row_values(0).index(self.tratamento_de_dados.get_Hierarquia_verificada()[key1][dado]["Titulo"])
                index_coluna_nivel = self.planilha.row_values(0).index(self.tratamento_de_dados.get_Hierarquia_verificada()[key1][nivel]["Titulo"])
                for linha in range(0, self.get_Total_de_linhas()):
                    valor1 = self.tratamento_de_dados.get_Hierarquia_verificada()[key1][dado]["Tipo"]
                    valor2 = self.pegar_Valor_na_celula(linha, index_coluna)
                    valor1_nivel = dados_para_alterar[valores][dado]["nivel"][1]
                    valor2_nivel = self.pegar_Valor_na_celula(linha, index_coluna_nivel)
                    if((valor1 == valor2) and (valor1_nivel == valor2_nivel)):
                        self.planilha_formatada.write(linha, index_coluna, dados_para_alterar[key1][dado]["sugestao"])

    def SalvarPlanilhaFormatada(self):
        return self.arquivo_escrita.save("Planilha_Formatada.xls")

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
        elif(type(coluna_lat) == dict):
            self.coluna_latitude = coluna_lat

    def set_Longitude_values(self, coluna_lng):
        self.coluna_longitude = []
        if(type(coluna_lng) == str):
            indice_coluna = self.planilha.row_values(0).index(coluna_lng)
            self.coluna_longitude = self.planilha.col_values(indice_coluna,1)
        elif(type(coluna_lng) == int):
            self.coluna_longitude = self.planilha.col_values(coluna_lng,1)
        elif(type(coluna_lng) == dict):
            self.coluna_longitude = coluna_lng
    
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

    def Converter_para_decimal(self, coordenada):
        for coord in coordenada:
            print(coord)
        return
    def Converter_para_grau(self):
        return None

    def is_Decimal(self, coordenada):
        if type(coordenada)==str:
            return False
        elif type(coordenada)==float:
            return True

    def isNumeros(self, valor):
        apenas_numeros = False
        if (valor.isdigit()):
            apenas_numeros = True
        return apenas_numeros

    def isNumeros_Letras(self, valor):
        apenas_numeros = False
        if (valor.isalnum()):
            apenas_numeros = True
        return apenas_numeros

    def isNumeros_Letras_Caracter(self, valor):
        apenas_numeros = False
        if (not (valor.isalnum())):
            apenas_numeros = True
        return apenas_numeros


class Tratamento_de_Dados:
    
    def __init__(self, plan):
        self.hierarquia_verificada = {} #NC = Nomes Científicos
        self.colunas_para_verificar = {}
        self.planilha = plan
        self.titulos_originais = []
        self.hierarquia_taxonomiaca = None

    def set_Colunas_para_verificar(self, titulo, valor):
            self.colunas_para_verificar[titulo] = valor
    def set_Titulos_Originais(self, titulo):
        self.titulos_originais.append(titulo)
    def get_Titulos_Originais(self):
        return self.titulos_originais
    def get_Colunas_para_verificar(self):
        if not self.colunas_para_verificar:
            return "Lista vazia"
        else:
            return self.colunas_para_verificar
    
    def set_Hierarquia_verificada(self, hierarquia):
        NC_value = hierarquia
        for indice in range(0, len(NC_value["especie"])):
            if(NC_value["genero"][indice] != ""):
                Scientific_Name = NC_value["genero"][indice] + " " + NC_value["especie"][indice]
                self.hierarquia_taxonomiaca = Hierarquia_Taxonomica(NC_value['reino'][indice], NC_value['filo'][indice],NC_value['classe'][indice] , NC_value['ordem'][indice], NC_value['familia'][indice], NC_value['genero'][indice], NC_value['especie'][indice], Scientific_Name)
                if Scientific_Name in self.hierarquia_verificada:
                    pass
                else:
                    #'http://api.gbif.org/v1/species/match?kingdom=''&phylum=''&order=''&family=''&genus=''&name=''Anodorhynchus hyacinthinus
                    valores = requests.get('http://api.gbif.org/v1/species/match?name='+Scientific_Name+"&rank=SPECIES&strict=true").json()
                    if(valores["matchType"] != "NONE"):
                        self.hierarquia_taxonomiaca.Definir_Corretude_Hierarquica(valores["kingdom"], valores["phylum"],valores["class"], valores["order"], valores["family"], valores["genus"], valores["species"], valores["canonicalName"])
                        self.hierarquia_taxonomiaca.Definir_Sugestao_Hierarquica(valores["kingdom"], valores["phylum"], valores["class"], valores["order"], valores["family"], valores["genus"], valores["species"], valores["canonicalName"])
                        self.hierarquia_verificada[Scientific_Name] = {
                                                                        "Reino"          : {
                                                                                                "Tipo"      : self.hierarquia_taxonomiaca.get_Reino(),
                                                                                                "Corretude" : self.hierarquia_taxonomiaca.get_Corretude_Reino(),
                                                                                                "Quantidade": NC_value['reino'].count(self.hierarquia_taxonomiaca.get_Reino()),
                                                                                                "Sugestão"  : self.hierarquia_taxonomiaca.get_Sugestao_Reino(),
                                                                                                "Titulo"    : self.get_Titulos_Originais()[0]

                                                                                           },
                                                                        "Filo"           : {
                                                                                                "Tipo"      : self.hierarquia_taxonomiaca.get_Filo(),
                                                                                                "Corretude" : self.hierarquia_taxonomiaca.get_Corretude_Filo(),
                                                                                                "Quantidade": NC_value['filo'].count(self.hierarquia_taxonomiaca.get_Filo()),
                                                                                                "Sugestão"  : self.hierarquia_taxonomiaca.get_Sugestao_Filo(),
                                                                                                "Titulo"    : self.get_Titulos_Originais()[1]
                                                                                           },
                                                                        "Classe"           : {
                                                                                                "Tipo"      : self.hierarquia_taxonomiaca.get_Classe(),
                                                                                                "Corretude" : self.hierarquia_taxonomiaca.get_Corretude_Classe(),
                                                                                                "Quantidade": NC_value['classe'].count(self.hierarquia_taxonomiaca.get_Classe()),
                                                                                                "Sugestão"  : self.hierarquia_taxonomiaca.get_Sugestao_Classe(),
                                                                                                "Titulo"    : self.get_Titulos_Originais()[2]
                                                                                           },
                                                                        "Ordem"          : {
                                                                                                "Tipo"      : self.hierarquia_taxonomiaca.get_Ordem(),
                                                                                                "Corretude" : self.hierarquia_taxonomiaca.get_Corretude_Ordem(),
                                                                                                "Quantidade": NC_value['ordem'].count(self.hierarquia_taxonomiaca.get_Ordem()),
                                                                                                "Sugestão"  : self.hierarquia_taxonomiaca.get_Sugestao_Ordem(),
                                                                                                "Titulo"    : self.get_Titulos_Originais()[3]
                                                                                           },
                                                                        "Família"        : {
                                                                                                "Tipo"      : self.hierarquia_taxonomiaca.get_Familia(),
                                                                                                "Corretude" : self.hierarquia_taxonomiaca.get_Corretude_Familia(),
                                                                                                "Quantidade": NC_value['familia'].count(self.hierarquia_taxonomiaca.get_Familia()),
                                                                                                "Sugestão"  : self.hierarquia_taxonomiaca.get_Sugestao_Familia(),
                                                                                                "Titulo"    : self.get_Titulos_Originais()[4]
                                                                                           },
                                                                        "Gênero"         : {
                                                                                                "Tipo"      : self.hierarquia_taxonomiaca.get_Genero(),
                                                                                                "Corretude" : self.hierarquia_taxonomiaca.get_Corretude_Genero(),
                                                                                                "Quantidade": NC_value['genero'].count(self.hierarquia_taxonomiaca.get_Genero()),
                                                                                                "Sugestão"  : self.hierarquia_taxonomiaca.get_Sugestao_Genero(),
                                                                                                "Titulo"    : self.get_Titulos_Originais()[5]
                                                                                           },
                                                                        "Espécie"        : {
                                                                                                "Tipo"      : self.hierarquia_taxonomiaca.get_Especie(),
                                                                                                "Corretude" : self.hierarquia_taxonomiaca.get_Corretude_Especie(),
                                                                                                "Quantidade": NC_value['especie'].count(self.hierarquia_taxonomiaca.get_Especie()),
                                                                                                "Sugestão"  : self.hierarquia_taxonomiaca.get_Sugestao_Especie(),
                                                                                                "Titulo"    : self.get_Titulos_Originais()[6]
                                                                                           },
                                                                        "Nome Científico": {
                                                                                                "Tipo"     : self.hierarquia_taxonomiaca.get_Scientific_Name(),
                                                                                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Scientific_Name(),
                                                                                                "Sugestão" : self.hierarquia_taxonomiaca.get_Sugestao_Scientific_Name(),
                                                                                                "Sinônimo" : valores["synonym"]
                                                                                           }
                                                                      }
                    else:
                        self.hierarquia_verificada[Scientific_Name] = {
                                                                        "Reino"         : {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Reino(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Reino(),
                                                                                            "Quantidade": NC_value['reino'].count(self.hierarquia_taxonomiaca.get_Reino()),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Reino(),
                                                                                            "Titulo": self.get_Titulos_Originais()[0]
                                                                                          },
                                                                        "Filo"          : {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Filo(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Filo(),
                                                                                            "Quantidade": NC_value['filo'].count(self.hierarquia_taxonomiaca.get_Filo()),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Filo(),
                                                                                            "Titulo": self.get_Titulos_Originais()[1]
                                                                                          },
                                                                        "Classe"          : {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Classe(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Classe(),
                                                                                            "Quantidade": NC_value['classe'].count(self.hierarquia_taxonomiaca.get_Classe()),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Classe(),
                                                                                            "Titulo": self.get_Titulos_Originais()[2]
                                                                                          },
                                                                        "Ordem"         : {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Ordem(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Ordem(),
                                                                                            "Quantidade": NC_value['ordem'].count(self.hierarquia_taxonomiaca.get_Ordem()),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Ordem(),
                                                                                            "Titulo": self.get_Titulos_Originais()[3]
                                                                                          },
                                                                        "Família"       : {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Familia(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Familia(),
                                                                                            "Quantidade": NC_value['familia'].count(self.hierarquia_taxonomiaca.get_Familia()),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Familia(),
                                                                                            "Titulo": self.get_Titulos_Originais()[4]
                                                                                          },
                                                                        "Gênero"        : {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Genero(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Genero(),
                                                                                            "Quantidade": NC_value['genero'].count(self.hierarquia_taxonomiaca.get_Genero()),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Genero(),
                                                                                            "Titulo": self.get_Titulos_Originais()[5]
                                                                                          },
                                                                        "Espécie"       : {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Especie(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Especie(),
                                                                                            "Quantidade": NC_value['especie'].count(self.hierarquia_taxonomiaca.get_Especie()),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Especie(),
                                                                                            "Titulo": self.get_Titulos_Originais()[6]
                                                                                           },
                                                                        "Nome Científico": {
                                                                                            "Tipo": self.hierarquia_taxonomiaca.get_Scientific_Name(),
                                                                                            "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Scientific_Name(),
                                                                                            "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Scientific_Name(),
                                                                                            "Sinônimo": ""
                                                                                           }
                                                                    }
        for nome_errado in self.hierarquia_verificada:

            if self.hierarquia_verificada[nome_errado]["Nome Científico"]["Corretude"] == "NONE":
                sugestao_request = requests.get('http://api.gbif.org/v1/species/suggest?q='+nome_errado+'&rank=SPECIES&strict=true').json()

                if not sugestao_request:
                    Media_Valores_Reino = {}
                    for nome_certo in self.hierarquia_verificada:
                        Media_Valores_Reino[nome_certo] = {}
                        for key in self.hierarquia_verificada[nome_certo]:
                            Media_Valores_Reino[nome_certo][key] = {}
                            if self.hierarquia_verificada[nome_certo][key]["Corretude"] == "EXACT":
                                certo = self.hierarquia_verificada[nome_certo][key]["Tipo"]
                                errado = self.hierarquia_verificada[nome_errado][key]["Tipo"]
                                Media_Valores_Reino[nome_certo][key][certo] = None
                                if (self.Comparar_String(certo, errado) > 60 and errado != certo):
                                    Media_Valores_Reino[nome_certo][key][certo] = self.Comparar_String(nome_certo, nome_errado)
                                    self.hierarquia_verificada[nome_errado][key]["Sugestão"].append(Media_Valores_Reino[nome_certo][key])
                                    self.hierarquia_verificada[nome_errado]["Espécie"]["Sugestão"].append(self.hierarquia_verificada[nome_certo]["Espécie"]["Tipo"])
                                if (certo == errado):
                                    self.hierarquia_verificada[nome_errado][key]["Corretude"] = self.hierarquia_verificada[nome_certo][key]["Corretude"]
                else:
                    self.hierarquia_taxonomiaca = Hierarquia_Taxonomica(
                                                                        self.hierarquia_verificada[nome_errado]["Reino"]["Tipo"],
                                                                        self.hierarquia_verificada[nome_errado]["Filo"]["Tipo"],
                                                                        self.hierarquia_verificada[nome_errado]["Classe"]["Tipo"],
                                                                        self.hierarquia_verificada[nome_errado]["Ordem"]["Tipo"],
                                                                        self.hierarquia_verificada[nome_errado]["Família"]["Tipo"],
                                                                        self.hierarquia_verificada[nome_errado]["Gênero"]["Tipo"],
                                                                        self.hierarquia_verificada[nome_errado]["Nome Científico"]["Tipo"],
                                                                        self.hierarquia_verificada[nome_errado]["Nome Científico"]["Tipo"]
                                                                        )
                    for key in self.hierarquia_verificada[nome_errado]:
                        self.hierarquia_verificada[nome_errado][key]["Sugestão"] = []
                    for indice in range(0,len(sugestao_request)):
                        try:
                            self.hierarquia_taxonomiaca.Definir_Corretude_Hierarquica(sugestao_request[indice]["kingdom"], sugestao_request[indice]["phylum"], sugestao_request[indice]["class"], sugestao_request[indice]["order"], sugestao_request[indice]["family"], sugestao_request[indice]["genus"], sugestao_request[indice]["species"], sugestao_request[indice]["canonicalName"])
                            self.hierarquia_taxonomiaca.Definir_Sugestao_Hierarquica(sugestao_request[indice]["kingdom"], sugestao_request[indice]["phylum"], sugestao_request[indice]["class"], sugestao_request[indice]["order"], sugestao_request[indice]["family"], sugestao_request[indice]["genus"], sugestao_request[indice]["species"], sugestao_request[indice]["canonicalName"])
                        except:
                            print('http://api.gbif.org/v1/species/suggest?q=' + nome_errado + '&rank=SPECIES&strict=true')
                        self.hierarquia_verificada[nome_errado]["Reino"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Reino()) if self.hierarquia_taxonomiaca.get_Sugestao_Reino() not in self.hierarquia_verificada[nome_errado]["Reino"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Filo"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Filo()) if self.hierarquia_taxonomiaca.get_Sugestao_Filo() not in self.hierarquia_verificada[nome_errado]["Filo"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Classe"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Classe()) if self.hierarquia_taxonomiaca.get_Sugestao_Classe() not in self.hierarquia_verificada[nome_errado]["Classe"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Ordem"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Ordem()) if self.hierarquia_taxonomiaca.get_Sugestao_Ordem() not in self.hierarquia_verificada[nome_errado]["Ordem"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Família"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Familia()) if self.hierarquia_taxonomiaca.get_Sugestao_Familia() not in self.hierarquia_verificada[nome_errado]["Família"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Gênero"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Genero()) if self.hierarquia_taxonomiaca.get_Sugestao_Genero() not in self.hierarquia_verificada[nome_errado]["Gênero"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Espécie"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Especie()) if self.hierarquia_taxonomiaca.get_Sugestao_Especie() not in self.hierarquia_verificada[nome_errado]["Espécie"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Nome Científico"]["Sugestão"].append(self.hierarquia_taxonomiaca.get_Sugestao_Scientific_Name()) if self.hierarquia_taxonomiaca.get_Sugestao_Scientific_Name() not in self.hierarquia_verificada[nome_errado]["Nome Científico"]["Sugestão"] else None

                        self.hierarquia_verificada[nome_errado]["Reino"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Reino()
                        self.hierarquia_verificada[nome_errado]["Filo"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Filo()
                        self.hierarquia_verificada[nome_errado]["Classe"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Classe()
                        self.hierarquia_verificada[nome_errado]["Ordem"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Ordem()
                        self.hierarquia_verificada[nome_errado]["Família"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Familia()
                        self.hierarquia_verificada[nome_errado]["Gênero"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Genero()
                        self.hierarquia_verificada[nome_errado]["Espécie"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Especie()
                        self.hierarquia_verificada[nome_errado]["Nome Científico"]["Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Scientific_Name()

    def get_Hierarquia_verificada(self):
        return self.hierarquia_verificada

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

class Hierarquia_Taxonomica:

    def __init__(self, r, fi, c, o, fa, g, e, SN):
        self.Scientific_Name = SN
        self.reino = r
        self.filo = fi
        self.classe = c
        self.ordem = o
        self.familia = fa
        self.genero = g
        self.especie = e
        self.corretude_reino = "NONE"
        self.corretude_filo = "NONE"
        self.corretude_classe = "NONE"
        self.corretude_ordem = "NONE"
        self.corretude_familia = "NONE"
        self.corretude_genero = "NONE"
        self.corretude_especie = "NONE"
        self.corretude_scientific_name = "NONE"
        self.sugestao_reino = []
        self.sugestao_filo = []
        self.sugestao_classe = []
        self.sugestao_ordem = []
        self.sugestao_familia = []
        self.sugestao_genero = []
        self.sugestao_especie = []
        self.sugestao_scientific_name = []

    def set_Hierarquia(self, r, fi, c, o, fa, g, e, SN):
        self.Scientific_Name = SN
        self.reino = r
        self.filo = fi
        self.classe = c
        self.ordem = o
        self.familia = fa
        self.genero = g
        self.especie = e
    def get_Hierarquia(self):
        return self.reino, self.filo, self.ordem, self.familia, self.genero, self.especie, self.Scientific_Name

    def Definir_Corretude_Hierarquica(self, reino, filo, classe, ordem, familia, genero, especie, Scientific_Name):
        self.corretude_reino = "EXACT" if (self.reino == reino) else "FUZZY"
        self.corretude_filo = "EXACT" if self.filo == filo else "FUZZY"
        self.corretude_classe = "EXACT" if self.classe == classe else "FUZZY"
        self.corretude_ordem = "EXACT" if self.ordem == ordem else "FUZZY"
        self.corretude_familia = "EXACT" if self.familia == familia else "FUZZY"
        self.corretude_genero = "EXACT" if self.genero == genero else "FUZZY"
        if (self.especie == especie.replace(genero + " ","")) or (self.especie == especie.replace(self.genero + " ","")):
            self.corretude_especie = "EXACT"
        else:
            self.corretude_especie = "FUZZY"
        self.corretude_scientific_name = "EXACT" if self.Scientific_Name == Scientific_Name else "FUZZY"

    def Definir_Sugestao_Hierarquica(self, reino, filo, classe, ordem, familia, genero, especie, Scientific_Name):
        self.sugestao_reino = None if self.corretude_reino == "EXACT" else reino
        self.sugestao_filo = None if self.corretude_filo == "EXACT" else  filo
        self.sugestao_classe = None if self.corretude_classe == "EXACT" else  classe
        self.sugestao_ordem = None if self.corretude_ordem == "EXACT" else ordem
        self.sugestao_familia = None if self.corretude_familia == "EXACT" else familia
        self.sugestao_genero = None if self.corretude_genero == "EXACT" else genero
        if self.corretude_especie == "EXACT":
            self.sugestao_especie = None
        else:
            self.sugestao_especie = especie.replace(genero + " ", "") if genero in especie else especie.replace(self.genero + " ", "")
        self.sugestao_scientific_name = None if self.corretude_scientific_name == "EXACT" else Scientific_Name

    def get_Reino(self):
        return self.reino
    def get_Filo(self):
        return self.filo
    def get_Classe(self):
        return self.classe
    def get_Ordem(self):
        return self.ordem
    def get_Familia(self):
        return self.familia
    def get_Genero(self):
        return self.genero
    def get_Especie(self):
        return self.especie
    def get_Scientific_Name(self):
        return self.Scientific_Name

    def get_Corretude_Reino(self):
        return self.corretude_reino
    def get_Corretude_Filo(self):
        return self.corretude_filo
    def get_Corretude_Classe(self):
        return self.corretude_classe
    def get_Corretude_Ordem(self):
        return self.corretude_ordem
    def get_Corretude_Familia(self):
        return self.corretude_familia
    def get_Corretude_Genero(self):
        return self.corretude_genero
    def get_Corretude_Especie(self):
        return self.corretude_especie
    def get_Corretude_Scientific_Name(self):
        return self.corretude_scientific_name

    def get_Sugestao_Reino(self):
        return self.sugestao_reino
    def get_Sugestao_Filo(self):
        return self.sugestao_filo
    def get_Sugestao_Classe(self):
        return self.sugestao_classe
    def get_Sugestao_Ordem(self):
        return self.sugestao_ordem
    def get_Sugestao_Familia(self):
        return self.sugestao_familia
    def get_Sugestao_Genero(self):
        return self.sugestao_genero
    def get_Sugestao_Especie(self):
        return self.sugestao_especie
    def get_Sugestao_Scientific_Name(self):
        return self.sugestao_scientific_name