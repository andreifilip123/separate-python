import os
import demucs.separate
import requests


def separate_song_parts(file_url: str, unique_id: str, model="htdemucs", jobs="1"):
    print(f"Separating song parts for {unique_id} with model {model} using {jobs} jobs")
    file_extension = file_url.split(".")[-1]

    output_path = f"downloads/{unique_id}/"

    file_path = f"downloads/{unique_id}.{file_extension}"

    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    # Download the file
    r = requests.get(file_url)
    with open(file_path, 'wb') as outfile:
        outfile.write(r.content)
    print("Downloaded the file locally")

    # Create an options array to pass to the separate function
    options = [
        "-n",
        model,
        "--mp3",
        "-j",
        jobs,
        "--two-stems",
        "vocals",
        file_path,
        "-o",
        output_path,
    ]

    if file_extension == "mp3":
        options.append("--mp3")

    demucs.separate.main(options)
    print("Separation complete")

    no_vocals = f"downloads/{unique_id}/htdemucs/{unique_id}/no_vocals.{file_extension}"
    vocals = f"downloads/{unique_id}/htdemucs/{unique_id}/vocals.{file_extension}"

    return {
        "no_vocals": no_vocals,
        "vocals": vocals,
    }
