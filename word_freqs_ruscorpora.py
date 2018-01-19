#!/usr/bin/env python3
"""Tool for counting words

Usage:
    word_freqs.py <input> <output>
"""

import conllu.parser
from collections import defaultdict
from docopt import docopt


def count_words(corpus):
    count = defaultdict(lambda: {'documents': 0, 'total': 0})
    for sentence in corpus:
        words_in_sentence = set()
        for word in sentence:
            lemma = word['lemma']
            if lemma not in words_in_sentence:
                count[lemma]['documents'] += 1
                words_in_sentence.add(lemma)
            count[lemma]['total'] += 1
    return count


def write_counts(filename, count):
    with open(filename, 'w') as f:
        for word, count in count.items():
            f.write(f"{count['total']}\t{count['documents']}\tu'{word}'\n")


def main():
    args = docopt(__doc__)
    text = open(args['<input>']).read()
    corpus = conllu.parser.parse(text)
    count = count_words(corpus)
    write_counts(filename=args['<output>'], count=count)


if __name__ == '__main__':
    main()
