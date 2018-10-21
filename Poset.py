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
Created on Sat Jul  1 15:15:59 2017

@author: Felipe
"""

class Set(object):
    
    def __init__(self, A, R):
        '''
        Esse é o construtor da classe Poset.
        Inicializa o conjunto A, a relação R e
        mais alguns atributos.
        O conjunto A deve ser uma lista.
        A relação R deve ser uma lista de tuplas.
        '''
        self.A = A
        self.R = R
        self.reflexive = self.isReflexive()
        self.antiSymmetric = self.isAntiSymmetric()
        self.transitive = self.isTransitive()
        self.irreflexive = self.isIrreflexive()
        self.symmetric = self.isSymmetric()
       
    def isReflexive(self):
        '''
        Saída: Boleano
        Para cada elemento distinto da relação verifica se o mesmo está
        presente na tupla atual, caso esteja verifica se se a tuple atual
        atende a propriedade reflexiva. Se o mesmo se repetir para todas as
        tuplas, então a relação é reflexiva
        '''
        for element in self.A:
            reflexive = False    
            for tup in self.R:
                if element in tup and tup == tuple(reversed(tup)):
                    reflexive = True
                    break                    
            if reflexive == False:
                return reflexive
        return True
    
    def isTransitive(self):
        '''
        Saída: Boleano
        Verifica a transitividade da relação R
        '''
        for a in self.A:
            for tup in self.R:                
                # Se (a, b) com a != b. Aqui não é necessário testar um (a, a)
                # dada a natureza do programa, qualquer relação reflexiva sempre
                # será transitiva
                aRb = False
                bRc = False
                aRc = False
                if tup[0] == a and tup[1] != a:
                    aRb = True
                    b = tup[1]
                    for element in self.R:
                        if b == element[0] and b != element[1] and a != element[1]:
                            bRc = True
                            c = element[1]
                            break
                    if bRc:
                        # se existe um a R b e um b R c.
                        # para determinar se é transitiva a 
                        # relação então deve determinar se 
                        # existe um a R c.
                        for elemento in self.R:
                            if a == elemento[0] and c == elemento[1]:
                                aRc = True
                                break
                if aRb and bRc:
                    # se aRb ^ bRc = Verdadeiro e aRc Falso 
                    # Então existem tuplas da relação que não
                    # atendem a propriedade de transitividade
                    # Caso aRb ou bRc sejam falsos, então a propriedade
                    # de transitividade é atendia.
                    # Prova: falso ^ falso => falso ou verdadeiro sempre
                    # resultará em verdadeiro
                    if not aRc:
                        return False
        return True
        
    def isAntiSymmetric(self):
        '''
        Saída: Boleano
        O método busca por tuplas (a, b) 
        onde a != b e seu recíproco. 
        Caso o recíproco seja encontrado
        então sabemos que a relação não é
        anti-simétrica.
        '''
        bRa = False
        for a in self.A:
           for tup in self.R:
               aRb = False
               if a == tup[0] and a != tup[1]:
                    b = tup[1]
                    aRb = True
                    for tupla in self.R:
                        if b == tupla[0] and a == tupla[1]:
                            bRa = True
                            break
                    if aRb and bRa:
                        return False
        return True

    def isIrreflexive(self):
        '''
        Saída: Boleano
        Para todos os elementos do conjunto A
        procura por tuplas (a, b), onde a = b.
        Caso encontre, retorna falso de imediato.
        Caso não encontre então tem-se uma relação
        que a tende a propriedade irreflexiva.
        '''
        for a in self.A:
            for tup in self.R:
                if a in tup and tup == tuple(reversed(tup)):
                    return False
        return True
        
    def isSymmetric(self):
        '''
        Saída: Boleano
        Se para todo aRb => bRa então
        tem-se uma relação simétrica.
        Para toda tupla (a, b), o método
        busca por uma tupla (b, a), caso não encontre
        retorna falso de imediato.
        '''
        for a in self.A:
            for tup in self.R:
                aRb = False                
                bRa = False
                if a == tup[0] and a != tup[1]:
                    aRb = True
                    b = tup[1]
                    for tupla in self.R:
                        if b == tupla[0] and a == tupla[1]:
                            bRa = True
                    if aRb:
                        if not bRa:
                            return False
        return True
        
    def isPoset(self):
        return self.reflexive and self.antiSymmetric and self.transitive 
    
    def properties(self):
        p = 'A relação atende as propriedades :\n'
        if self.reflexive:
            p += 'Reflexiva\n'
        if self.antiSymmetric:
            p += 'Anti-simétrica\n'
        if self.transitive:
            p += 'Transitiva\n'
        if self.irreflexive:
            p += 'Irreflexiva\n'
        if self.symmetric:
            p += 'Simétrica\n'            
        return p                 
    
    def genPowerset(self):
        '''
        Gera o conjunto das partes dos elementos em A
        '''
        length = len(self.getA())
        powerset = []
        for i in range(1 << length):
            powerset.append([self.getA()[j] for j in range(length) if (i & (1 << j))])
        return powerset
        
    # Retorna uma lista de caracteres com o conjunto A    
    def getA(self):
        return self.A
    
    # Retorna uma lista de tuplas com a relação R    
    def getR(self):
        return self.R  

    # retorna True ou False
    def getIrreflexive(self):
        return self.irreflexive
    
    # retorna True ou False
    def getReflexive(self):
        return self.reflexive
        
    # retorna True ou False
    def getAntiSymmetric(self):
        return self.antiSymmetric
        
    # retorna True ou False
    def getTransitive(self):
        return self.transitive
        
    # retorna True ou False
    def getSymmetric(self):
        return self.symmetric    
    
