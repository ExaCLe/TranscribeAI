import whisper
from rich import print as rprint


def transcribe_audio(path, model_name):
    rprint(f"[yellow]Loading model {model_name}...")
    model = whisper.load_model(model_name)
    rprint("[green]Model loaded successfully!")
    audio = whisper.load_audio(path)
    rprint("[yellow]Transcribing audio...")
    return model.transcribe(audio)


if __name__ == "__main__":
    print(transcribe_audio("audio.m4a", "tiny"))
