#!/usr/bin/env python3

import click
import os
import sys
import logging

from script import Captions

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "-s",
    "--summarize",
    prompt="Enter the YouTube link:",
    help="Generates summary from the YouTube link.",
)
@click.option(
    "-v/-nv",
    "--verbose/--no-verbose",
    default=False,
    help="Verbose mode: shows progress bar and other information.",
)
def generate_summary(summarize, verbose):
    captions_obj = Captions(summarize)

    # TO-DO
    # captions_obj.video_path + "/script.txt" is the path to the combined script.
    # import your file and then
    # call your NLP model function here.


# Returns the size of the terminal
def get_terminal_size():
    rows, columns = os.popen("stty size", "r").read().split()
    return int(rows), int(columns)


# Displays a simple progress bar
def display_progress_bar(bytes_received, filesize, ch="█", scale=0.55):
    _, columns = get_terminal_size()
    max_width = int(columns * scale)

    filled = int(round(max_width * bytes_received / float(filesize)))
    remaining = max_width - filled
    bar = ch * filled + " " * remaining
    percent = round(100.0 * bytes_received / float(filesize), 1)
    text = " ↳ |{bar}| {percent}%\r".format(bar=bar, percent=percent)
    sys.stdout.write(text)
    sys.stdout.flush()


# On download progress callback function
def on_progress(stream, chunk, bytes_remaining):
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)


def welcome_message():
    os.system("clear")
    print(" ██████╗██╗     ██╗██████╗ ██████╗ ██╗████████╗")
    print("██╔════╝██║     ██║██╔══██╗██╔══██╗██║╚══██╔══╝")
    print("██║     ██║     ██║██████╔╝██████╔╝██║   ██║   ")
    print("██║     ██║     ██║██╔═══╝ ██╔══██╗██║   ██║   ")
    print("╚██████╗███████╗██║██║     ██████╔╝██║   ██║   ")
    print(" ╚═════╝╚══════╝╚═╝╚═╝     ╚═════╝ ╚═╝   ╚═╝   \n")
    print("Generate concise meaningful summaries of videos.\n")


if __name__ == "__main__":
    welcome_message()
    generate_summary()
