from django import forms

class ValveForm(forms.Form):
    
    open_input = forms.IntegerField(min_value=0, max_value=100, widget = forms.fields.NumberInput(attrs={'id': 'id-open-input'}))
    min_temp = forms.IntegerField(min_value=7, max_value=28, widget=forms.fields.NumberInput(attrs={'id': 'id-min-temp-input'}))
    max_temp = forms.IntegerField(min_value=7, max_value=28, widget=forms.fields.NumberInput(attrs={'id': 'id-max-temp-input'}))

    # open_input = section.find_element_by_css_selector("input#id-open-input")
#     max_temp = section.find_element_by_css_selector("input#id-max-temp-input")
#     min_temp = section.find_element_by_css_selector("input#id-min-temp-input")
#     button = section.find_element_by_css_selector('input[type="submit"]')

