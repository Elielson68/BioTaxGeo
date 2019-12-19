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
        if (self.especie == especie.replace(genero + " ", "")) or (
                self.especie == especie.replace(self.genero + " ", "")):
            self.corretude_especie = "EXACT"
        else:
            self.corretude_especie = "FUZZY"
        self.corretude_scientific_name = "EXACT" if self.Scientific_Name == Scientific_Name else "FUZZY"

    def Definir_Sugestao_Hierarquica(self, reino, filo, classe, ordem, familia, genero, especie, Scientific_Name):
        self.sugestao_reino = None if self.corretude_reino == "EXACT" else reino
        self.sugestao_filo = None if self.corretude_filo == "EXACT" else filo
        self.sugestao_classe = None if self.corretude_classe == "EXACT" else classe
        self.sugestao_ordem = None if self.corretude_ordem == "EXACT" else ordem
        self.sugestao_familia = None if self.corretude_familia == "EXACT" else familia
        self.sugestao_genero = None if self.corretude_genero == "EXACT" else genero
        if self.corretude_especie == "EXACT":
            self.sugestao_especie = None
        else:
            self.sugestao_especie = especie.replace(genero + " ", "") if genero in especie else especie.replace(
                self.genero + " ", "")
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