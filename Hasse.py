'''
   Copyright (C) 2017 Felipe de Lima Peressim
 
  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
 
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.
 
  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 16:13:40 2017

@author: felipe
"""

from Poset import Set

class Hasse(object):
    
    def __init__(self, poset):
        '''
        Construtor da classe. Espera uma instância
        de um objeto do tipo Set como argumento.
        Assume-se que o objeto seja um 'poset'.
        Atribui o objeto a variável de instância
        e inicializa os objetos emin e emax, que
        são os elementos mínimos e máximos
        '''
        self.poset = poset            
        self.emin = self.minElements()
        self.emax = self.maxElements()
        if type(self.limitMin()) == list:
            self.lMin = True
        else:
            self.lMin = False
        if type(self.limitMax()) == list:
            self.lMax = True
        else:
            self.lMax = False
    
    def minElements(self):
        '''
        Retorna os elementos 
        mínimos da relação R. 
        Percorre todas as tuplas e
        busca por elementos que aparecem
        na posição (x, y) x, mas não 
        na posição y sendo x != y.
        '''
        A = self.poset.getA()
        R = self.poset.getR()  
        emin = []
       
        for a in A:
            for tup in R:
                if a == tup[0]:# and a != tup[1]:
                    isMin = True
                    for tupla in R:
                        if a != tupla[0] and a == tupla[1]:
                            isMin = False
                            break
                    if isMin and a not in emin:
                        emin.append(a)
        return emin
        
    def maxElements(self):
        '''
        Retorna os elementos 
        máximos da relação R. 
        Percorre todas as tuplas e
        busca por elementos que aparecem
        na posição (x, y) y, mas não 
        na posição x, sendo x != y.
        '''
        A = self.poset.getA()
        R = self.poset.getR()  
        emax = []       
        for a in A:
            for tup in R:
                if a == tup[1]: #a != tup[0] and                     
                    isMax = True
                    for tupla in R:
                        if a == tupla[0] and a != tupla[1]:
                            isMax = False
                            break
                    if isMax and a not in emax:
                        emax.append(a)
        return emax
        
    def limitMin(self):
        '''
        Se existir apenas um elemento mínimo
        então tem-se um limite mínimo
        '''
        emin = self.getEmin()
        if len(emin) == 1:
            return emin
        else:
            return 'Não exite limite mínimo'

    def limitMax(self):
        '''
        Se existir apenas um elemento máximo
        então tem-se um limite máximo
        '''        
        emax = self.getEmax()
        if len(emax) == 1:
            return emax
        else:
            return 'Não exite limite máximo'

    def getSucessor(self, element):
        '''
        Entrada: element => character ou número
        Saída: Lista com elementos
        Método auxiliar, retorna uma lista
        com todos os elementos que sucedem
        um determinado elemento 'element'.
        '''
        R = self.poset.getR()
        sucessors = []
        for tup in R:
            if element == tup[0]:
                sucessors.append(tup[1])
        return sucessors
    
    def getPredecessor(self, element):
        '''
        Entrada: element => character ou número
        Saída: Lista com elementos
        Método auxiliar, retorna uma lista
        com todos os elementos que sucedem
        um determinado elemento 'element'.
        '''
        R = self.poset.getR()
        predecessors = []
        for tup in R:
            if element == tup[1]:
                predecessors.append(tup[0])
        return predecessors
    
    def intersect(self, l1, l2):
        '''
        Entrada: Duas listas contendo characteres ou números
        Saída: Intersecção dos elementos das duas listas.
        Faz a intersecção de dois subconjuntos. Assume que
        os elementos de cada lista apareçam apenas uma vez
        em cada lista.
        '''
        inter = []
        for element in l1:
            if element in l2:
                inter.append(element)
        return inter
        
    def fs(self, subset):
        '''
        Entrada: subset => Subconjunto do conjunto A.
        Saída: Lista contendo a fronteira superior de subset
        Cada elemento do subconjunto subset
        é passado para o método getSucessorPath
        o qual retorna uma lista com todos os 
        sucessores de cada elemento do subconjunto.
        As listas são guardadas dentro da lista Path,
        ao final é feito a intersecção através do método
        auxiliar intersect entre os caminhos resultando 
        assim na fronteira superior dos elementos
        contidos em subset
        '''
        if len(subset) < 2:
            return []

        path = []
        fts = []
        for element in subset:
            path.append(self.getSucessor(element))
        
        i = 1
        fts = path[0]
        while i < len(path):
            fts = self.intersect(fts, path[i])
            i = i + 1

        return fts
    
    def fi(self, subset):
        '''
        Entrada: subset => Subconjunto do conjunto A.
        Saída: Lista contendo a fronteira inferior de subset
        Cada elemento do subconjunto subset
        é passado para o método getPredecessor
        o qual retorna uma lista com todos os 
        predecessores de cada elemento do subconjunto.
        As listas são guardadas dentro da lista Path,
        ao final é feito a intersecção através do método
        auxiliar intersect entre os caminhos resultando 
        assim na fronteira superior dos elementos
        contidos em subset
        '''
        if len(subset) < 2:
            return []

        path = []
        fti = []
        for element in subset:
            path.append(self.getPredecessor(element))
        i = 1
        fti = path[0]
        while i < len(path):
            fti = self.intersect(fti, path[i])
            i = i + 1
            
        return fti

    def fsMin(self, subset):
        '''
        Entrada: subset => Lista de character ou número
        Retorna uma lista com a Fronteira superior mínima
        de um conjunto A. Torna-se um novo conjunto o qual
        contém a fronteira superior do subset, e com isso
        os elementos que não pertencem a A, são excluídos 
        da relação R e uma nova relação é gerada, caso nessa relação
        '''
        A = self.fs(subset)
        R = self.newR(A)
        poset = Set(A, R)
        hasse = Hasse(poset)
        if hasse.lMin:
            return hasse.limitMin()                 
        else:
            return []
    
    def fiMax(self, subset):
        '''
        Entrada: subset => Lista de character ou número
        Retorna uma lista com a Fronteira inferior máxima
        de um conjunto A. Torna-se um novo conjunto o qual
        contém a fronteira superior do subset, e com isso
        os elementos que não pertencem a A, são excluídos 
        da relação R e uma nova relação é gerada, caso nessa relação
        '''
        A = self.fi(subset)
        R = self.newR(A)
        poset = Set(A, R)
        hasse = Hasse(poset)
        if hasse.lMax:
            return hasse.limitMax()                 
        else:
            return []
            
    def newR(self, A):
        '''
        Entrada: A => Conjunto com character ou número
        Saída: Lista de tuplas com a nova relação
        Método auxiliar que adiciona apenas tuplas que contenham
        elementos que estejam no conjunto A
        '''
        R = []
        for tup in self.poset.getR():
            if tup[0] in A and tup[1] in A:  
                R.append(tup)
        return R
    
    def isReticulate(self):
        '''
        Saída: Boleano True, False
        Testa todas as tuplas da
        relação binária AXA e verifica
        se cada têm uma fronteira superior
        mínima e fronteira inferior máxima.
        caso seja, então tem-se um reticulado
        '''
        for a in self.poset.getA():
            for b in self.poset.getA():
                if a != b:
                    if len(self.fsMin([a, b])) == 0 or len(self.fiMax([a, b])) == 0:
                        return False
        return True
                        
    def hasLimitMin(self):
        '''
        Retorna booleano caso o Poset
        tenha Limite Mínimo
        '''
        return self.lMin
    
    def hasLimitMax(self):
        '''
        Retorna booleano caso o Poset
        tenha Limite Mínimo
        '''
        return self.lMax
        
    # Retorna os elementos mínimos
    def getEmin(self):
        return self.emin
    
    # Retorna os elementos máximos
    def getEmax(self):
        return self.emax
    
    def drawDiagram(self):
        '''
        Desenha o diagrama de Hasse
        usando a lib networkx.
        '''
        import networkx as nx
        import matplotlib.pyplot as plt

        G=nx.DiGraph()
        A = self.poset.getA()
        G.add_nodes_from(A)
        edges = self.makeEdges()
        G.add_edges_from(edges)
        pos = self.makePos(edges)
        nx.draw(G, pos, with_labels=True, arrows=True)
        plt.savefig("diagrama")

    def makeEdges(self):
        '''
        Gera uma lista com tuplas 
        que representam os edges 
        usados para contruir o
        diagrama de Hasse.
        '''  
        edges = []
        for element in self.poset.getA():
            elementPredecessorLength = len(self.getPredecessor(element))
            elementSucessorLength = len(self.getSucessor(element))
            # Quando o elemento não tiver sucessores e nem predecessores
            # ele é adicionado com ele mesmo.
            if elementPredecessorLength <= 1 and elementSucessorLength <= 1:
                edges.append((element, element))
            else:
                # Quando os sucessores de um elemento
                # forem o próprio elemento e mais 
                if elementSucessorLength > 1:
                    noAmbiguity = True 
                    for sucessor in self.getSucessor(element)[1:]:
                        for candidateToMakePair in self.getSucessor(element):
                            if candidateToMakePair == element or candidateToMakePair == sucessor:
                                continue
                            else:
                                if (candidateToMakePair, sucessor) in self.poset.getR(): 
                                    noAmbiguity = False
                        if noAmbiguity:
                            edges.append((element, sucessor))                                
                        noAmbiguity = True
        return edges

    def makePos(self, edges):
        '''
        Cria a posição dos nodos.
        '''            
        x = 1
        y = len(edges)
        pos = {}
        empty = lambda x : x == []
        hasse = Hasse(Set(self.poset.getA(), self.poset.getR()))
        
        while not empty(hasse.getEmax()):
            for e in hasse.getEmax():
                pos[e] = (x, y)
                x += 0.2
            x = x/2 
            y -= 0.54
            A = hasse.poset.getA()[:]
            for e in hasse.getEmax():
                A.remove(e)
            hasse = Hasse(Set(A, hasse.newR(A)))
        return pos
