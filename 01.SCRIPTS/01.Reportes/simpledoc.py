# -*- coding: utf-8 -*-
from reportlab.lib.pagesizes import A4, landscape, portrait
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table, Flowable, SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib import randomtext
from reportlab import platypus
from functions import pdf_functions
from reportlab.lib.units import inch, cm

import os, random


styles = getSampleStyleSheet()
cwd = os.getcwd() + '\\images'
doc = SimpleDocTemplate("salida.pdf",pagesize=A4)


#################             IMAGES       ##############################
generalMontoCreditoDebito = cwd + '\\4.png'
generalNumeroOperacionesCredito = cwd + '\\8.png'
generalEstadisticaDescriptivaGeneral = cwd + '\\8.png'
generalOcupaciones = cwd + '\\8.png'
generalActividades = cwd + '\\8.png'

clusterPoblacion = cwd + '\\8.png'
clusterGeneral = cwd + '\\8.png'
clusterTotalIngresosEgresos = cwd + '\\8.png'
clusterMontoCreditoDebito = cwd + '\\8.png'
clusterPatrimonio = cwd + '\\8.png'

#############   AJUSTES A IMAGEN       ##################################

ajuste= 0.25
ancho =  700- (700*ajuste)
alto =  450 - (450*ajuste)
x= 80
y= 400

########################################################################

elements = []

im = Image(generalMontoCreditoDebito , width=ancho, height=alto)
im.hAlign = 'CENTER'

elements.append(im)
doc.build(elements)
