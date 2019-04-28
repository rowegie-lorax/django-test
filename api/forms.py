from django import forms

from api.models import FileDirectory


class DocumentForm(forms.ModelForm):
    class Meta:
        model = FileDirectory
        fields = ('description', 'document', )