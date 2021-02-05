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

#
    def create_srt(self):
        """
        This creates the .srt file
        Parameters: None
        returns: .srt file path location
        """
        caption_dict = self.yt.captions.lang_code_index

        # Regex searches for keys that start with "en"
        en_key = None
        for key in caption_dict.keys():
            if re.findall("^en.*", key):
                en_key = key
                break
        try:
            if en_key:
                self.yt.captions[en_key].download("captions")
            elif caption_dict.get("a.en", None):
                self.yt.captions["a.en"].download("captions")
                en_key = "a.en"
            else:
                logger.error("clipbit: error in downloading caption file")


            os.rename(f"captions ({en_key}).srt", f"{self.video_path}/captions.srt")
            return f"{self.video_path}/captions.srt"

        except Exception as e:
            logger.error(e)
            logger.error('clipbit: No captions associated with this video.')

    def generate_script(self):
        srt_file = pysrt.open(self.srt_filename)
        text = ""
        for obj in srt_file:
            text += f"{obj.text} "

        with open(f"{self.video_path}/script.txt", "w+") as f:
            f.write(text)
