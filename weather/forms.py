from django import forms

class CityForm(forms.Form):
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            "placeholder": "Enter city name (e.g., Delhi, London)",
            "class": "form-control"
        })
    )
