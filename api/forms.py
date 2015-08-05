from django import forms

class ValveForm(forms.Form):

    house_code = forms.CharField(widget=forms.fields.TextInput(attrs={'id': 'id-house-code-input'}))
    open = forms.CharField(widget=forms.fields.TextInput(attrs={'id': 'id-open-input'}))
