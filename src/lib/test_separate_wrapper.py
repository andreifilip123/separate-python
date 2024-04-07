import os
import unittest
from unittest.mock import patch

from .separate_wrapper import _download_file, separate_song_parts


class TestSeparateWrapper(unittest.TestCase):
    def test_download_file(self):
        file_url = "https://example.com/file.txt"
        unique_id = "12345"

        # Mock the requests.get function to return a response with content
        with patch("requests.get") as mock_get:
            mock_get.return_value.content = b"File content"

            # Call the function
            file_extension, output_path, file_path = _download_file(file_url, unique_id)

            # Assert that the file path is correct
            expected_file_path = f"downloads/{unique_id}.txt"
            expected_file_extension = "txt"
            expected_output_path = f"downloads/{unique_id}/"
            self.assertEqual(file_path, expected_file_path)
            self.assertEqual(file_extension, expected_file_extension)
            self.assertEqual(output_path, expected_output_path)

            # Assert that the file is downloaded and saved correctly
            self.assertTrue(os.path.exists(expected_file_path))
            with open(expected_file_path, "rb") as file:
                self.assertEqual(file.read(), b"File content")

        # Assert that the "downloads" directory is created
        self.assertTrue(os.path.exists("downloads"))

    @patch("src.lib.separate_wrapper.os.path.exists")
    @patch("src.lib.separate_wrapper.os.makedirs")
    @patch("src.lib.separate_wrapper.requests.get")
    @patch("src.lib.separate_wrapper.open")
    @patch("src.lib.separate_wrapper.demucs.separate.main")
    def test_separate_song_parts(
        self, mock_separate, mock_open, mock_get, mock_makedirs, mock_exists
    ):
        # Setup the mocks
        mock_exists.return_value = False
        # Test case 1: Separating song parts with a valid file URL
        file_url = "https://example.com/song.mp3"
        unique_id = "12345"
        model = "htdemucs"
        jobs = "1"

        result = separate_song_parts(file_url, unique_id, model, jobs)

        mock_makedirs.assert_called_once_with("downloads")
        mock_get.assert_called_once_with(file_url)
        mock_open.assert_called_once_with(f"downloads/{unique_id}.mp3", "wb")
        mock_separate.assert_called_once_with(
            [
                "-n",
                model,
                "-j",
                jobs,
                "--two-stems",
                "vocals",
                f"downloads/{unique_id}.mp3",
                "-o",
                f"downloads/{unique_id}/",
                "--mp3",
            ]
        )

        self.assertEqual(
            result["no_vocals"],
            f"downloads/{unique_id}/htdemucs/{unique_id}/no_vocals.mp3",
        )
        self.assertEqual(
            result["vocals"], f"downloads/{unique_id}/htdemucs/{unique_id}/vocals.mp3"
        )


if __name__ == "__main__":
    unittest.main()
