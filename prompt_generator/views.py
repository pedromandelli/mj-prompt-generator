from django.shortcuts import render

from django_app.forms import UserInputForm
from transformers import AutoTokenizer, AutoModelWithLMHead, pipeline, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("succinctly/text2image-prompt-generator")
model = AutoModelWithLMHead.from_pretrained("succinctly/text2image-prompt-generator")


def generate(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            medium = form.cleaned_data['medium']
            scene_description = form.cleaned_data['scene_description']
            style = form.cleaned_data['style']
            prompt = f"{medium} de {scene_description}, {style}"
            english_prompt = translate_to_english(prompt)
            prompts = generate_prompt(english_prompt)

            return render(request, 'prompt_generator/result.html', {'prompts': prompts})
        else:
            return render(request, 'prompt_generator/input.html', {'form': form})
    else:
        form = UserInputForm()
        return render(request, 'prompt_generator/input.html', {'form': form})


def generate_prompt(user_input):
    prompt_generator = pipeline('text-generation', model='succinctly/text2image-prompt-generator')
    prompts = prompt_generator(user_input, max_length=300, temperature=0.7, top_k=50, num_return_sequences=3)
    return prompts


def translate_text(user_input, source_lang, target_lang):
    model_name = f"unicamp-dl/translation-{source_lang}-{target_lang}-t5"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    translation_pipeline = pipeline('text2text-generation', model=model, tokenizer=tokenizer)
    translated_text = translation_pipeline(user_input)
    return translated_text[0]['generated_text']


def translate_to_english(user_input):
    return translate_text(user_input, "pt", "en")


def translate_to_portuguese(user_input):
    return translate_text(user_input, "en", "pt")
