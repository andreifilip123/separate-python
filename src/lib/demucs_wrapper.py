import demucs.separate

from .aws_wrapper import download_file


def separate_song_parts(file_name, file_extension, model="htdemucs", jobs="1"):
    print(f"Separating song parts {file_name} with model {model} using {jobs} jobs")
    download_file(file_name)

    path = f"downloads/{file_name}.{file_extension}"

    demucs.separate.main(
        ["-n", model, "--mp3", "-j", jobs, "--two-stems", "vocals", path]
    )
