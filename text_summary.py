import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

model = T5ForConditionalGeneration.from_pretrained('t5-small') # use pretrained model
tokenizer = T5Tokenizer.from_pretrained('t5-small') # use pretrained tokenizer
device = torch.device('cpu')


def text_summary(text):
    '''
    Abstractive text summarization
    :param text: body of text to be summarized
    :return: summarized version of original text
    '''
    # preprocessing
    clean_text = text.strp().replace("\n","")
    t5_text = "summarize: " + clean_text # define task

    #tokenizer
    tokenized_text = tokenizer.encode(t5_text, return_tensors="pt").to(device)
    # summmarize
    summary_ids = model.generate(tokenized_text,
                                 num_beams=4,
                                 no_repeat_ngram_size=2,
                                 min_length=30,
                                 max_length=100,
                                 early_stopping=True)

    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary
