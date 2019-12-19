import requests
from model.taxon_validation import Hierarquia_Taxonomica
from fuzzywuzzy import fuzz
class Tratamento_de_Dados:

    def __init__(self, plan):
        self.hierarquia_verificada = {}  # NC = Nomes Científicos
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
            if (NC_value["genero"][indice] != ""):
                Scientific_Name = NC_value["genero"][indice] + " " + NC_value["especie"][indice]
                self.hierarquia_taxonomiaca = Hierarquia_Taxonomica(NC_value['reino'][indice], NC_value['filo'][indice],
                                                                    NC_value['classe'][indice],
                                                                    NC_value['ordem'][indice],
                                                                    NC_value['familia'][indice],
                                                                    NC_value['genero'][indice],
                                                                    NC_value['especie'][indice], Scientific_Name)
                if Scientific_Name in self.hierarquia_verificada:
                    pass
                else:
                    # 'http://api.gbif.org/v1/species/match?kingdom=''&phylum=''&order=''&family=''&genus=''&name=''Anodorhynchus hyacinthinus
                    valores = requests.get(
                        'http://api.gbif.org/v1/species/match?name=' + Scientific_Name + "&rank=SPECIES&strict=true").json()
                    if (valores["matchType"] != "NONE"):
                        self.hierarquia_taxonomiaca.Definir_Corretude_Hierarquica(valores["kingdom"], valores["phylum"],
                                                                                  valores["class"], valores["order"],
                                                                                  valores["family"], valores["genus"],
                                                                                  valores["species"],
                                                                                  valores["canonicalName"])
                        self.hierarquia_taxonomiaca.Definir_Sugestao_Hierarquica(valores["kingdom"], valores["phylum"],
                                                                                 valores["class"], valores["order"],
                                                                                 valores["family"], valores["genus"],
                                                                                 valores["species"],
                                                                                 valores["canonicalName"])
                        self.hierarquia_verificada[Scientific_Name] = {
                            "Reino": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Reino(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Reino(),
                                "Quantidade": NC_value['reino'].count(self.hierarquia_taxonomiaca.get_Reino()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Reino(),
                                "Titulo": self.get_Titulos_Originais()[0]

                            },
                            "Filo": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Filo(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Filo(),
                                "Quantidade": NC_value['filo'].count(self.hierarquia_taxonomiaca.get_Filo()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Filo(),
                                "Titulo": self.get_Titulos_Originais()[1]
                            },
                            "Classe": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Classe(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Classe(),
                                "Quantidade": NC_value['classe'].count(self.hierarquia_taxonomiaca.get_Classe()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Classe(),
                                "Titulo": self.get_Titulos_Originais()[2]
                            },
                            "Ordem": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Ordem(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Ordem(),
                                "Quantidade": NC_value['ordem'].count(self.hierarquia_taxonomiaca.get_Ordem()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Ordem(),
                                "Titulo": self.get_Titulos_Originais()[3]
                            },
                            "Família": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Familia(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Familia(),
                                "Quantidade": NC_value['familia'].count(self.hierarquia_taxonomiaca.get_Familia()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Familia(),
                                "Titulo": self.get_Titulos_Originais()[4]
                            },
                            "Gênero": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Genero(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Genero(),
                                "Quantidade": NC_value['genero'].count(self.hierarquia_taxonomiaca.get_Genero()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Genero(),
                                "Titulo": self.get_Titulos_Originais()[5]
                            },
                            "Espécie": {
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
                                "Sinônimo": valores["synonym"],
                                "Fonte": "GBIF"
                            }
                        }
                    else:
                        self.hierarquia_verificada[Scientific_Name] = {
                            "Reino": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Reino(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Reino(),
                                "Quantidade": NC_value['reino'].count(self.hierarquia_taxonomiaca.get_Reino()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Reino(),
                                "Titulo": self.get_Titulos_Originais()[0]
                            },
                            "Filo": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Filo(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Filo(),
                                "Quantidade": NC_value['filo'].count(self.hierarquia_taxonomiaca.get_Filo()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Filo(),
                                "Titulo": self.get_Titulos_Originais()[1]
                            },
                            "Classe": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Classe(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Classe(),
                                "Quantidade": NC_value['classe'].count(self.hierarquia_taxonomiaca.get_Classe()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Classe(),
                                "Titulo": self.get_Titulos_Originais()[2]
                            },
                            "Ordem": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Ordem(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Ordem(),
                                "Quantidade": NC_value['ordem'].count(self.hierarquia_taxonomiaca.get_Ordem()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Ordem(),
                                "Titulo": self.get_Titulos_Originais()[3]
                            },
                            "Família": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Familia(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Familia(),
                                "Quantidade": NC_value['familia'].count(self.hierarquia_taxonomiaca.get_Familia()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Familia(),
                                "Titulo": self.get_Titulos_Originais()[4]
                            },
                            "Gênero": {
                                "Tipo": self.hierarquia_taxonomiaca.get_Genero(),
                                "Corretude": self.hierarquia_taxonomiaca.get_Corretude_Genero(),
                                "Quantidade": NC_value['genero'].count(self.hierarquia_taxonomiaca.get_Genero()),
                                "Sugestão": self.hierarquia_taxonomiaca.get_Sugestao_Genero(),
                                "Titulo": self.get_Titulos_Originais()[5]
                            },
                            "Espécie": {
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
                                "Sinônimo": "",
                                "Fonte:": "Planilha"
                            }
                        }
        for nome_errado in self.hierarquia_verificada:

            if self.hierarquia_verificada[nome_errado]["Nome Científico"]["Corretude"] == "NONE":
                sugestao_request = requests.get(
                    'http://api.gbif.org/v1/species/suggest?q=' + nome_errado + '&rank=SPECIES&strict=true').json()

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
                                    Media_Valores_Reino[nome_certo][key][certo] = self.Comparar_String(nome_certo,
                                                                                                       nome_errado)
                                    self.hierarquia_verificada[nome_errado][key]["Sugestão"].append(
                                        Media_Valores_Reino[nome_certo][key])
                                    self.hierarquia_verificada[nome_errado]["Espécie"]["Sugestão"].append(
                                        self.hierarquia_verificada[nome_certo]["Espécie"]["Tipo"])
                                    self.hierarquia_verificada[nome_errado]["Nome Científico"]["Fonte"] = "Planilha"
                                if (certo == errado):
                                    self.hierarquia_verificada[nome_errado][key]["Corretude"] = \
                                    self.hierarquia_verificada[nome_certo][key]["Corretude"]
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
                    for indice in range(0, len(sugestao_request)):
                        try:
                            self.hierarquia_taxonomiaca.Definir_Corretude_Hierarquica(
                                sugestao_request[indice]["kingdom"], sugestao_request[indice]["phylum"],
                                sugestao_request[indice]["class"], sugestao_request[indice]["order"],
                                sugestao_request[indice]["family"], sugestao_request[indice]["genus"],
                                sugestao_request[indice]["species"], sugestao_request[indice]["canonicalName"])
                            self.hierarquia_taxonomiaca.Definir_Sugestao_Hierarquica(
                                sugestao_request[indice]["kingdom"], sugestao_request[indice]["phylum"],
                                sugestao_request[indice]["class"], sugestao_request[indice]["order"],
                                sugestao_request[indice]["family"], sugestao_request[indice]["genus"],
                                sugestao_request[indice]["species"], sugestao_request[indice]["canonicalName"])
                        except:
                            print(
                                'http://api.gbif.org/v1/species/suggest?q=' + nome_errado + '&rank=SPECIES&strict=true')
                        self.hierarquia_verificada[nome_errado]["Reino"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Reino()) if self.hierarquia_taxonomiaca.get_Sugestao_Reino() not in \
                                                                                 self.hierarquia_verificada[
                                                                                     nome_errado]["Reino"][
                                                                                     "Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Filo"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Filo()) if self.hierarquia_taxonomiaca.get_Sugestao_Filo() not in \
                                                                                self.hierarquia_verificada[nome_errado][
                                                                                    "Filo"]["Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Classe"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Classe()) if self.hierarquia_taxonomiaca.get_Sugestao_Classe() not in \
                                                                                  self.hierarquia_verificada[
                                                                                      nome_errado]["Classe"][
                                                                                      "Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Ordem"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Ordem()) if self.hierarquia_taxonomiaca.get_Sugestao_Ordem() not in \
                                                                                 self.hierarquia_verificada[
                                                                                     nome_errado]["Ordem"][
                                                                                     "Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Família"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Familia()) if self.hierarquia_taxonomiaca.get_Sugestao_Familia() not in \
                                                                                   self.hierarquia_verificada[
                                                                                       nome_errado]["Família"][
                                                                                       "Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Gênero"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Genero()) if self.hierarquia_taxonomiaca.get_Sugestao_Genero() not in \
                                                                                  self.hierarquia_verificada[
                                                                                      nome_errado]["Gênero"][
                                                                                      "Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Espécie"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Especie()) if self.hierarquia_taxonomiaca.get_Sugestao_Especie() not in \
                                                                                   self.hierarquia_verificada[
                                                                                       nome_errado]["Espécie"][
                                                                                       "Sugestão"] else None
                        self.hierarquia_verificada[nome_errado]["Nome Científico"]["Sugestão"].append(
                            self.hierarquia_taxonomiaca.get_Sugestao_Scientific_Name()) if self.hierarquia_taxonomiaca.get_Sugestao_Scientific_Name() not in \
                                                                                           self.hierarquia_verificada[
                                                                                               nome_errado][
                                                                                               "Nome Científico"][
                                                                                               "Sugestão"] else None

                        self.hierarquia_verificada[nome_errado]["Reino"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Reino()
                        self.hierarquia_verificada[nome_errado]["Filo"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Filo()
                        self.hierarquia_verificada[nome_errado]["Classe"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Classe()
                        self.hierarquia_verificada[nome_errado]["Ordem"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Ordem()
                        self.hierarquia_verificada[nome_errado]["Família"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Familia()
                        self.hierarquia_verificada[nome_errado]["Gênero"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Genero()
                        self.hierarquia_verificada[nome_errado]["Espécie"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Especie()
                        self.hierarquia_verificada[nome_errado]["Nome Científico"][
                            "Corretude"] = self.hierarquia_taxonomiaca.get_Corretude_Scientific_Name()
                        self.hierarquia_verificada[nome_errado]["Nome Científico"]["Fonte"] = "GBIF"

    def get_Hierarquia_verificada(self):
        return self.hierarquia_verificada

    def Ocorrencia_de_String_na_Coluna(self, coluna):
        tratar_coluna = self.planilha.col_values(coluna, 1)
        coluna_tratada = {}
        for nome in tratar_coluna:
            if nome in coluna_tratada:
                pass
            else:
                coluna_tratada[nome] = {"quantidade": tratar_coluna.count(nome)}
        return coluna_tratada

    def Comparar_String(self, String1, String2):

        Ratio_valor = fuzz.ratio(String1.lower(), String2.lower())
        Partial_Ratio_valor = fuzz.partial_ratio(String1.lower(), String2.lower())
        Token_Sort_Ratio_valor = fuzz.token_sort_ratio(String1, String2)
        Token_Set_Ratio_valor = fuzz.token_set_ratio(String1, String2)
        Media = (Ratio_valor + Partial_Ratio_valor + Token_Sort_Ratio_valor + Token_Set_Ratio_valor) / 4

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
                if self.Comparar_String(nome1, nome2) > 60 and nome1 != nome2:
                    sugestoes.append({"Similaridade de": self.Comparar_String(nome1, nome2), "Sugestão de nome": nome2})
            tratar_coluna[nome1]["Sugestões"] = sugestoes
        return tratar_coluna
