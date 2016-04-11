from django import forms

from .models import *

class EditTicketStateForm(forms.ModelForm):
    class Meta:
        CHOICES_STATE = (('Iniciado','Iniciado'),
                         ('Asignado','Asignado'),
                         ('En Proceso','En Proceso'),
                         ('En Espera','En Espera'),
                         ('Resuelto','Resuelto'),
                         ('Cerrado','Cerrado'),
                         ('Re-abierto','Re-abierto'))
        model = Ticket
        fields = ('t_state',)
        labels = {
            't_state': (''),
        }    
        widgets = {
            't_state': forms.Select(choices=CHOICES_STATE,attrs={'class':'form-control'}),
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