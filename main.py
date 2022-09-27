import operator
import nltk
import pandas as pd
import re                                                           # підтримка парсінгу сайту
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt                                     # підтримка парсінгу сайту
from bs4 import BeautifulSoup                                       # підтримка парсінгу сайту
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

# ---------- Парсер САЙТУ Interfax.ru для отримання html структури і вилучення з неї стрічки новин  --------
def Parser_URL_interfax(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    quotes_1 = soup.find_all('div', class_="an")
    output_file = open('C:/Users/serg/PycharmProjects/ds_lab51/text_1.txt', 'a')
    output_file_final = open('C:/Users/serg/PycharmProjects/ds_lab51/text_1_clear.txt', 'a')

    for quote in quotes_1:
        quote.encoding = 'cp1251'
        output_file.write(str(quote))

    with open(r'C:/Users/serg/PycharmProjects/ds_lab51/text_1.txt') as f:
        f = f.read()

    soup2 = BeautifulSoup(f, "html.parser")
    for link in soup2.find_all('h3'):
        link.encoding = 'cp1251'
        output_file_final.write(link.text +  '\n')
    return

# ---------- Парсер САЙТУ Korrespondent для отримання html структури і вилучення з неї стрічкі новин  --------
def Parser_URL_korrespondent (url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    quotes_2 = soup.find_all('div', class_='article__title')
    output_file_2 = open('C:/Users/serg/PycharmProjects/ds_lab51/text_2.txt', 'a')

    for quote in quotes_2:
        quote.encoding = 'cp1251'
        output_file_2.write(quote.text)
    return


# -------------- Частотний text mining --------------------------
def text_mining_wordcloud(f):
    text = str(f.readlines())
    # -------------- Аналіз тексту на частоту слів БЕЗ СОЮЗНИХ СЛІВ (наприклад НА, ЗА і т.д.) ----------------
    # words = re.findall('[a-zA-Z]{2,}', text)  # regex для англійських слів
    words = re.findall('[а-яА-Я]{2,}', text)  # regex для  російських слів
    stats = {}

    stop_words = stopwords.words("russian")
    stop_words.append('млн')
    stop_words.append('млрд')
    stop_words.append('июня')
    stop_words.append('против')
    stop_words_title = [None] * len(stop_words)
    for i in range(len(stop_words)):
        stop_words_title[i] = stop_words[i].title()

    for word in words:
        if word in stop_words:
            for i in range(words.count(word)):
                words.remove(word)
        if word in stop_words_title:
           for i in range(words.count(word)):
                words.remove(word)

    for w in words:
        stats[w] = stats.get(w, 0) + 1
    #print(stats)
    w_ranks = sorted(stats.items(), key=lambda x: x[1], reverse=True)[0:10]
    _wrex = re.findall('[а-яА-Я]+', str(w_ranks))
    _drex = re.findall('[0-9]+', str(w_ranks))

    pl = [p for p in range(1, 11)]
    for j in range(len(_wrex)):
        places = '{} place,{} - {} times'.format(pl[j], _wrex[j], _drex[j])
        print('places', places)
    text_raw = " ".join(_wrex)

    wordcloud = WordCloud().generate(text_raw)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
    return

# ---------- Докладний частотний text mining --------------
def text_mining_ru(filename):
    #nltk.download('punkt')
    #nltk.download('stopwords')
    with open(filename) as file:
        text = file.read()

    tokens = word_tokenize(text)
    #видалення союзних слів
    stop_words = stopwords.words("russian")
    filtered_tokens = []
    for token in tokens:
        if token not in stop_words:
            filtered_tokens.append(token)
    #видалення символів та номерів
    regex_numbers = re.compile('^[0-9]{1,4}([,:-][0-9]{1,4})*(\.[0-9]+)?$')
    digits = ['.', '-', ',', '/', '' '', '!', '@', '" "',
              '#', '№', '$', ':', ';', '%', '^', '&', '?',
              '*', '(', ')', '_', '+', '=', '[', ']', '{', '}',
              '"', ' ', '<', '>', '|', '`', '~', ',']

    for token in filtered_tokens:
        if token in digits:
            filtered_tokens.remove(token)
    for token in filtered_tokens:
        if (regex_numbers.search(token) != None):
            filtered_tokens.remove(token)

    words = []
    snowball = SnowballStemmer(language="russian")
    for i in filtered_tokens:
        word = snowball.stem(i)
        words.append(word)

    words.sort()
    words_dict = dict()

    for word in words:
        if word in words_dict:
            words_dict[word] = words_dict[word] + 1
        else:
            words_dict[word] = 1

    print("Кількість слів: %d" % len(words))
    print("Кількість унікальних слів: %d" % len(words_dict))
    print("Усі використані слова:")
    for word in words_dict:
        print(word.ljust(20), words_dict[word])

    return

# -------------- Головні виклики парсера для отримання даних text mining --------------------
print('Оберіть інформаційне джерело:')
print('1 - https://www.interfax.ru/')
print('2 - https://korrespondent.net/')
mode = int(input('mode:'))
if (mode == 1):
    with open('C:/Users/serg/PycharmProjects/ds_lab51/text_1.txt', 'w'):
        pass
    with open('C:/Users/serg/PycharmProjects/ds_lab51/text_1_clear.txt', 'w'):
        pass
    print('Обрано інформаційне джерело: https://www.interfax.ru/')
    url = 'https://www.interfax.ru/'
    url1 = 'https://www.interfax.ru/news/2022/06/02/all'
    url2 = 'https://www.interfax.ru/news/2022/06/02/all/page_2'
    url3 = 'https://www.interfax.ru/news/2022/06/02/all/page_3'
    url4 = 'https://www.interfax.ru/news/2022/06/03/all'
    url5 = 'https://www.interfax.ru/news/2022/06/03/all/page_2'
    url6 = 'https://www.interfax.ru/news/2022/06/03/all/page_3'

    #print (' ----------------- Новини Інтерфакс за 02.06 ---------')
    Parser_URL_interfax(url1)
    Parser_URL_interfax(url2)
    Parser_URL_interfax(url3)
    #print(' ----------------- Новини Інтерфакс за 03.06 ---------')
    Parser_URL_interfax(url4)
    Parser_URL_interfax(url5)
    Parser_URL_interfax(url6)

    print('Докладний частотний аналіз інформаційного джерела:', mode, ':', url)
    filename = 'C:/Users/serg/PycharmProjects/ds_lab51/text_1_clear.txt'
    words_dict = text_mining_ru(filename)

    f = open('C:/Users/serg/PycharmProjects/ds_lab51/text_1_clear.txt', 'r')
    print('Домінуючий контент сайту:', mode, ':', url)
    text_mining_wordcloud(f)



if (mode == 2):
    with open('C:/Users/serg/PycharmProjects/ds_lab51/text_2.txt', 'w'):
        pass
    print('Обрано інформаційне джерело: https://korrespondent.net/')
    url = 'https://korrespondent.net/'
    with open('C:/Users/serg/PycharmProjects/ds_lab51/text_2.txt', 'w'):
        pass
    #------------------- Новини за 02.06 -------------------------
    url11 = 'https://korrespondent.net/all/2022/june/2/print/'
    url21 = 'https://korrespondent.net/all/2022/june/2/p2/print/'
    url31 = 'https://korrespondent.net/all/2022/june/2/p3/print/'
    url41 = 'https://korrespondent.net/all/2022/june/2/p4/print/'
    url51 = 'https://korrespondent.net/all/2022/june/2/p5/print/'
    #------------------- Новини за 03.06 -------------------------
    url61 = 'https://korrespondent.net/all/2022/june/3/print/'
    url71 = 'https://korrespondent.net/all/2022/june/3/p2/print/'
    url81 = 'https://korrespondent.net/all/2022/june/3/p3/print/'
    url91 = 'https://korrespondent.net/all/2022/june/3/p4/print/'
    url101 = 'https://korrespondent.net/all/2022/june/3/p5/print/'

    Parser_URL_korrespondent(url11)
    Parser_URL_korrespondent(url21)
    Parser_URL_korrespondent(url31)
    Parser_URL_korrespondent(url41)
    Parser_URL_korrespondent(url51)
    Parser_URL_korrespondent(url61)
    Parser_URL_korrespondent(url71)
    Parser_URL_korrespondent(url81)
    Parser_URL_korrespondent(url91)
    Parser_URL_korrespondent(url101)

    # -------------- Частотний text mining аналіз даних від новосних сайтів --------------------
    f = open('C:/Users/serg/PycharmProjects/ds_lab51/text_2.txt', 'r')
    print('Домінуючий контент сайту:', mode, ':', url)
    text_mining_wordcloud(f)
    print('Докладний частотний аналіз інформаційного джерела:', mode, ':', url)
    filename = 'C:/Users/serg/PycharmProjects/ds_lab51/text_2.txt'
    text_mining_ru(filename)




