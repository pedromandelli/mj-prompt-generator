from django import forms


class UserInputForm(forms.Form):
    medium = forms.CharField(label='Tipo de imagem', max_length=100)
    scene_description = forms.CharField(label='Descrição da imagem', max_length=500)
    style = forms.CharField(label='Estilo e características', max_length=500)
