import parse_text as pt
import re
import collections
import argparse
import sys
import random


def capitalizeFirst(string):
    """
    Делает первую букву строки заглавной
    """
    if string:
        return string[0].upper() + string[1:]
    return string


def createParser():
    """
    Создаёт парсер аргументов командной строки и настраивает справку
    """
    parser = argparse.ArgumentParser(prog='Бредогенератор',
                                     epilog='(c) Vitali Samodelkin, 2015')
    parser.add_argument('-c', '--count',
                        type=int, default=150,
                        help='Длина текста"')
    parser.add_argument('-p', '--paragraph_lenght',
                        type=int, default=5,
                        help='Число предложений в абзаце')
    parser.add_argument('-f', '--file',
                        default=None,
                        help='Текст для обучения')
    parser.add_argument('-e', '--encoding',
                        default='utf8',
                        help='Кодировка входного файла, по умолчанию utf8')
    parser.add_argument('-s', '--start',
                        default='князь',
                        help='Стартовое слово для генерации текста')
    return parser

def generate(namespace,mytext):
    bigrams = pt.bigramms(mytext)
    current_word = namespace.start
    used_words = collections.Counter()
    waswor = set()
    total = 0
    bit = bigrams.items()
    current_text = '   '
    current_sent = capitalizeFirst(current_word)
    sent = 0
    for i in range(namespace.count):
        total += 1
        if total > 5 or current_word not in bigrams or len(bigrams[current_word]) == 0:
            if (total > 1):
                current_text += current_sent+'. '
                sent += 1
                if (sent > namespace.paragraph_lenght):
                    current_text += '\n\n   '
                    sent = 0
            current_word = list(bit)[random.randrange(len(bit))][0]
            current_sent = capitalizeFirst(current_word)
            total = 0
        now = list(bigrams[current_word].items())
        next_index = used_words[current_word]
•        used_words[current_word] += 1 
        while next_index >= (len(now)):
            current_word = list(bit)[random.randrange(len(bit))][0]
            now = list(bigrams[current_word].items())
            total = 0
            next_index = used_words[current_word]
        while now[next_index][0] in waswor:
            next_index += 1
            while next_index >= (len(now)):
                current_word = list(bit)[random.randrange(len(bit))][0]
                now = list(bigrams[current_word].items())
                total = 0
                next_index = used_words[current_word]
        waswor.add(now[next_index][0])
        current_sent += ' '+now[next_index][0]
        current_word = now[next_index][0]
    return current_text
    
def main():
    parser = createParser()
    namespace = parser.parse_args()
    if (namespace.file == None):
        file = sys.stdin
    else:
        try:
            file = open(namespace.file,'r',encoding = namespace.encoding)
        except FileNotFoundError:
            print("Файл не найден")
            return
    mytext = file.read()
    file.close()
    print(generate(namespace,mytext))

if __name__ == '__main__':
    main()
