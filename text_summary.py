import torch
import logging
import colorama
import time
from rich.console import Console
from transformers import T5Tokenizer, T5ForConditionalGeneration

logger = logging.getLogger(__name__)
colorama.init()
console = Console()

# Returns content of the script file
def read_file(filepath):
    with open(filepath, "r") as f:
        file_obj = f.read()

    return file_obj


# Writes the final summary to summary.txt
def create_summary_file(filepath, summary):
    with open(filepath, "w+") as f:
        f.write(summary)


# Runs the model with the following parameters
def run_model(model, tokenized_text):
    summary_ids = model.generate(
        tokenized_text,
        num_beams=4,
        no_repeat_ngram_size=2,
        min_length=30,
        max_length=512,
        early_stopping=True,
    )

    return summary_ids


def summary(dirpath, verbose):
    """
    Abstractive text summarization
    :param text: body of text to be summarized
    :return: summarized version of original text
    """
    # Only prints if verbose flag is set to True
    verboseprint = console.log if verbose else lambda *a, **k: None

    model = T5ForConditionalGeneration.from_pretrained(
        "t5-small"
    )  # use pretrained model
    tokenizer = T5Tokenizer.from_pretrained("t5-small")  # use pretrained tokenizer
    device = torch.device("cpu")

    # Read captions from script.txt
    try:
        text = read_file(dirpath + "/script.txt")
    except:
        logging.info("\033[93m[\u21b3] Ignoring... no captions file\033[0m")
        return (None, None)

    # preprocessing
    clean_text = text.strip().replace("\n", "")
    t5_text = "summarize: " + clean_text  # define task

    # tokenizer
    tokenized_text = tokenizer.encode(t5_text, return_tensors="pt").to(device)
    total_tokens = len(tokenized_text[0])
    if total_tokens > 512:
        logging.error(
            u"\n\033[91m\u2717 Max token length exceeded: too many words!\033[0m"
        )
        return (None, None)

    # summmarize
    with console.status(
        "[bold magenta]Generating summary...", spinner="bouncingBar"
    ) as status:
        summary_ids = run_model(model, tokenized_text)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        create_summary_file(dirpath + "/summary.txt", summary)
        verboseprint("[bold green]Dumped summary to file\n")
        time.sleep(1)

    return (text, summary)


if __name__ == "__main__":
    pass
