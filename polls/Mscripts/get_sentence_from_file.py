import re

from django.core.files.storage import FileSystemStorage


def get_sentence_from_file(uploadedFile):
    fs = FileSystemStorage()
    name = fs.save(uploadedFile.name, uploadedFile)
    f = open(fs.path(name), 'rt', errors='ignore')
    sentenceRR = f.read()
    f.close()
    sentenceR = re.sub('@', '', sentenceRR)
    sentencee = re.sub('[uU][Ss][Ee][Rr]', '', sentenceR)
    sentenceee = re.sub('_', ' ', sentencee)
    sentenceeee = re.sub('-', ' ', sentenceee)
    sentenceeeee = re.sub('=', ' ', sentenceeee)
    sentenceeeeee = re.sub('%', ' ', sentenceeeee)
    sentenceeeeeee = re.sub('"', ' ', sentenceeeeee)
    sentence = re.sub("'", ' ', sentenceeeeeee)

    sepsent = re.findall('\d,+(.*)\n', sentence)
    return sepsent
