import os
import re
import pysrt
import logging
from time import sleep
from pathlib import Path
from pytube import YouTube
from rich.console import Console

logger = logging.getLogger(__name__)
console = Console()

# Create Captions Object that creates .srt and .txt file of youtube video
class Captions:
    def __init__(self, URL, verbose):
        # Only prints if verbose flag is set to True
        self.verboseprint = console.log if verbose else lambda *a, **k: None

        self.yt = YouTube(URL)
        self.video_path = os.getcwd() + "/clipbit/videos/{}".format(
            self.yt.title.lower().replace(" ", "_")
        )
        Path(self.video_path).mkdir(parents=True, exist_ok=True)
        self.verboseprint("Created new directory for video")
        sleep(1)

        self.srt_filename = self.create_srt()
        self.generate_script()

    def create_srt(self):
        """
        This creates the .srt file
        Parameters: None
        returns: .srt file path location
        """
        caption_dict = self.yt.captions.lang_code_index

        # Regex searches for keys that start with "en"
        self.verboseprint("Looking for English Captions")
        sleep(1)
        en_key = None
        for key in caption_dict.keys():
            if re.findall("^en.*", key):
                en_key = key
                break
        try:
            if en_key:
                self.verboseprint("[bold green]Found English subtitles")
                self.yt.captions[en_key].download("captions")
            elif caption_dict.get("a.en", None):
                self.verboseprint("[bold green]Found auto-generated captions")
                self.yt.captions["a.en"].download("captions")
                en_key = "a.en"
            else:
                logger.error(
                    "\033[91m\u2717 clipbit: error in retrieving caption file\033[0m"
                )
            sleep(1)

            os.rename(f"captions ({en_key}).srt", f"{self.video_path}/captions.srt")
            self.verboseprint("[bold green]Downloaded script.txt")
            sleep(1)

            return f"{self.video_path}/captions.srt"

        except Exception:
            logger.error(
                "\033[91m\u2717 clipbit: No captions associated with this video.\033[0m"
            )

    def generate_script(self):
        if self.srt_filename:
            srt_file = pysrt.open(self.srt_filename)
            text = ""
            for obj in srt_file:
                text += f"{obj.text} "

            with open(f"{self.video_path}/script.txt", "w+") as f:
                f.write(text)
            self.verboseprint("[bold green]Created captions.srt file")
        else:
            self.verboseprint(
                "[bold yellow]No .srt file created. Captions most likely not available"
            )
        sleep(1)
