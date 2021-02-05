import os
import re
import pysrt
import logging
from pathlib import Path
from pytube import YouTube

logger = logging.getLogger(__name__)

# Create Captions Object that creates .srt and .txt file of youtube video
class Captions:
    def __init__(self, URL):
        self.yt = YouTube(URL)
        self.video_path = os.getcwd() + "/videos/{}".format(
            self.yt.title.lower().replace(" ", "_")
        )
        Path(self.video_path).mkdir(parents=True, exist_ok=True)
        self.srt_filename = self.create_srt()
        self.generate_script()

# This creates the .srt file and returns the file path location
    def create_srt(self):
        try:
            caption_dict = self.yt.captions.lang_code_index

        except Exception as e:
            logger.error(e)
            logger.error("clipbit: error in downloading captions.")

# Caption_dict is a dictionary and were looking for a key that containts 'en'
        en_key = None
        for key in caption_dict.keys():
            if re.findall("^en.*", key):
                en_key = key
                break

        if en_key:
            self.yt.captions[en_key].download("captions")
        elif caption_dict.get("a.en", None):
            self.yt.captions["a.en"].download("captions")
            en_key = "a.en"
        else:
            logger.error("clipbit: error in downloading caption file")

        os.rename(f"captions ({en_key}).srt", f"{self.video_path}/captions.srt")
        return f"{self.video_path}/captions.srt"

    def generate_script(self):
        srt_file = pysrt.open(self.srt_filename)
        text = ""
        for obj in srt_file:
            text += f"{obj.text} "

        with open(f"{self.video_path}/script.txt", "w+") as f:
            f.write(text)
