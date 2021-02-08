![Clipbit Logo](media/clipbit_logo.png)

![License](https://img.shields.io/pypi/l/clipbit?style=for-the-badge)
![PyPi Version](https://img.shields.io/pypi/v/clipbit?style=for-the-badge)
![Python Versions](https://img.shields.io/pypi/pyversions/clipbit?style=for-the-badge)
![PyPi Format](https://img.shields.io/pypi/format/clipbit?style=for-the-badge)
![Top Language](https://img.shields.io/github/languages/top/MLH-Fellowship/ClipBit?style=for-the-badge)
![Code Size](https://img.shields.io/github/languages/code-size/MLH-Fellowship/ClipBit?style=for-the-badge)
![Stars](https://img.shields.io/github/stars/MLH-Fellowship/ClipBit?style=for-the-badge)
![Forks](https://img.shields.io/github/forks/MLH-Fellowship/ClipBit?style=for-the-badge)
![Issues](https://img.shields.io/github/issues/MLH-Fellowship/ClipBit?style=for-the-badge)
![Activity](https://img.shields.io/github/commit-activity/w/MLH-Fellowship/ClipBit?style=for-the-badge)

## Introduction

[ClipBit](https://pypi.org/project/clipbit/1.0.0/) is a CLI tool developed to generate an abstractive text summary of youtube videos. All you need to provide is a link to a Youtube
video of your choice and the program will give a text summary.

## Installation
```
pip install clipbit
```

## Basic Usage
To know more about the program and the flags available, run the help command by running `clipbit --help`.
![clipbit_help](media/clipbit.png)

To summarize a youtube video, grab the link and feed to the CLI program as demonstrated in the gif below
![ClipBit in action](media/clipbit.gif)

## Inspiration
Often times, we might find videos that we don't have the time to watch from end-to-end or we would wish to only get a summary of the important points in it, and leave out the rest. Our purpose with ClipBit was to create a small, simple CLI program that could generate a concise summary of things in a video using the power of Natural Language Processing. The hope was to have an easy and accessible way to get those summaries and automate yet another mundane part of our lives.

## What it does
It generates summaries of YouTube videos by extracting the captions (English or auto-generated), compiling them into a chunk and getting a small yet meaningful summary from that chunk of text.

## How we built it
- **Click** for CLI
- **pytube** to extract captions from any YouTube video via it's link
- **pysrt** to compile the captions from a `.srt` file
- **pytorch** for a pre-trained NLP model to generate a summary from the captions.
- **rich** to format and pretty print everything

## Challenges we ran into
- In the case that a YouTube video does not have captions of any sort, we had to look for speech-to-text libraries to generate the text. At first, we struggled with setting up Google Speech-To-Text and due to it's limited free usage, we tried relying on other open source libraries like `deepspeech`. However, the results weren't acceptable and figuring out this part was the most time consuming.
- We tried to incorporate loading bars and animations into the CLI for the whole program but struggled to do so. We had to resort to using intermittent loading animations since we could not set-up any way of measuring progress of all the tasks in the project.
- The NLP Model has a limitation of 512 Tokens which prevents us from giving it large amounts of text (long videos). This limits what our project can do and how realistic it would be to use it. This is something we would really like to work around/fix.

## Accomplishments we're proud of
- Despite the struggles, we managed to get a working software made on time.
- We managed to have a relatively clean repository with good practices.
- The program is easy to install and run, which makes it an extremely practical day-to-day choice.
- The overall structure and potential of the project makes it something that could be expanded and improved upon by other contributors and eventually, be something that people could actually use in their daily lives.

## What we learned
- Using `Click` to make clean, minimal CLIs - animating, color coding and pretty-printing.
- Experiencing using NLP via `pytorch` - what they can do, their limitations and practical use cases.
- Defining scope of a project, planning it and completing it on time.
- Having to work with each other across different time-zones.

## Future add-ons

1. Generate summaries for videos with no captions.
2. Generate summaries for longer videos exceeding 1 hour.
3. Workaround NLP model limit of 512 Tokens.
4. GUI or web-app

## Authors

Meet the ClipBit team
1. [Miguel Guardia](https://github.com/Miguel-Enrique13)
2. [Sarthak Khattar](https://github.com/m0mosenpai)
3. [Kimaru Thagana](https://github.com/KimaruThagna)

## License 
![License](https://img.shields.io/pypi/l/clipbit?style=for-the-badge) <br>
ClipBit is free and open source under the MIT License.

