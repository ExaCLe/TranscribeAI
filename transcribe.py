import os

import psutil
from PyInquirer import prompt
from rich import print as rprint

from analysis import transcribe_audio

models_and_ram = [("large", 10), ("medium", 5), ("small", 2), ("base", 1)]

whisper_model_options = [
    {
        'type': 'list',
        'name': 'model',
        'message': 'Select one model (larger models are more accurate but also need more time): ',
        'default': 'auto',
        'choices': [
            {
                'name': 'auto (best model possible will be chosen)',
                'value': 'auto'
            },
            {
                'name': 'tiny ~ 1GB',
                'value': 'tiny'
            },
            {
                'name': 'base ~ 1GB',
                'value': 'base'
            },
            {
                'name': 'small ~ 2GB',
                'value': 'small'
            },
            {
                'name': 'medium ~ 5GB',
                'value': 'medium'
            },
            {
                'name': 'large ~ 10GB',
                'value': 'large'
            },
        ],
    }
]


def make_transcription(path, model_name, output):
    print(path, model_name)
    rprint("[#00e0d7]Welcome to Transcribe AI![/#00e0d7]")

    path = get_audio_path(path)

    if model_name is None:
        model_name = get_model_name()

    try:
        transcription = transcribe_audio(path, model_name)
        rprint("[green bold]Transcription successful![/green bold]")

        save = should_save_model(output)
        if save:
            output = get_and_create_output(output)

            with open(output, "w") as f:
                f.write(transcription['text'])

            rprint(f"[green]Saved transcription to '{output}'[/green]")
        rprint("[gray]transcription[/gray]")
        rprint(f"[gray]{transcription['text']}[/gray]")

    except Exception as e:
        rprint("[red]Error:[red] " + str(e))


def get_and_create_output(output):
    while output == "":
        rprint("Please enter the path where you want to save the transcription (e.g. ./output.txt):")
        output = input()

    output_path = os.path.dirname(output)
    os.makedirs(output_path, exist_ok=True)

    return output


def should_save_model(output):
    if output == "":
        options = [{
            'type': 'confirm',
            'name': 'save',
            'message': 'You did not provide an output path. Do you want to save the transcription?',
            'default': True,
        }]
        save = prompt(options)['save']
    else:
        save = True
    return save


def get_model_name():
    model_name = prompt(whisper_model_options)['model']
    if model_name == "auto":
        rprint("[yellow]Choosing model automatically based on RAM...")
        ram = psutil.virtual_memory().total
        for model, required_ram in models_and_ram:
            if ram >= required_ram * 1024 ** 3:
                model_name = model
                break
    return model_name


def get_audio_path(path):
    while path == "":
        rprint("Please enter the path of the audio file you want to transcribe:")
        path = input()
    return path
