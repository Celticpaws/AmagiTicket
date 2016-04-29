from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from reportlab.lib.colors import pink, black, red, blue, green, gray, Color
from reportlab.lib.pagesizes import letter
from django.core.urlresolvers import reverse
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import *
from django.http import HttpResponse
from django.utils import timezone
from .models import *
from .forms import *
from datetime import datetime
import math

edef pageBrake(n):
    page = n/680
    return page

def drawBorder(p,j):
    p.setFillColor(gray)
    p.circle(50, j-5, 12, fill=1,stroke=False)
    p.circle(550, j-5, 12, fill=1,stroke=False)
    p.rect(50,j-17,500,24, fill=1,stroke=False)
    p.setFont("Helvetica", 14)
    p.setFillColor(black)

def ticket_printed(request,pk):
    userjob = UserProfile.get_jobtitle(request.user)
    userdepartment = UserProfile.get_department(request.user)
    try:
        ticketpk = Ticket.objects.get(pk=pk)
    except:
        ticketpk = None
    useraffected = UserProfile.get_UserProfile(ticketpk.t_useraffected)
    usersolver = UserProfile.get_UserProfile(ticketpk.t_usersolver)
    sla = (ticketpk.t_reportmadeon-timezone.now())+ticketpk.t_sla.ToDeltaTime()
    slahour = sla.seconds//3600
    slaminute = (sla.seconds //60)%60
    attacheds = Archive.archives_of_a_ticket(ticketpk)
    sons = Ticket.get_sons(ticketpk)
    activities = Activity.activities_of_a_ticket(ticketpk).order_by('at_date')

    lastactivity = Activity.last_modified(ticketpk)
    dateopen = Activity.date_of_event(ticketpk,'')
    datesolved = Activity.date_of_event(ticketpk,'Resuelto')
    dateclosed = Activity.date_of_event(ticketpk,'Cerrado')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = "filename='Reporte-Ticket"+str(ticketpk.t_id)+".pdf'"

    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response,bottomup=0,pagesize=letter)
    p.setFont("Helvetica-Bold", 18)
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    u = 10
    p.setFillColor(gray)
    p.circle(50, 50-5, 17, fill=1,stroke=False)
    p.rect(50,50-22,800,34, fill=1,stroke=False)
    p.setFillColor(black)
    p.drawString(50, 50, "Reporte - Ticket #"+str(ticketpk.t_id))
    p.setFont("Helvetica", 14)
    drawBorder(p,100)
    p.drawString(50, 100, "Resumen del ticket")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, 125, "Titulo del ticket:")
    p.drawString(70, 149, "Fecha de resolución:")
    p.drawString(70, 173, "Ultima modificación: ")
    p.setFont("Helvetica", 10)
    p.drawString(80, 137, ticketpk.t_title)
    p.drawString(80, 161, datesolved)
    p.drawString(80, 185, lastactivity)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(300, 125, "Fecha de apertura:")
    p.drawString(300, 149, "Fecha de cierre:")
    p.setFont("Helvetica", 10)
    p.drawString(310, 137, dateopen)
    p.drawString(310, 161, dateclosed)
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, 209,"Descripción: ")
    p.setFont("Helvetica", 10)
    textobject = p.beginText()
    textobject.setTextOrigin(75,221)
    textobject.setFont("Helvetica",10)
    j=0
    for line in ticketpk.t_description.split('\n') :
        if len(line)>90:
            i=0
            while i<len(line):
                if i+90 < len(line):
                    textobject.textLine(line[i:i+90])
                    i+=90
                else:
                    textobject.textLine(line[i:len(line)])
                    i = len(line)+1
            j+= len(line)/90
        else:
            textobject.textLine(line)
            j+=1
        if(pageBrake(j)>=1):
            p.showPage()
            j=20
    p.drawText(textobject)
    j= round(j)+1
    j = 233+12*j



    if(pageBrake(j+73)>=1):
        p.showPage()
        j=20

    drawBorder(p,j)
    p.setFont("Helvetica", 14)
    p.drawString(50, j, "Detalle del Usuario Afectado")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, j+25, "Gerencia:")
    p.drawString(70, j+49, "Departmento:")
    p.drawString(70, j+73, "Usuario final afectado: ")
    p.drawString(300, j+25, "Cuenta del usuario final afectado:")
    p.drawString(300, j+49, "Teléfono:")
    p.drawString(300, j+73, "Correo: ")
    p.setFont("Helvetica", 10)
    p.drawString(80, j+25+12, str(useraffected.u_management))
    p.drawString(80, j+49+12, str(useraffected.u_department))
    p.drawString(80, j+73+12, useraffected.u_user.get_full_name())
    p.drawString(310, j+25+12, str(useraffected.u_user.username))
    p.drawString(310, j+49+12, str(useraffected.u_phone))
    p.drawString(310, j+73+12, str(useraffected.u_user.email))

    j= j+73+36

    if(pageBrake(j+97)>=1):
        p.showPage()
        j=20

    p.setFont("Helvetica", 14)
    drawBorder(p,j)
    p.drawString(50, j, "Detalle del Ticket")
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, j+25, "Tipo:")
    p.drawString(70, j+49, "Categoria:")
    p.drawString(70, j+73, "Servicio afectado: ")
    p.drawString(70, j+97, "Servidor afectado: ")

    p.drawString(240, j+25, "Prioridad:")
    p.drawString(240, j+49, "Estado actual: ")
    p.drawString(240, j+73, "Grupo solucionador:")
    p.drawString(240, j+97, "Usuario solucionador asignado:")
    
    p.drawString(420, j+25, "Ticket reportado por: ")
    p.drawString(420, j+49, "Impacto: ")
    p.drawString(420, j+73, "SLA:")
    p.drawString(420, j+97, "Tiempo de vida: ")

    p.setFont("Helvetica", 10)
    if ticketpk.t_isincident:
        p.drawString(80, j+25+12, "Incidente")
    else:
        p.drawString(80, j+25+12, "Solicitud")   
    p.drawString(80, j+49+12, ticketpk.t_category)
    p.drawString(80, j+73+12, str(ticketpk.t_server))
    p.drawString(80, j+97+12, str(ticketpk.t_service))

    p.drawString(250, j+25+12, str(ticketpk.t_priority))
    p.drawString(250, j+49+12, ticketpk.t_state)
    p.drawString(250, j+73+12, str(ticketpk.t_department))
    if ticketpk.t_usersolver == None :
        p.drawString(250, j+97+12, "El ticket no ha sido asignado")
    else:
        p.drawString(250, j+97+12, ticketpk.t_usersolver.get_full_name())

    p.drawString(430, j+25+12, ticketpk.t_userreporter.get_full_name())
    p.drawString(430, j+49+12, str(ticketpk.t_impact))
    p.drawString(430, j+73+12, str(ticketpk.t_sla))
    p.drawString(430, j+97+12, ticketpk.life_spawn())
    j= j+97+36

    if(pageBrake(j)>=1):
        p.showPage()
        j=20

    drawBorder(p,j)
    p.setFont("Helvetica", 14)
    p.drawString(50, j, "Actividades del ticket")

    if len(activities) == 0:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "No hay actividades asociadas a este ticket ")
        j=j+25+24
    else:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "Tipo ")
        p.drawString(200, j+25, "Fecha")
        p.drawString(420, j+25, "Creada por")
        for activity in activities:
            p.setFont("Helvetica", 8)
            p.drawString(70, j+25+12, activity.at_tipe)
            p.drawString(200, j+25+12, activity.at_date.strftime("%d de %b del %Y a las %I:%M:%S %p"))
            p.drawString(420, j+25+12, activity.at_createdby.get_full_name())
            j = j+12
            if(pageBrake(j+12)>=1):
                p.showPage()
                j=20
        j=j+25+24

    drawBorder(p,j)
    p.setFont("Helvetica", 14)
    p.drawString(50, j, "Detalle Padre/Hijo")
    p.setFont("Helvetica-Bold", 10)
    if ticketpk.t_mother != None:
        p.drawString(70, j+25, "Padre: Ticket " + str(ticketpk.t_mother) )
        p.drawString(200, j+25,"Estado: "+ticketpk.t_mother.t_state)
        j=j+12
        if ticketpk.t_mother.t_usersolver == None:
            p.drawString(350, j+25,"Asignatario: Ticket no asignado")
        else:
            p.drawString(350, j+25,"Asignatario: "+ticketpk.t_mother.t_usersolver.get_full_name())
    else:    
        p.drawString(70, j+25, "Padre: El ticket no posee padre" )
    j=j+12

    if len(sons) == 0:
        p.drawString(70, j+25, " El ticket no posee ningun hijo ")
        j=j+24
    else:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "Ticket hijo # ")
        p.drawString(150, j+25, " Fecha")
        p.drawString(300, j+25, "Estado")
        p.drawString(420, j+25, "Asigantatio")

        for son in sons:
            p.setFont("Helvetica", 8)
            p.drawString(80, j+25+12, str(son))
            p.drawString(150, j+25+12, son.t_reportmadeon.strftime("%d de %b del %Y a las %I:%M:%S %p"))
            p.drawString(300, j+25+12, son.t_state)
            if son.t_usersolver == None:
                p.drawString(420, j+25+12, "Ticket no asignado")
            else:
                p.drawString(420, j+25+12, son.t_usersolver.get_full_name())
            j = j+12
            if(pageBrake(j)>=1):
                p.showPage()
                j=20
        j=j+25+24

    drawBorder(p,j)
    p.drawString(50, j, "Archivos adjuntos del ticket")

    if len(attacheds) == 0:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "No hay archivos adjuntos en este ticket ")
        j=j+25+24
    else:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(70, j+25, "Documento ")
        p.drawString(200, j+25, "Fecha")
        p.drawString(420, j+25, "Usuario")
        for attached in attacheds:
            p.setFont("Helvetica", 8)
            p.drawString(70, j+25+12, attached.a_name)
            p.drawString(200, j+25+12, attached.a_dateattached.strftime("%d de %b del %Y a las %I:%M:%S %p"))
            p.drawString(420, j+25+12, attached.a_userattacher.get_full_name())
            j = j+12
            if(pageBrake(j)>=1):
                p.showPage()
                j=20
        j=j+25+24

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response