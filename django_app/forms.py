from django import forms


class UserInputForm(forms.Form):
    input_text = forms.CharField(widget=forms.Textarea)
