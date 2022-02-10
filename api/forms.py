from django import forms

class MyValidationForm(forms.Form):
    buyer_id = forms.IntegerField()
    plant_id = forms.IntegerField()
    seller_id = forms.IntegerField()