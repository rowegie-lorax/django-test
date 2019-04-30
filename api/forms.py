from django import forms
from django.http import JsonResponse
from api.models import FileDirectory


class DocumentForm(forms.ModelForm):
    class Meta:
        model = FileDirectory
        fields = ('description', 'document', )
