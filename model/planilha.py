import os
import xlrd
from xlutils.copy import copy
from model.coordinate import Coordenadas
from model.data_treatment import Tratamento_de_Dados

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
        self.diretorio = str(os.getcwd())+"/files/"+diretorio #O comando os.getcwd pega o diretório atual de onde o arquivo python está.

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
    
    def get_Diretorio(self):
        return self.diretorio

    def Escolher_planilha (self):
        self.index_planilha = input("Digite o nome ou o index da planilha: ")
        try:
            self.index_planilha = int(self.index_planilha)
            if(self.index_planilha >= len(self.lista_de_planilhas)):
                return "Index de planilha excede ao limite de planilhas do arquivo."
            else:
                self.planilha = self.arquivo.sheet_loaded(self.index_planilha)
        except:
            self.index_planilha = self.lista_de_planilhas.index(self.index_planilha)
            self.planilha = self.arquivo.sheet_loaded(self.index_planilha)

    def Get_Planilha (self):
        return self.lista_de_planilhas[self.index_planilha]

    def get_Lista_de_planilhas (self):
        self.lista_de_planilhas = self.arquivo.sheet_names()
        return self.lista_de_planilhas

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
            return "Coluna não encontrada."

    def pegar_Valores_da_linha(self, linha):
        if(linha <= self.get_Total_de_linhas() and linha > 0):
            self.Resetar_valores()
            self.valores_na_linha = self.planilha.row_values((linha-1))
            return self.valores_na_linha
        else:
            return "Linha excede limite de linhas do documento."
    
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
        return self.arquivo_escrita.save("files/Planilha_Formatada.xls")

