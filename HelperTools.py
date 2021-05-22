import nltk
from docx import Document
from pdfminer.high_level import extract_text
import bs4 as bs
import urllib.request
import wikipedia
from gensim.summarization import keywords
import RAKE
import operator

stopwords = nltk.corpus.stopwords.words('english')

#text = """"


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
        print(text)
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


def get_keywords(text):
    return (keywords(text).split('\n'))


def sort_tup(tup):
    tup.sort(key=lambda x: x[1])
    return tup


def get_keyphrases(text):
    stop_dir = "smartstoplist.txt"
    rakeobj = RAKE.Rake(stop_dir)

    lst = []
    keywords = sort_tup(rakeobj.run(text))
    for i in range(len(keywords)):
        if keywords[i][1] > 0 and len(keywords[i][0].split(' ')) > 1:
            lst.append(keywords[i][0])

    return lst[::-1]



