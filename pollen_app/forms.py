from django.forms import ModelForm
from pollen_app.models import Nepenthes


class addPlantForm(ModelForm):
    class Meta:
        model = Nepenthes
        fields = ['name', 'description', 'flower', 'sex',"shipping","image"]



