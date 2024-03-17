import logging
import shutil

import demucs.separate
from botocore.exceptions import ClientError

from .aws_wrapper import download_file, upload_file_obj


def separate_song_parts(file_name, file_extension, model="htdemucs", jobs="1"):
    print(f"Separating song parts for {file_name} with model {model} using {jobs} jobs")
    download_file(file_name)

    path = f"downloads/{file_name}/original.{file_extension}"
    output_path = f"downloads/{file_name}/"

    demucs.separate.main(
        [
            "-n",
            model,
            "--mp3",
            "-j",
            jobs,
            "--two-stems",
            "vocals",
            path,
            "-o",
            output_path,
        ]
    )
    print("Separation complete")

    no_vocals = f"downloads/{file_name}/htdemucs/original/no_vocals.{file_extension}"
    vocals = f"downloads/{file_name}/htdemucs/original/vocals.{file_extension}"

    with open(no_vocals, "rb") as data:
        try:
            upload_file_obj(data, f"{file_name}/no_vocals.{file_extension}")
        except ClientError as e:
            logging.error(e)

    with open(vocals, "rb") as data:
        try:
            upload_file_obj(data, f"{file_name}/vocals.{file_extension}")
        except ClientError as e:
            logging.error(e)

    # Clean up
    print("Cleaning up")
    shutil.rmtree(f"downloads/{file_name}", ignore_errors=True)
