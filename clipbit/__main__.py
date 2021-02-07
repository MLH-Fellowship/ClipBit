#!/usr/bin/env python3

import click
import os
import sys
import logging
import colorama
from rich.console import Console
from rich.table import Table

from clipbit.script import Captions
from clipbit.text_summary import summary as ts

logger = logging.getLogger(__name__)
colorama.init()
console = Console()


@click.command()
@click.option(
    "-s",
    "--summarize",
    prompt="\033[93mEnter the YouTube link:\033[0m",
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
        script, final_summary = ts(captions.video_path, verbose)
        if final_summary:
            if detailed:
                pp_print(script, final_summary, captions)
            else:
                print(f"\n{final_summary}\n")
            verboseprint(
                "\033[96m\u2192 Captions, Script and Summary are all available under videos/<video_name>/ directory.\033[0m"
            )


# Pretty prints the results
def pp_print(script, summary, captions):
    """
    OPTIONAL
    Pretty prints filename, script and summar.
    :param summary: final generated summary from the NLP model
    :param captions: script.Captions object

    """
    table = Table(show_header=True, header_style="bold red")
    table.add_column("VIDEO", style="dim", width=12, justify="center")
    table.add_column("CAPTIONS", style="dim", justify="center")
    table.add_column("SUMMARY", style="dim", justify="center")
    table.add_row(captions.yt.title, script, summary)

    console.print(table)


# Returns the size of the terminal
def get_terminal_size():
    rows, columns = os.popen("stty size", "r").read().split()
    return int(rows), int(columns)


# Displays a simple progress bar
def display_progress_bar(bytes_received, filesize, ch="█", scale=0.55):
    """
    OPTIONAL
    Creates and displays a simple progress bar.
    :param bytes_received: bytes successfully received
    :param filesize: total filesize in bytes
    :param scale: scaling coefficient for the loading bar

    """
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
    """
    callback function for pytube to use to display the bar
    :param stream: pytube.YouTube.stream object
    :param chunk: chuck of bytes
    :param bytes_remaining: bytes left to download

    """
    filesize = stream.filesize
    bytes_received = filesize - bytes_remaining
    display_progress_bar(bytes_received, filesize)


def main():
    os.system("clear")
    print("\033[96m ██████╗██╗     ██╗██████╗ ██████╗ ██╗████████╗\033[0m")
    print("\033[96m██╔════╝██║     ██║██╔══██╗██╔══██╗██║╚══██╔══╝\033[0m")
    print("\033[96m██║     ██║     ██║██████╔╝██████╔╝██║   ██║   \033[0m")
    print("\033[96m██║     ██║     ██║██╔═══╝ ██╔══██╗██║   ██║   \033[0m")
    print("\033[96m╚██████╗███████╗██║██║     ██████╔╝██║   ██║   \033[0m")
    print("\033[96m ╚═════╝╚══════╝╚═╝╚═╝     ╚═════╝ ╚═╝   ╚═╝   \033[0m")
    print("\033[94mGenerate concise meaningful summaries of videos.\033[0m\n")
    generate_summary()


if __name__ == "__main__":
    main()
