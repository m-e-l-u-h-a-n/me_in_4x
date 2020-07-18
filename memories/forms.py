from .models import Memory, Files
from django import forms


class MemoryAddForm(forms.ModelForm):
    class Meta:
        model = Memory
        exclude = ('owner',)


class FileForm(forms.ModelForm):
    class Meta:
        model = Files
        fields = ('file',)
