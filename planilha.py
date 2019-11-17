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
        self.arquivo = xlrd.open_workbook(self.diretorio, formatting_info=True) #Abre o arquivo com o nome enviado no parâmetro diretorio
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

    def get_NC_Tratado(self):
        return self.tratamento_de_dados.get_NC_Tratado()

    def set_Colunas_para_verificar(self, titulos):
        for coluna in titulos:
            valores_em_coluna = self.pegar_Valores_da_coluna(titulos[coluna])
            self.tratamento_de_dados.set_Colunas_para_verificar(coluna, valores_em_coluna)
    def get_Colunas_para_verificar(self):
        return self.tratamento_de_dados.get_Colunas_para_verificar()
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
        self.colunas_para_verificar = {}
        self.planilha = plan

    def set_Colunas_para_verificar(self, titulo, valor):
            self.colunas_para_verificar[titulo] = valor
    
    def get_Colunas_para_verificar(self):
        if not self.colunas_para_verificar:
            return "Lista vazia"
        else:
            return self.colunas_para_verificar

    def get_NC_Tratado(self):
        NC_value = self.get_Colunas_para_verificar()
        for indice in range(0, len(NC_value["especie"])):
            Scientific_Name = NC_value["genero"][indice] + " " + NC_value["especie"][indice]
            reino = NC_value['reino'][indice]
            filo = NC_value['filo'][indice]
            ordem = NC_value['ordem'][indice]
            familia = NC_value['familia'][indice]
            genero = NC_value['genero'][indice]
            especie = NC_value['especie'][indice]
            corretude_reino = None
            corretude_filo = None
            corretude_ordem = None
            corretude_familia = None
            corretude_genero = None
            corretude_especie = None
            corretude_scientific_name = None
            sugestao_reino = None
            sugestao_filo = None
            sugestao_ordem = None
            sugestao_familia = None
            sugestao_genero = None
            sugestao_especie = None
            sugestao_scientific_name = None
            if Scientific_Name in self.ocorrencias_NC:
                pass
            else:
                #'http://api.gbif.org/v1/species/match?kingdom=''&phylum=''&order=''&family=''&genus=''&name=''Anodorhynchus hyacinthinus
                valores = requests.get('http://api.gbif.org/v1/species/match?name='+Scientific_Name+"&rank=SPECIES&strict=true").json()
                if(valores["matchType"] != "NONE"):
                    corretude_reino = "EXACT" if reino == valores["kingdom"] else corretude_reino = "FUZZY"
                    corretude_filo = "EXACT" if filo == valores["phylum"] else corretude_filo = "FUZZY"
                    corretude_ordem = "EXACT" if ordem == valores["order"] else corretude_ordem = "FUZZY"
                    corretude_familia = "EXACT" if familia == valores["family"] else corretude_familia = "FUZZY"
                    corretude_genero = "EXACT" if genero == valores["genus"] else corretude_genero = "FUZZY"
                    corretude_especie = "EXACT" if especie == valores["species"].replace(valores["genus"]+" ","") else corretude_especie = "FUZZY"
                    corretude_scientific_name = "EXACT" if Scientific_Name == valores["especies"] else corretude_scientific_name = "FUZZY"
                    sugestao_reino = None if corretude_reino == "EXACT" else sugestao_reino = valores["kingdom"]
                    sugestao_filo = None if corretude_filo == "EXACT" else sugestao_filo = valores["phylum"]
                    sugestao_ordem = None if corretude_ordem == "EXACT" else sugestao_ordem = valores["order"]
                    sugestao_familia = None if corretude_familia == "EXACT" else sugestao_familia = valores["family"]
                    sugestao_genero = None if corretude_genero == "EXACT" else sugestao_genero = valores["genus"]
                    sugestao_especie = None if corretude_especie == "EXACT" else sugestao_especie = valores["species"].replace(valores["genus"]+" ","")
                    sugestao_scientific_name = None if corretude_scientific_name == "EXACT" else sugestao_scientific_name = valores["species"]
                    self.ocorrencias_NC[Scientific_Name] = {"Reino": {"Tipo": reino, "Corretude": corretude_reino, "Quantidade": NC_value['reino'].count(reino), "Sugestão": sugestao_reino}, "Filo": {"Tipo": filo, "Corretude": corretude_filo, "Quantidade": NC_value['filo'].count(filo), "Sugestão": sugestao_filo}, "Ordem": {"Tipo": ordem, "Corretude": corretude_ordem, "Quantidade": NC_value['ordem'].count(ordem), "Sugestão": sugestao_ordem}, "Família": {"Tipo": familia, "Corretude": corretude_familia, "Quantidade": NC_value['familia'].count(familia), "Sugestão": sugestao_familia}, "Gênero": {"Tipo": genero, "Corretude": corretude_genero, "Quantidade": NC_value['genero'].count(genero), "Sugestão": sugestao_genero}, "Espécie": {"Tipo": especie, "Corretude": corretude_especie, "Quantidade": NC_value['especie'].count(especie), "Sugestão": sugestao_especie}, "Nome Científico": {"Corretude": corretude_scientific_name, "Sugestão": sugestao_scientific_name}}
                else:
                    corretude_reino = "NONE"
                    corretude_filo = "NONE"
                    corretude_ordem = "NONE"
                    corretude_familia = "NONE"
                    corretude_genero = "NONE"
                    corretude_especie = "NONE"
                    corretude_scientific_name = "NONE"
                    self.ocorrencias_NC[Scientific_Name] = {"Reino": {"Tipo": reino, "Corretude": corretude_reino, "Quantidade": NC_value['reino'].count(reino), "Sugestão": None}, "Filo": {"Tipo": filo, "Corretude": corretude_filo, "Quantidade": NC_value['filo'].count(filo), "Sugestão": None}, "Ordem": {"Tipo": ordem, "Corretude": corretude_ordem, "Quantidade": NC_value['ordem'].count(ordem), "Sugestão": None}, "Família": {"Tipo": familia, "Corretude": corretude_familia, "Quantidade": NC_value['familia'].count(familia), "Sugestão": None}, "Gênero": {"Tipo": genero, "Corretude": corretude_genero, "Quantidade": NC_value['genero'].count(genero), "Sugestão": None}, "Espécie": {"Tipo": especie, "Corretude": corretude_especie, "Quantidade": NC_value['especie'].count(especie), "Sugestão": None}, "Nome Científico": {"Corretude": corretude_scientific_name, "Sugestão": None}}

        for nome_errado in self.ocorrencias_NC:
            Media_Valores_Reino = {}
            if self.ocorrencias_NC[nome_errado]["Nome Científico"]["Corretude"] == "NONE":
                sugestao_request = requests.get('http://api.gbif.org/v1/species/suggest?q='+nome_errado+'&rank=SPECIES&strict=true').json()
                sugestoes = []
                if not sugestao_request:
                    for nome_certo in self.ocorrencias_NC:
                        if self.ocorrencias_NC[nome_certo]["Reino"]["Corretude"] == "EXACT":
                            reino_certo = self.ocorrencias_NC[nome_certo]["Reino"]["Tipo"]
                            reino_errado = self.ocorrencias_NC[nome_errado]["Reino"]["Tipo"]
                            if(self.Comparar_String(reino_certo, reino_errado)>60 and reino_errado != reino_certo):
                                Media_Valores_Reino[reino_certo] =  self.Comparar_String(nome_certo,nome_errado)
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
    def AlterandoDadosPlanilha(self, coluna, dado_errado, dado_certo):
        index_coluna = self.planilha.row_values(0).index(coluna)
        for linha in self.planilha.get_Total_de_linhas():
            if(dado_errado == self.planilha.pegar_Valor_na_celula(linha, index_coluna)):
                self.planilha_formatada.write(linha,index_coluna, dado_certo)
    def SalvarPlanilhaFormatada(self):
        return self.arquivo_escrita.save("Planilha_Formatada.xls")