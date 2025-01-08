from django.forms import ModelForm
from .models import Exam

class RoomForm(ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'
        