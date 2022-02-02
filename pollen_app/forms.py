from django import forms
from pollen_app.models import FLOWER,SEX

class addPlantForm(forms.Form):
    nepenthes = forms.CharField(max_length=500,required=True)
    flower_status = forms.ChoiceField(choices=FLOWER.choices, widget=forms.RadioSelect, required=True)
    sex = forms.ChoiceField(choices=SEX.choices, widget=forms.RadioSelect,required=True)
    image = forms.ImageField(required=True)

