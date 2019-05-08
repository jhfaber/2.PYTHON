from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Image,Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch, cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import os

cwd = os.getcwd() + '\\images'

c = canvas.Canvas("descriptiva2.pdf")

#Header
c.setLineWidth(.3)
c.setFont('Helvetica', 22)
c.drawString(30,750,'CONSOFI')

c.setFont('Helvetica', 12)
c.drawString(30,735,'Reporte descriptivo')

c.setFont('Helvetica-Bold', 12)
c.drawString(480, 750,"01/04/2018")
c.line(460,747,560,747)

################# TABLE  #####################
students = [{'#':'1','name':'Diana','b1':'3.4','b2':'1.2','b3':'4.5','total':'3.36'},
            {'#':'2','name':'Fabian','b1':'2.4','b2':'2.2','b3':'4.5','total':'4.36'},
            {'#':'3','name':'Zulay','b1':'6.4','b2':'0.2','b3':'4.5','total':'2.36'},
            {'#':'4','name':'John','b1':'3.4','b2':'2.2','b3':'4.5','total':'1.36'},
            {'#':'5','name':'Martha','b1':'3.4','b2':'1.2','b3':'3.5','total':'4'},
            ]

#TABLE HEAD
styles = getSampleStyleSheet()
styleBH = styles["Normal"]
styleBH.aligment  = TA_CENTER
styleBH.fontSize = 10

numero = Paragraph('''#''',styleBH)
alumno = Paragraph('''Empleado''',styleBH)
b1= Paragraph('''BIM1''',styleBH)
b2= Paragraph('''BIM2''',styleBH)
b3= Paragraph('''BIM3''',styleBH)
total = Paragraph('''TOTAL''', styleBH)

data = []

data.append([numero,alumno,b1,b2,b3,total])

#TABLE BodyText
styleN = styles["BodyText"]
styleN.aligment = TA_CENTER
styleN.fontSize = 7

high = 650
for student in students:
    this_student = [student['#'],student['name'],student['b1'],student['b2'],student['b3'],student['total']]
    data.append(this_student)
    high= high -  18
#TABLES writing
width, height = A4
table = Table(data, colWidths=[1.9 * cm, 7.5 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm, 1.9 * cm])
table.setStyle(TableStyle([
    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
    ('BOX', (0,0), (-1,-1), 0.25, colors.black),
]))

#PDF size
table.wrapOn(c, width, height)
table.drawOn(c,30,high)
c.showPage()

ajuste= 0.39
ancho =  700- (700*ajuste)
alto =  450 - (450*ajuste)

x= 80
y= 400
################################## FUNCTIONS ###################################################

def simpleText(canvas):
    from reportlab.lib.units import inch
    textobject = canvas.beginText()
    textobject.setTextOrigin(inch, 2.5*inch)
    textobject.setFont("Helvetica-Oblique", 14)
    for line in lyrics:
        textobject.textLine(line)
    textobject.setFillGray(0.4)

    canvas.drawText(textobject)


##############################################################################################################
#########    ##############################     GENERAL               ########################################
##############################################################################################################



#3 ########   ESTADISTICA DESCRIPTIVA GENERAL ##########




#6 ############## TOTAL, INGRESOS -EGRESOS ###############################

lyrics = [
"Total de ingresos",
"Para la entidad el total de ingresos puede ser una buena manera utilizar su comportamiento,",
"es por esto que se debe utilizar de buena manera en la estadistica descriptiva ",

]

simpleText(c)
c.drawImage(cwd + '\\total_ingresos_egresos.png', x,y,width=ancho,height=alto,mask='auto')
c.showPage()

#7 ############ MONTO OPERACIONES CREDITO - DEBITO #################

c.drawImage(cwd + '\\monto_credito_debito.PNG', x,y,width=ancho,height=alto,mask='auto')
c.showPage()

##############################################################################################################
#########    ##############################     CLUSTER               ########################################
##############################################################################################################



#4 ########## POBLACION POR CLUSTER ###############

c.drawImage(cwd + '\\poblacionxcluster.png', x,y,width=ancho,height=alto,mask='auto')

c.showPage()


#5 ########  GRAFICA CLUSTER debito ############

c.drawImage(cwd + '\\clusterdebito.png', x,y,width=ancho,height=alto,mask='auto')
c.showPage()



#8 ############## PATRIMONIO POR CLUSTER ############
c.drawImage(cwd + '\\patrimonio_cluster.PNG', x,y,width=ancho,height=alto,mask='auto')
c.showPage()

#9 ########### DISTRIBUCION OCUPACIONES #######
c.drawImage(cwd + '\\ocupaciones.png', x,y,width=ancho,height=alto,mask='auto')
c.showPage()

#10 ###  ACTIVIDADES  ######

c.drawImage(cwd + '\\actividades.png', x,y,width=ancho,height=alto,mask='auto')
c.showPage()


#11 ###  ESTADISTICA DESCRIPTIVA POR CLUSTER ######

##############################################################################################################
#########    ##############################     GUARDAR               ########################################
##############################################################################################################

c.save()
