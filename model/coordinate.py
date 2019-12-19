class Coordenadas:

    def __init__(self, Plan):
        self.coluna_latitude_plan = []
        self.coluna_longitude_plan = []
        self.planilha = Plan
        self.coordenadas = {
            "latitude":
                {
                    "grau": None,
                    "minuto": None,
                    "segundo": None,
                    "emisferio": None,
                    "decimal": None
                },
            "longitude":
                {
                    "grau": None,
                    "minuto": None,
                    "segundo": None,
                    "emisferio": None,
                    "decimal": None
                }
        }
        self.lista_coordenadas = []
        self.emisferios = ["w", "W", "s", "S", "e", "E", "n", "N"]

    def set_Latitude_Column_values(self, coluna_lat):
        if (type(coluna_lat) == str):
            indice_coluna = self.planilha.row_values(0).index(coluna_lat)
            self.coluna_latitude_plan = self.planilha.col_values(indice_coluna, 1)
            self.coluna_latitude_plan = list(filter(None,
                                                    self.coluna_latitude_plan))  # O Comando filter serve para retirar valores vázios da lista, porém ele retorna apenas o endereço do objeto, utilizo o list para que o endereço seja convertido em um objeto do tipo lsita
        elif (type(coluna_lat) == int):
            self.coluna_latitude_plan = self.planilha.col_values(coluna_lat, 1)
        elif (type(coluna_lat) == dict):
            self.coluna_latitude_plan = list(filter(None, coluna_lat))

    def set_Longitude_Column_values(self, coluna_lng):
        if (type(coluna_lng) == str):
            indice_coluna = self.planilha.row_values(0).index(coluna_lng)
            self.coluna_longitude_plan = self.planilha.col_values(indice_coluna, 1)
            self.coluna_longitude_plan = list(filter(None, self.coluna_longitude_plan))
        elif (type(coluna_lng) == int):
            self.coluna_longitude_plan = self.planilha.col_values(coluna_lng, 1)
        elif (type(coluna_lng) == dict):
            self.coluna_longitude_plan = list(filter(None, coluna_lng))

    def get_Latitude_Column_values(self):
        if (self.coluna_latitude_plan == []):
            return "Coluna vazia."
        else:
            return self.coluna_latitude_plan

    def get_Longitude_Column_values(self):
        if (self.coluna_longitude_plan == []):
            return "Coluna vazia."
        else:
            return self.coluna_longitude_plan

    # Precisa ser melhorado o método que os valores são inseridos no dicionario coordenadas. Mas por enquanto vai ser feito assim.
    def Formatar_Lat_Lng(self, coord, nome_coord):  # Bem vindo a loucura de Elielson. Ta grande, mas funciona.
        valor_separado = str(coord).split()
        valor_juntado = " ".join(valor_separado)
        espacos = valor_juntado.count(" ")
        emisferio_ultimo = False
        emisferios_negativos = ["w", "W", "s", "S"]
        possui_emisf = True if list(set(self.emisferios).intersection(valor_separado)) != [] else False
        emisf_neg = True if list(set(valor_separado).intersection(emisferios_negativos)) != [] else False
        # Caso a coordenada tenha alguma letra, significa que o decimal dela será descrito como positivo ou negativo com base no emisfério descrito
        if possui_emisf:
            for coordenada in valor_separado:
                # Caso a coordenada esteja em formato Grau, minuto por segundo.
                if espacos == 3:

                    # Referente ao emisfério
                    if (coordenada in self.emisferios) and (valor_separado.index(coordenada) != 0):
                        self.coordenadas[nome_coord]["emisferio"] = coordenada
                        if (emisf_neg):
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"] * -1
                    elif (coordenada in self.emisferios) and (valor_separado.index(coordenada) == 0):
                        self.coordenadas[nome_coord]["emisferio"] = coordenada

                    # Referente ao grau
                    if ("°" in coordenada):
                        if valor_separado.index(coordenada) == 0:
                            emisferio_ultimo = True
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace("°", "").replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["grau"]:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"].replace("-", "")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                    elif (coordenada not in self.emisferios) and (valor_separado.index(coordenada) == 0):
                        emisferio_ultimo = True
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["grau"]:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"].replace("-", "")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 1) and emisferio_ultimo == False:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                        if emisf_neg:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"] * -1

                    # Referente aos minutos
                    if ("'" in coordenada):
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace("'", "").replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 1) and emisferio_ultimo:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["minuto"]:
                            self.coordenadas[nome_coord]["minuto"] = self.coordenadas[nome_coord]["minuto"].replace("-",
                                                                                                                    "")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 2) and emisferio_ultimo == False:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                        if emisf_neg:
                            self.coordenadas[nome_coord]["minuto"] = self.coordenadas[nome_coord]["minuto"] * -1

                    # Referente aos segundos
                    if ('"' in coordenada):
                        self.coordenadas[nome_coord]["segundo"] = coordenada.replace('"', "").replace(",", ".")
                        self.coordenadas[nome_coord]["segundo"] = float(self.coordenadas[nome_coord]["segundo"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 2) and emisferio_ultimo:
                        self.coordenadas[nome_coord]["segundo"] = coordenada.replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["segundo"]:
                            self.coordenadas[nome_coord]["segundo"] = self.coordenadas[nome_coord]["segundo"].replace(
                                "-", "")
                        self.coordenadas[nome_coord]["segundo"] = float(self.coordenadas[nome_coord]["segundo"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 3) and emisferio_ultimo == False:
                        self.coordenadas[nome_coord]["segundo"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["segundo"] = float(self.coordenadas[nome_coord]["segundo"])
                        if emisf_neg:
                            self.coordenadas[nome_coord]["segundo"] = self.coordenadas[nome_coord]["segundo"] * -1

                # Caso a coordenada esteja em formato Grau por minuto.
                if espacos == 2:

                    # Referente ao emisfério
                    if (coordenada in self.emisferios) and (valor_separado.index(coordenada) != 0):
                        self.coordenadas[nome_coord]["emisferio"] = coordenada.replace(",", ".")
                        if (emisf_neg):
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"] * -1
                    elif (coordenada in self.emisferios) and (valor_separado.index(coordenada) == 0):
                        self.coordenadas[nome_coord]["emisferio"] = coordenada.replace(",", ".")

                    # Referente ao grau
                    if "°" in coordenada:
                        if (valor_separado.index(coordenada) == 0):
                            emisferio_ultimo = True
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace("°", "")
                        if "-" in self.coordenadas[nome_coord]["grau"]:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"].replace("-", "")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                    elif (coordenada not in self.emisferios) and (valor_separado.index(coordenada) == 0):
                        emisferio_ultimo = True
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["grau"]:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"].replace("-", "")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 1) and emisferio_ultimo == False:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                        if emisf_neg:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"] * -1

                    # Referente ao minuto
                    if "'" in coordenada:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace("'", "").replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 1) and emisferio_ultimo:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["minuto"]:
                            self.coordenadas[nome_coord]["minuto"] = self.coordenadas[nome_coord]["minuto"].replace("-",
                                                                                                                    "")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                    elif (coordenada not in self.emisferios) and (
                            valor_separado.index(coordenada) == 2) and emisferio_ultimo == False:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                        if emisf_neg:
                            self.coordenadas[nome_coord]["minuto"] = self.coordenadas[nome_coord]["minuto"] * -1

                            # Caso a coordenada esteja em Grau/Decimal somente
                if espacos == 1:

                    # Referente ao emisfério
                    if (coordenada in self.emisferios) and (valor_separado.index(coordenada) != 0):
                        self.coordenadas[nome_coord]["emisferio"] = coordenada.replace(",", ".")
                        if (emisf_neg):
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"] * -1
                            self.coordenadas[nome_coord]["decimal"] = self.coordenadas[nome_coord]["grau"]
                    elif (coordenada in self.emisferios) and (valor_separado.index(coordenada) == 0):
                        self.coordenadas[nome_coord]["emisferio"] = coordenada.replace(",", ".")

                    # Referente ao grau
                    if "°" in coordenada:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace("°", "").replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["grau"]:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"].replace("-",
                                                                                                                "")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                        self.coordenadas[nome_coord]["decimal"] = self.coordenadas[nome_coord]["grau"]
                    elif (coordenada not in self.emisferios) and (valor_separado.index(coordenada) == 0):
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        if "-" in self.coordenadas[nome_coord]["grau"]:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"].replace("-", "")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                        self.coordenadas[nome_coord]["decimal"] = self.coordenadas[nome_coord]["grau"]
                    elif (coordenada not in self.emisferios) and (valor_separado.index(coordenada) == 1):
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                        if emisf_neg:
                            self.coordenadas[nome_coord]["grau"] = self.coordenadas[nome_coord]["grau"] * -1
                        self.coordenadas[nome_coord]["decimal"] = self.coordenadas[nome_coord]["grau"]
        # Caso não tenha nenhuma letra, o emisfério e descrito apenas pelo sinal de '-', se for positivo é norte, se for negativo é sul.
        else:

            for coordenada in valor_separado:

                # Caso a coordenada esteja em formato Grau, minuto por segundo.
                if espacos == 2:

                    # Referente ao grau.
                    if "°" in coordenada:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace("°", "").replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                    elif valor_separado.index(coordenada) == 0:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])

                    # Referente ao minuto
                    if "'" in coordenada:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace("'", "").replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                    elif valor_separado.index(coordenada) == 1:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])

                    # Referente ao segundo
                    if '"' in coordenada:
                        self.coordenadas[nome_coord]["segundo"] = coordenada.replace('"', "").replace(",", ".")
                        self.coordenadas[nome_coord]["segundo"] = float(self.coordenadas[nome_coord]["segundo"])
                    elif valor_separado.index(coordenada) == 2:
                        self.coordenadas[nome_coord]["segundo"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["segundo"] = float(self.coordenadas[nome_coord]["segundo"])

                # Caso a coordenada esteja em formato Grau por minuto.
                if espacos == 1:

                    # Referente ao grau.
                    if "°" in coordenada:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace("°", "").replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                    elif valor_separado.index(coordenada) == 0:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])

                    # Referente ao minuto.
                    if "'" in coordenada:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace("'", "").replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])
                    elif valor_separado.index(coordenada) == 1:
                        self.coordenadas[nome_coord]["minuto"] = coordenada.replace(",", ".")
                        self.coordenadas[nome_coord]["minuto"] = float(self.coordenadas[nome_coord]["minuto"])

                # Caso a coordenada esteja em formato de Grau/Decimal
                if espacos == 0:

                    # Referente ao grau/decimal
                    if "°" in coordenada:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace("°", "").replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                        self.coordenadas[nome_coord]["decimal"] = self.coordenadas[nome_coord]["grau"]
                    else:
                        self.coordenadas[nome_coord]["grau"] = coordenada.replace("°", "").replace(",", ".")
                        self.coordenadas[nome_coord]["grau"] = float(self.coordenadas[nome_coord]["grau"])
                        self.coordenadas[nome_coord]["decimal"] = self.coordenadas[nome_coord]["grau"]

    def get_Latitude(self):
        return self.coordenadas["latitude"]

    def get_Longitude(self):
        return self.coordenadas["longitude"]

    def Resetar_Valores_Coordenadas(self):
        self.coordenadas = {
            "latitude":
                {
                    "grau": None,
                    "minuto": None,
                    "segundo": None,
                    "emisferio": None,
                    "decimal": None
                },
            "longitude":
                {
                    "grau": None,
                    "minuto": None,
                    "segundo": None,
                    "emisferio": None,
                    "decimal": None
                }
        }

    def Listar_Coordenadas(self):
        return self.lista_coordenadas

    def Converter_Lat_Decimal(self, lat):
        lat_convertida = "Nada"
        lista_lat_convertida = []
        if type(lat) == str:
            self.Resetar_Valores_Coordenadas()
            self.Formatar_Lat_Lng(lat, "latitude")

            if self.get_Latitude()["decimal"] == None:

                if self.get_Latitude()["segundo"] == None:

                    lat_convertida = self.get_Latitude()["grau"]
                    valor_aux_seg = self.get_Latitude()["minuto"] / 60

                    if "-" in str(self.get_Latitude()["grau"]):

                        lat_convertida *= -1
                        lat_convertida = lat_convertida + valor_aux_seg
                        lat_convertida *= -1

                    else:

                        lat_convertida += valor_aux_seg

                else:

                    lat_convertida = self.get_Latitude()["grau"]
                    valor_aux_seg = self.get_Latitude()["segundo"] / 60
                    valor_aux_min = self.get_Latitude()["minuto"] + valor_aux_seg
                    valor_aux_min /= 60

                    if "-" in str(lat_convertida):
                        lat_convertida *= -1
                        lat_convertida = lat_convertida + valor_aux_min
                        lat_convertida *= -1
                    else:
                        lat_convertida += valor_aux_min
            else:

                lat_convertida = self.get_Latitude()["decimal"]

            return lat_convertida
        elif type(lat) == list:

            for l in lat:

                self.Resetar_Valores_Coordenadas()
                self.Formatar_Lat_Lng(l, "latitude")
                if self.get_Latitude()["decimal"] == None:

                    if self.get_Latitude()["segundo"] == None:

                        lat_convertida = self.get_Latitude()["grau"]
                        valor_aux_seg = self.get_Latitude()["minuto"] / 60

                        if "-" in str(self.get_Latitude()["grau"]):

                            lat_convertida *= -1
                            lat_convertida = lat_convertida + valor_aux_seg
                            lat_convertida *= -1

                        else:

                            lat_convertida += valor_aux_seg
                    else:

                        lat_convertida = self.get_Latitude()["grau"]
                        valor_aux_seg = self.get_Latitude()["segundo"] / 60
                        valor_aux_min = self.get_Latitude()["minuto"] + valor_aux_seg
                        valor_aux_min /= 60

                        if "-" in str(lat_convertida):

                            lat_convertida *= -1
                            lat_convertida = lat_convertida + valor_aux_min
                            lat_convertida *= -1

                        else:

                            lat_convertida += valor_aux_min
                else:

                    lat_convertida = self.get_Latitude()["decimal"]
                lista_lat_convertida.append(lat_convertida)
                if (lat_convertida == -72.95):
                    print(self.get_Latitude())
            return lista_lat_convertida

    def Converter_Lng_Decimal(self, lng):

        lng_convertida = "Nada"
        lista_lng_convertida = []

        if type(lng) == str:

            self.Resetar_Valores_Coordenadas()
            self.Formatar_Lat_Lng(lng, "longitude")

            if self.get_Longitude()["decimal"] == None:

                if self.get_Longitude()["segundo"] == None:

                    lng_convertida = self.get_Longitude()["grau"]
                    valor_aux_seg = self.get_Longitude()["minuto"] / 60

                    if "-" in str(self.get_Longitude()["grau"]):

                        lng_convertida *= -1
                        lng_convertida = lng_convertida + valor_aux_seg
                        lng_convertida *= -1

                    else:

                        lng_convertida += valor_aux_seg

                else:

                    lng_convertida = self.get_Longitude()["grau"]
                    valor_aux_seg = self.get_Longitude()["segundo"] / 60
                    valor_aux_min = self.get_Longitude()["minuto"] + valor_aux_seg
                    valor_aux_min /= 60

                    if "-" in str(lng_convertida):

                        lng_convertida *= -1
                        lng_convertida = lng_convertida + valor_aux_min
                        lng_convertida *= -1

                    else:

                        lng_convertida += valor_aux_min
            else:

                lng_convertida = self.get_Longitude()["decimal"]

            return lng_convertida
        elif type(lng) == list:

            for l in lng:

                self.Resetar_Valores_Coordenadas()
                self.Formatar_Lat_Lng(l, "longitude")

                if self.get_Longitude()["decimal"] == None:

                    if self.get_Longitude()["segundo"] == None:

                        lng_convertida = self.get_Longitude()["grau"]
                        valor_aux_seg = self.get_Longitude()["minuto"] / 60

                        if "-" in str(self.get_Longitude()["grau"]):

                            lng_convertida *= -1
                            lng_convertida = lng_convertida + valor_aux_seg
                            lng_convertida *= -1

                        else:

                            lng_convertida += valor_aux_seg

                    else:

                        lng_convertida = self.get_Longitude()["grau"]
                        valor_aux_seg = self.get_Longitude()["segundo"] / 60
                        valor_aux_min = self.get_Longitude()["minuto"] + valor_aux_seg
                        valor_aux_min /= 60

                        if "-" in str(lng_convertida):

                            lng_convertida *= -1
                            lng_convertida = lng_convertida + valor_aux_min
                            lng_convertida *= -1

                        else:

                            lng_convertida += valor_aux_min
                else:

                    lng_convertida = self.get_Longitude()["decimal"]

                lista_lng_convertida.append(lng_convertida)

            return lista_lng_convertida
