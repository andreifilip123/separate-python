from os.path import join

import demucs.separate


def separate_song_parts(path, model="htdemucs", jobs="1"):
    demucs.separate.main(
        ["-n", model, "--mp3", "-j", jobs, "--two-stems", "vocals", join("../", path)]
    )
