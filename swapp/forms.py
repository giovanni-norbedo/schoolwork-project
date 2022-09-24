from django import forms 
from .models import Ask, Reply, Bad, Chat, Solved, Yes
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as l

def val(value):
    if value > 10 or value < 6:
        raise ValidationError(
            l('Valutazione inesistente. Inserisci un valore da 6 a 10.'),
        )

class AskForm(forms.ModelForm):
    class Meta: 
        model = Ask 
        fields = ["coins", "title", "text", "file"]

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply 
        fields = ["text", "file"]
        
class BadForm(forms.ModelForm):
    class Meta:
        model = Bad
        fields = ["text"]

class YesForm(forms.ModelForm):
    evaluation = forms.IntegerField(label='Is this reply is awsome?<br>Vote from 6 to 10.', validators=[val])
    class Meta:
        model = Yes
        fields = ['evaluation']

class SolvedForm(forms.ModelForm):
    class Meta:
        model = Solved
        fields = ["text", 'coins_ask', 'coins_reply']

class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ["text"]
