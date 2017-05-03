#!/usr/bin/env python3
"""A tool to form input for brown clustering from conllu corpus.

Usage:
    brown_input.py <input> <output>
"""

import conllu.parser
from docopt import docopt


def write_output(filename, corpus):
    with open(filename, 'w') as f:
        for sentence in corpus:
            for word in sentence:
                f.write(word['lemma'])
                f.write(' ')
            f.write('\n')


def main():
    args = docopt(__doc__)
    text = open(args['<input>']).read()
    corpus = conllu.parser.parse(text)
    write_output(filename=args['<output>'], corpus=corpus)


if __name__ == '__main__':
    main()
