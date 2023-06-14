from django.shortcuts import render

from django_app.forms import UserInputForm
from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline


tokenizer = AutoTokenizer.from_pretrained("succinctly/text2image-prompt-generator")
model = AutoModelWithLMHead.from_pretrained("succinctly/text2image-prompt-generator")


def generate(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.cleaned_data['user_input']
            prompts = generate_prompt(user_input)  # This function should return a list of prompts
            return render(request, 'prompt_generator/result.html', {'prompts': prompts})
    else:
        form = UserInputForm()
    return render(request, 'prompt_generator/input.html', {'form': form})


def generate_prompt(user_input):
    prompt_generator = pipeline('text-generation', model='succinctly/text2image-prompt-generator')
    prompts = prompt_generator(user_input, num_return_sequences=5)
    return prompts
