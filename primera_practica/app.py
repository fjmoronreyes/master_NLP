#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import re
import csv
from collections import Counter
import nltk
from nltk.tokenize import word_tokenize
from nltk.probability import FreqDist
from importlib import reload

reload(sys)  
#sys.setdefaultencoding('utf8')


#Abrimos el fichero de texto

f = open ('texto.txt')
freqdist = nltk.FreqDist()
words=nltk.word_tokenize(f.read())
fd = nltk.FreqDist(word.lower() for word in words)
fdf= fd.most_common(100)

print('Palabras del texto ordenadas por frecuencia')
t=''
for w in fdf:
    t+='('+w[0]+','+str(w[1])+') '
print (t)


########################################
# DICCIONARIO DE EXPRESIONES LITERALES #
########################################
'''Aquí vamos a definir, mediante literales, etiquetas para clases cerradas u otros grupos más definidos.
 Este grupo no presenta gran variabilidad, así que se ha apostado por un etiquetado más estricto.
 Los adjetivos y los adversios se incluirá aquí y también en el apartado de expresiones regulares

PREPOSICIONES
CONJUNCIONES
ARTÍCULOS
DETERMINANTES
PRONOMBRES
NUMERALES
INTERJECCIONES
ABREVIATURAS
ADVERBIOS
ADJETIVOS
DÍAS DE LA SEMANA

VERBOS IRREGULARES
'''

dict ={}

#CREAMOS EL DICCIONARIO DE CLASES CERRADAS MEDIANTE UN ARCHIVO DE CONFIGURACIÓN EXTERNO (CSV)
reader = csv.reader(open('clases-cerradas.csv'), delimiter='\t')

dict = {}
for rows in reader:
    dict.update({rows[0]:rows[1]})


##################################
# LISTA DE EXPRESIONES REGULARES #
##################################
'''Para aquellos grupos más difíciles de definir, como nombres o verbos, se apostará por expresiones regulares,
menos precisas que un literal pero más generalizables. También añadiremos expresiones regulares que puedan servirnos
para grupos fácilmente abarcables por ellas

NUMERALES
SIGNOS DE PUNTUACIÓN
VERBOS
SUSTANTIVOS

'''


