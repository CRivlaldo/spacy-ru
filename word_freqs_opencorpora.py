#!/usr/bin/env python3
"""Tool for counting words in opencorpora

Usage:
    word_freqs_opencorpora.py <input> <output>
"""
import xml
import spacy
from collections import defaultdict
from docopt import docopt


def count_words(corpus):
    count = defaultdict(lambda: {'documents': 0, 'total': 0})
    current_text_words = set()
    nlp = spacy.load('ru')
    source = False

    def start_element(name, attrs):
        nonlocal source
        if name == 'source':
            source = True

    def end_element(name):
        nonlocal source
        if name == 'source':
            source = False
        elif name == 'text':
            current_text_words = set()

    def char_data(data):
        nonlocal current_text_words
        data = data.strip()
        if data and source:
            sentence = set(str(word) for word in nlp(data))
            for word in sentence:
                if word not in current_text_words:
                    count[word]['documents'] += 1
                count[word]['total'] += 1
            current_text_words.update(sentence)

    p = xml.parsers.expat.ParserCreate()
    p.StartElementHandler = start_element
    p.EndElementHandler = end_element
    p.CharacterDataHandler = char_data
    p.Parse(corpus)
    return count


def write_counts(filename, count):
    with open(filename, 'w') as f:
        for word, count in count.items():
            f.write(f"{count['total']}\t{count['documents']}\t{word}\n")


def main():
    args = docopt(__doc__)
    text = open(args['<input>']).read()
    count = count_words(text)
    write_counts(filename=args['<output>'], count=count)


if __name__ == '__main__':
    main()
