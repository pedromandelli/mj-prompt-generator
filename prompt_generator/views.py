from django.shortcuts import render

from django_app.forms import UserInputForm
from transformers import AutoTokenizer, AutoModelWithLMHead

tokenizer = AutoTokenizer.from_pretrained("succinctly/text2image-prompt-generator")
model = AutoModelWithLMHead.from_pretrained("succinctly/text2image-prompt-generator")


def generate(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            prompts = generate(user_input)  # This function should return a list of prompts
            return render(request, 'prompt_generator/result.html', {'prompts': prompts})
    else:
        form = UserInputForm()
    return render(request, 'prompt_generator/input.html', {'form': form})

