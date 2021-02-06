#!/usr/bin/env python3

import click
import os
import sys
import logging
import colorama
from tabulate import tabulate

from script import Captions
from text_summary import summary as ts

logger = logging.getLogger(__name__)
colorama.init()


@click.command()
@click.option(
    "-s",
    "--summarize",
    prompt="\033[93m\u2192 Enter the YouTube link:\033[0m",
    help="Generates summary from the YouTube link.",
)
@click.option(
    "-v/-nv",
    "--verbose/--no-verbose",
    default=False,
    help="Verbose mode: shows progress bar and other information.",
)
@click.option(
    "-d/-c",
    "--detailed/--clean",
    default=False,
    help="Detailed mode: displays title, captions and summary in a table.",
)
def generate_summary(summarize, verbose, detailed):
    verboseprint = print if verbose else lambda *a, **k: None

    captions = Captions(summarize, verbose)
    if captions.srt_filename:
        final_summary = ts(captions.video_path, verbose)
        if final_summary:
            if detailed:
                tabulate_summary(final_summary, captions)
            else:
                print(f"\n{final_summary}\n")
            verboseprint(
                "\033[96m\u2192 Captions, Script and Summary are all available under videos/<video_name>/ directory.\033[0m"
            )


def tabulate_summary(summary, captions):
    pass
    # table = []
    # headers = ["VIDEO", "CAPTIONS", "SUMMARY"]
    # table.append([captions.video_path, captions.video_path + "/script.txt", captions.video_path + "/summary.txt"])
    # print(tabulate(table, headers, tablefmt="pretty"))


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
    print("\033[95m ██████╗██╗     ██╗██████╗ ██████╗ ██╗████████╗\033[0m")
    print("\033[95m██╔════╝██║     ██║██╔══██╗██╔══██╗██║╚══██╔══╝\033[0m")
    print("\033[95m██║     ██║     ██║██████╔╝██████╔╝██║   ██║   \033[0m")
    print("\033[95m██║     ██║     ██║██╔═══╝ ██╔══██╗██║   ██║   \033[0m")
    print("\033[95m╚██████╗███████╗██║██║     ██████╔╝██║   ██║   \033[0m")
    print("\033[95m ╚═════╝╚══════╝╚═╝╚═╝     ╚═════╝ ╚═╝   ╚═╝   \033[0m")
    print("\033[94mGenerate concise meaningful summaries of videos.\033[0m\n")


if __name__ == "__main__":
    welcome_message()
    generate_summary()
