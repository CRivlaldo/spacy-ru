#!/usr/bin/env python3
"""A tool to form input for brown clustering from opencorpora

Usage:
brown_input_opencorpora.py <input> <output>
"""
import xml
import spacy
from docopt import docopt


def prepare(filename_out, corpus):
    with open(filename_out, 'w') as f:
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

        def char_data(data):
            data = data.strip()
            if data and source:
                sentence = list(str(word) for word in nlp(data))
                f.writelines([' '.join(sentence) + '\n'])

        p = xml.parsers.expat.ParserCreate()
        p.StartElementHandler = start_element
        p.EndElementHandler = end_element
        p.CharacterDataHandler = char_data
        p.Parse(corpus)


def main():
    args = docopt(__doc__)
    corpus = open(args['<input>']).read()
    prepare(filename_out=args['<output>'], corpus=corpus)


if __name__ == '__main__':
    main()
