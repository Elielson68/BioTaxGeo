class Hierarchy_Taxon:
       def __init__(self, k=None, p=None, c=None, o=None, f=None, g=None, e=None, sn=None):
              self.Scientific_Name = sn
              self.kingdom = k
              self.phylum = p
              self.classs = c
              self.order = o
              self.family = f
              self.genus = g
              self.specie = e

       def get_Kingdom(self):
              return self.kingdom

       def get_Phylum(self):
              return self.phylum

       def get_Classs(self):
              return self.classs

       def get_Order(self):
              return self.order

       def get_Family(self):
              return self.family

       def get_Genus(self):
              return self.genus

       def get_Specie(self):
              return self.specie

       def set_Kingdom(self, k):
              self.kingdom = k

       def set_Phylum(self, p):
              self.phylum = p

       def set_Classs(self, c):
              self.classs = c

       def set_Order(self, o):
              self.order = o

       def set_Family(self, f):
              self.family = f

       def set_Genus(self, g):
              self.genus = g

       def set_Specie(self, s):
              self.specie = s