#!/usr/bin/python
import re
import collections
import string


def all_pairs(text,
              forward=float("inf"),
              alltext=False,
              ignoreOrder=False
              ):
    """
    Возвращает отсортированный список пар с заданными характеристиками.

    Аргументы:
    text -- исходный текст
    forward -- длина заглядывания вперёд (default INF)
    alltext -- игнорирование разбиения на предложения (default False)
    ignoreOrder -- игнорирование порядка слов (default False)
    """
    pairs = {}
    for s in sentences(text, alltext):
        ws = words(s)
        for a in range(0, len(ws)):
            for b in range(a+1, min(a+forward+1, len(ws))):
                w = ws[a]
                g = ws[b]
                if w != '' and g != '' and w != g:
                    match1 = (w, g)
                    match2 = (g, w)
                    if match1 in pairs:
                        pairs[match1] += 1
                    elif match2 in pairs and ignoreOrder:
                        pairs[match2] += 1
                    else:
                        pairs[match1] = 1
    return sorted(pairs.items(), key=lambda elem: -elem[1])


def words(sentence):
    """
    Возвращает массив непустых строк из разбиения sentence по пробелам
    """
    return list(filter(lambda x: x != '', sentence.split(' ')))


def sentences(text, alltext=False):
    """
    Возвращает список предложений исходного текста,
    Удаляя все не-буквы и лишние пробельные символы.

    Аргументы:
    alltext -- вернуть список из 1 элемента (исходного текста) (default False)
    """
    sents = []
    raw_sentences = []
    dec = r'[.!;?…]'

    if alltext:
        raw_sentences.append(text)
    else:
        raw_sentences = re.split(dec, text)

    de = r'[.'
    for c in string.punctuation:
        de += '\\'+c
    de += r'\d]+|[^\s|\w]+'


    for sent in raw_sentences:
        sent = re.sub(de, '', sent)
        sent = re.sub('[\s]+', ' ', sent)
        if sent != '':
            sents.append(sent)
    return sents


def bigramms(text):
    """
    Строит пары подряд идущих слов с учётом границ предложений.
    """
    pairs_counters = {}
    for s in sentences(text):
        ws = words(s)
        for i in range(len(ws)-1):
            if ws[i] in pairs_counters:
                pairs_counters[ws[i]][ws[i+1]] += 1
            else:
                pairs_counters[ws[i]] = collections.Counter()
                pairs_counters[ws[i]][ws[i+1]] += 1
    return pairs_counters


def rate_words(text):
    """
    Вычисляет частоту слов в тексте.
    """
    rates = collections.Counter()
    for sent in sentences(text):
        for word in words(sent):
            rates[word] += 1
    return sorted(rates.items(), key=lambda elem: -elem[1])


def nowords(file, text):
    """
    Удаляет из text все слова, встречающиеся в файле file.
    Затем удаляет лишние пробелы.
    """
    de = r''
    for w in file.read().split(' '):
        de += r'\b' + w + r'\b|'
    de = re.sub(r'|$', '', de)
    text = re.sub(de, '', text)
    text = re.sub(r'[\s]+', ' ', text)
    return text
