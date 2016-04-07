from django import forms

from .models import *

class EditTicketStateForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ('t_state','t_usersolver',)

class AddingTicketActivityDescriptionForm(forms.ModelForm):

    class Meta:
        model = Activity
        fields = ('at_description',)