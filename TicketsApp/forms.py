from django import forms

from .models import *

class EditTicketStateForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('t_state',)
        labels = {
            't_state': (''),
        }    
        widgets = {
            't_state': forms.Select(attrs={'class':'form-control'}),
        }

class AddArchiveForm(forms.ModelForm):
    class Meta:
        model = Archive
        fields = ('a_name','a_route','a_description')
        labels = {
            'a_name': ('Nombre del documento a adjuntar'),
            'a_route': ('Ruta del documento'),
            'a_description': ('Descripción del documento a adjuntar'),
        }   
        widgets = {
            'a_name': forms.TextInput(attrs={'class':'form-control'}),
            'a_description': forms.Textarea(attrs={'class':'form-control'}),
            'a_route': forms.FileInput(attrs={'class':'btn btn-primary'}),
            
        }

class EditScaleForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('t_priority',)
        labels = {
            't_priority': (''),
        }    
        widgets = {
            't_priority': forms.NumberInput(attrs={'class':'form-control'}),
        }

class TransferForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ('at_description',)
        labels = {
            'at_description': (''),
        }    
        widgets = {
            'at_description': forms.Textarea(attrs={'class':'form-control'}),
        }

class CreateTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ('t_priority','t_mother','t_useraffected','t_category','t_title','t_description',
            't_server','t_service','t_impact','t_priority','t_sla','t_department',)

        labels = {
            't_mother': ('Ticket Padre:'),
            't_useraffected': ('Usuario afectado:'),
            't_category': ('Categoria:'),
            't_title': ('Titulo:'),
            't_description': ('Descripción:'),
            't_server': ('Servidor afectado:'),
            't_service': ('Servicio afectado:'),
            't_impact': ('Impacto:'),
            't_priority': ('Prioridad:'),
            't_sla': ('Tiempo de respuesta (SLA):'),
            't_department': ('Departamento solucionador:'),
        }    

        widgets = {
            't_mother': forms.Select(attrs={'class':'form-control'}),
            't_useraffected': forms.Select(attrs={'class':'form-control'}),
            't_category': forms.Select(attrs={'class':'form-control'}),
            't_title': forms.TextInput(attrs={'class':'form-control'}),
            't_description': forms.Textarea(attrs={'class':'form-control'}),
            't_server': forms.Select(attrs={'class':'form-control'}),
            't_service': forms.Select(attrs={'class':'form-control'}),
            't_impact':  forms.NumberInput(attrs={'class':'form-control'}),
            't_priority':  forms.NumberInput(attrs={'class':'form-control'}),
            't_sla': forms.Select(attrs={'class':'form-control'}),
            't_department': forms.Select(attrs={'class':'form-control'}),
        }

class AsignateSolverTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields =('t_usersolver',)
        label = {'t_usersolver':('Usuario Solucionador')}
        widgets = {'t_usersolver':forms.Select(attrs={'class':'form-control'})}

class CloseTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields =('t_issolved',)
        label = {'t_issolved':('Ticket resuelto')}
        widgets = {'t_issolved':forms.CheckboxInput(attrs={'class':'form-control'})}