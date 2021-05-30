import re
from googletrans import Translator
import nltk
from docx import Document
from pdfminer.high_level import extract_text
import bs4 as bs
import urllib.request
import wikipedia
from gensim.summarization import keywords
import RAKE
from nltk import tokenize
from operator import itemgetter
import math
import operator
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

f = open('SmartStoplist.txt', 'r')
try:
    smartstoplist = f.read()
    # print(text)
except UnicodeDecodeError:
    pass

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(smartstoplist.split('\n'))
stopwords = set(stopwords)


def text_file(file):
    rf = file[::-1].index('.')
    extension = file[-1 * rf:]
    print(extension)
    if extension == 'txt':

        f = open(file, 'r')
        try:
            text = f.read()
            # print(text)
        except UnicodeDecodeError:
            pass

    elif extension == 'docx':

        text = ''
        f = Document(file)
        for i in f.paragraphs:
            text += i.text

    elif extension == 'pdf':

        text = extract_text(file)

    else:
        print("Please upload correct file !!!")
        return 0

    return text


def get_text_from_link(urllink):
    if urllink.find('wikipedia.org') != -1:
        result = urllink.find('wikipedia.org/wiki/')
        wiki = wikipedia.page(urllink[result + 19:])
        text = wiki.content
        text = text.replace('==', '')
        text = re.sub(r'\[[0-9]*\]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        text = re.sub('[^a-zA-Z]', ' ', text)
        text = re.sub(r'\s+', ' ', text)

        # print(text)
        return text

    scraped_data = urllib.request.urlopen(urllink)
    article = scraped_data.read()

    parsed_article = bs.BeautifulSoup(article, 'lxml')

    paragraphs = parsed_article.find_all('p')

    article_text = ""

    for p in paragraphs:
        article_text += p.text

    # article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
    # article_text = re.sub(r'\s+', ' ', article_text)
    # formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )
    # formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
    print(article_text)
    return article_text


def keywords_code(text):
    return keywords(text).split('\n')


# https://monkeylearn.com/keyword-extraction/
# https://medium.com/analytics-vidhya/keyword-extraction-techniques-using-python-edea5fc35678
# https://www.section.io/engineering-education/keyword-extraction-in-python/
# https://github.com/prachiprakash26/Keyword_Extractor_Python/blob/main/Keyword_Extraction_Python.ipynb
import TextVisualizations as tv
def get_keywords(doc , howmuch):
    doc=doc.lower()
    doc=re.sub('[^a-zA-Z" ".]+', '', doc)
    total_words = doc.split()
    total_word_length = len(total_words)
    # print(total_word_length, " twl")
    total_sentences = tokenize.sent_tokenize(doc)
    total_sent_len = len(total_sentences)
    # print(total_sent_len, " tsl")
    tf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stopwords:
            if each_word in tf_score:
                tf_score[each_word] += 1
            else:
                tf_score[each_word] = 1
    # print(tf_score, " tf score")

    # Dividing by total_word_length for each dictionary element
    tf_score.update((x, y / int(total_word_length)) for x, y in tf_score.items())

    # print(tf_score, " update tf score")

    def check_sent(word, sentences):
        final = [all([w in x for w in word]) for x in sentences]
        sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
        return int(len(sent_len))

    # Step 4: Calculate IDF for each word
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.', '')
        if each_word not in stopwords:
            if each_word in idf_score:
                idf_score[each_word] = check_sent(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(total_sent_len) / y)) for x, y in idf_score.items())

    # print(idf_score, " update idf score ")
    tf_idf_score = {key: tf_score[key] * idf_score.get(key, 0) for key in tf_score.keys()}

    # print(tf_idf_score, " tf idf score")

    # Get top N important words in the document
    def get_top_n(dict_elem, n):
        result = dict(sorted(dict_elem.items(), key=itemgetter(1), reverse=True)[:n])
        return result


    '''j = 1
    for i in (get_top_n(tf_idf_score,300 )).keys():
        print(j, ")", i)
        j += 1'''

    total=len(tf_idf_score.keys())
    howmuch= howmuch * total // 100
    return get_top_n(tf_idf_score , howmuch)




    #return get_top_n(tf_idf_score , 15 )



# get_keywords(text.lower())


def sort_tup(tup):
    tup.sort(key=lambda x: x[1])
    return tup

# https://bdewilde.github.io/blog/2014/09/23/intro-to-automatic-keyphrase-extraction/
def get_keyphrases(text , howmuch):
    stop_dir = "smartstoplist.txt"
    rakeobj = RAKE.Rake(stop_dir)
    keywords = sort_tup(rakeobj.run(text))
    keywords=keywords[::-1]
    total=len(keywords)
    howmuch= howmuch * total // 100
    lst=[]
    for i in range(howmuch):
        lst.append(keywords[i][0])
    return lst

def langtranslate(text , des):

    translator = Translator()
    translation = translator.translate(text, dest=des)

    return (translation.text)

def detect_lang(text):
    translator=Translator()
    return (translator.detect(text)).lang