p=[
    (r'[0-9]+(º|ª)','NUM'), # Expresión regular para ordinales
    (r'[0-9]+','NUM'), # Expresión regular para números
    (r'[_"¡!¿;,.:\'()-/=~.-]+','PUNCT'), # Expresión regular para puntuación
    (r'.*mente$','ADV'), # Expresión regular para advervios
    ####VERBOS
    #INFITIVOS, PARTICIPIOS Y GERUNDIOS
    #Infinitivo
    (r'.*ar$','VN'),
    (r'.*er$','VN'),
    (r'.*ir$','VN'),
    #Participio
    (r'.*ado$','VP'),
    (r'.*ido$','VP'),
    (r'.*ído$','VP'), 
    #Gerundio
    (r'.*ando$','VG'),
    (r'.*iendo$','VG'),
    (r'.*endo$','VG'), 
    (r'.*yendo$','VG'), 
    ##IMPERTATIVOS PLURALES
    (r'.*ad$','VM'),
    (r'.*ed$','VM'), 
    (r'.*id$','VM'), 
    ### INDICATIVO
    ##CONDICIONAL - Se coloca primero para evitar confusiones, por ejemplo, con el indicativo.
    #Primera conjugación
    (r'.*aría$','VCF1S'),
    (r'.*arías$','VCF2S'),
    (r'.*aría$','VCF3S'),
    (r'.*aríamoss$','VCF1P'),
    (r'.*aríais$','VCF2P'),
    (r'.*arían$','VCF3P'),
    #Segunda conjugación
    (r'.*ería$','VCF1S'),
    (r'.*erías$','VCF2S'),
    (r'.*ería$','VCF3S'),
    (r'.*eríamoss$','VCF1P'),
    (r'.*eríais$','VCF2P'),
    (r'.*erían$','VCF3P'),
    #Tercera conjugación
    (r'.*iría$','VCF1S'),
    (r'.*irías$','VCF2S'),
    (r'.*iría$','VCF3S'),
    (r'.*iríamoss$','VCF1P'),
    (r'.*iríais$','VCF2P'),
    (r'.*irían$','VCF3P'),
    ##PRESENTE DE INDICATIVO - 1 Y 2 persona del plural
    (r'.*amos$','VIP1P'),
    (r'.*emos$','VIP1P'),
    (r'.*imos$','VIP1P'),
    (r'.*áis$','VIP2P'),
    (r'.*éis$','VIP2P'),
    (r'.*ís$','VIP2P'),
    ##PRETÉRITO IMPERFECTO DE INDICATIVO --> 1 y 3 persona se neutralizan sólo en primera
    #Primera conjugación
    (r'.*aba$','VII1S'),
    (r'.*abas$','VII2S'),
    (r'.*ábamos$','VII1P'),
    (r'.*abais$','VII2P'),
    (r'.*aban$','VII3P'),
    #Segunda conjugación y tercera conjugación
    (r'.*ía$','VII1S'),
    (r'.*ías$','VII2S'),
    (r'.*íamos$','VII1P'),
    (r'.*íais$','VII2P'),
    (r'.*ían$','VII3P'),
    ##PRETÉRITO PERFECTO SIMPLE DE INDICATIVO - No contamos con la primera del plural por ser igual que en presente 1P
    #Primera conjugación
    (r'.*é$','VIS1S'),
    (r'.*aste$','VIS2S'),
    (r'.*ó$','VIS3S'),
    (r'.*asteis$','VIS2P'),
    (r'.*aron$','VIS3P'),
    #Segunda conjugación y tercera conjugación
    (r'.*í$','VIS1S'),
    (r'.*iste$','VIS2S'),
    (r'.*ió$','VIS3S'),
    (r'.*isteis$','VIS2P'),
    (r'.*ieron$','VIS3P'),
    ##FUTURO DE INDICATIVO
    #Primera conjugación
    (r'.*aré$','VIF1S'),
    (r'.*arás$','VIF2S'),
    (r'.*ará$','VIF3S'),
    (r'.*aremos$','VIF1P'),
    (r'.*aréis$','VIF2P'),
    (r'.*arán$','VIF3P'),
    #Segunda conjugación
    (r'.*eré$','VIF1S'),
    (r'.*erás$','VIF2S'),
    (r'.*erá$','VIF3S'),
    (r'.*eremos$','VIF1P'),
    (r'.*eréis$','VIF2P'),
    (r'.*erán$','VIF3P'),
    #Tercera conjugación
    (r'.*iré$','VIF1S'),
    (r'.*irás$','VIF2S'),
    (r'.*irá$','VIF3S'),
    (r'.*iremos$','VIF1P'),
    (r'.*iréis$','VIF2P'),
    (r'.*irán$','VIF3P'),
    ### SUBJUNTIVO
    ##PRETÉRITO IMPERFECTO DEL SUBJUNTIVO
    #Primera conjugación
    (r'.*ara$','VSI1S'),
    (r'.*ase$','VSI1S'),
    (r'.*aras$','VSI2S'),
    (r'.*ases$','VSI2S'),
    (r'.*ara$','VSI3S'),
    (r'.*ase$','VSI3S'),
    (r'.*áramos$','VSI1P'),
    (r'.*ásemos$','VSI1P'),
    (r'.*arais$','VSI2P'),
    (r'.*aseis$','VSI2P'),
    (r'.*aran$','VSI3P'),
    (r'.*asen$','VSI3P'),
    #Segunda conjugación y tercera conjugación
    (r'.*iera$','VSI1S'),
    (r'.*iese$','VSI1S'),
    (r'.*ieras$','VSI2S'),
    (r'.*ieses$','VSI2S'),
    (r'.*iera$','VSI3S'),
    (r'.*iese$','VSI3S'),
    (r'.*iéramos$','VSI1P'),
    (r'.*iésemos$','VSI1P'),
    (r'.*ierais$','VSI2P'),
    (r'.*ieseis$','VSI2P'),
    (r'.*ieran$','VSI3P'),
    (r'.*iesen$','VSI3P'),
    ##FUTURO DEL SUBJUNTIVO - Neutralizamos primera y tercera persona
    #Primera conjugación 
    (r'.*are$','VSF1S'),
    (r'.*ares$','VSF2S'),
    (r'.*áremos$','VSF1P'),
    (r'.*areis$','VSF2P'),
    (r'.*aren$','VSF3P'),
    #Segunda conjugación y tercera conjugación
    (r'.*iere$','VSF1S'),
    (r'.*ieres$','VSF2S'),
    (r'.*iéremos$','VSF1P'),
    (r'.*iereis$','VSF2P'),
    (r'.*ieren$','VSF3P'),
    #######################
    #SUSTANTIVOS FEMENINOS - SINGULAR
    #Excepciones
    (r'.*ma$','NCMS'),
    (r'.*ad$','NCFS'),
    (r'.*a$','NCFS'),
    (r'.*z$','NCFS'),
    (r'.*eza$','NCFS'),
    (r'.*ad$','NCFS'),
    (r'.*ón$','NCFS'),
    (r'.*is$','NCFS'),
    (r'.*ie$','NCFS'),
    (r'.*umbre$','NCFS'),
    (r'.*ed$','NCFS'),
    (r'.*id$','NCFS'),
    (r'.*ud$','NCFS'),
    (r'.*ia$','NCFS'),
    (r'.*ie$','NCFS'),
    #######################
    #SUSTANTIVOS FEMENINOS - PLURAL
    (r'.*as$','NCFP'),
    ########################
    #SUSTANTIVOS MASCULINOS
    (r'.*ambre$','NCMS'),
    (r'.*aje$','NCMS'),
    (r'.*ar$','NCMS'),
    (r'.*er$','NCMS'),
    (r'.*or$','NCMS'),
    (r'.*an|én|ín|ón|ún$','NCMS'),
    (r'.*ate|ete|ote$','NCMS'),
    (r'.*é|és$','NCMS'),
    (r'.*che$','NCMS'),
    (r'.*miento$','NCMS'),
    (r'.*o$','NCMS'),
    (r'.*$','NCMS'),
    #######################
    #SUSTANTIVOS MASCULINOS - PLURAL
    (r'.*os$','NCMP'),
    (r'.*es$','NCMP')
    ]



# Iteramos y mostramos los resultados
rt=nltk.RegexpTagger(p)
taggedText=rt.tag(words)
for item in taggedText:
#   if dict.has_key(item[0]):
    if item[0] in dict:
        print (item[0]+' '+dict[item[0]])
    else:
        print (item[0]+' '+item[1])

sys.exit()
