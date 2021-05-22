import collections
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure
import mpld3
import nltk
from nltk.tokenize import sent_tokenize
import re
import unicodedata
from nltk.corpus import stopwords
from collections import Counter
import mpld3
from matplotlib.pyplot import figure
from wordcloud import WordCloud, STOPWORDS
from textblob import TextBlob

ADDITIONAL_STOPWORDS = ['covfefe']
stopwords = nltk.corpus.stopwords.words('english') + ADDITIONAL_STOPWORDS


def preprocess(ReviewText):
    ReviewText = ReviewText.replace("(<br/>)", "")
    ReviewText = ReviewText.replace('(<a).*(>).*(</a>)', '')
    ReviewText = ReviewText.replace('(&amp)', '')
    ReviewText = ReviewText.replace('(&gt)', '')
    ReviewText = ReviewText.replace('(&lt)', '')
    ReviewText = ReviewText.replace('(\xa0)', ' ')
    return ReviewText


def get_top_n_words_wo_stopwords(corpus, n_print=None):
    corpus = preprocess(corpus)
    wordcount = {}
    a = corpus
    fig = figure()
    ax = fig.gca()

    for word in a.lower().split():
        word = word.replace(".", "")
        word = word.replace(",", "")
        word = word.replace(":", "")
        word = word.replace("\"", "")
        word = word.replace("!", "")
        word = word.replace("â€œ", "")
        word = word.replace("â€˜", "")
        word = word.replace("*", "")
        if word not in stopwords:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
    word_counter = collections.Counter(wordcount)
    # for word, count in word_counter.most_common(n_print):
    #    print(word, ": ", count)
    lst = word_counter.most_common(n_print)
    df = pd.DataFrame(lst, columns=['Word', 'Count'])
    df.plot.bar(x='Word', y='Count', ax=ax, figsize=(14, 6))
    plt.xlabel('Words')
    plt.ylabel('Word Count')

    plt.title(label='Most Common Words (Unigrams)',
              fontweight=10,
              pad='7.0')
    plt.tight_layout()
    mpld3.save_html(fig, "static/unigram_wo_stopwords.html")


def get_top_n_words(corpus, n_print=None):
    fig = figure()
    ax = fig.gca()

    corpus = preprocess(corpus)
    wordcount = {}
    a = corpus
    for word in a.lower().split():
        word = word.replace(".", "")
        word = word.replace(",", "")
        word = word.replace(":", "")
        word = word.replace("\"", "")
        word = word.replace("!", "")
        word = word.replace("â€œ", "")
        word = word.replace("â€˜", "")
        word = word.replace("*", "")
        if word not in wordcount:
            wordcount[word] = 1
        else:
            wordcount[word] += 1
    word_counter = Counter(wordcount)
    lst = word_counter.most_common(n_print)
    df = pd.DataFrame(lst, columns=['Word', 'Count'])
    df.plot.bar(x='Word', y='Count', ax=ax, figsize=(14, 6))
    plt.xlabel('Words')
    plt.ylabel('Word Count')

    plt.title(label='Most Common Words with stop words (Unigrams)',
              fontweight=10,
              pad='7.0')
    plt.tight_layout()
    mpld3.save_html(fig, "static/unigram_stopwords.html")


def get_top_n_bigram_stopwords(corpus, n_print=None):
    fig = figure()
    ax = fig.gca()

    corpus = preprocess(corpus)
    a = corpus
    for word in a.lower().split():
        word = word.replace(".", "")
        word = word.replace(",", "")
        word = word.replace(":", "")
        word = word.replace("\"", "")
        word = word.replace("!", "")
        word = word.replace("â€œ", "")
        word = word.replace("â€˜", "")
        word = word.replace("*", "")

    bigrams = zip(a.split(), a.split()[1:])
    counts = Counter(bigrams)
    # print(counts.most_common())

    lst = counts.most_common(n_print)
    another_lst = []

    for i in lst:
        another_lst.append((i[0][0] + " " + i[0][1], i[1]))

    lst = another_lst

    df = pd.DataFrame(lst, columns=['Word', 'Count'])
    df.plot.bar(x='Word', y='Count', ax=ax, figsize=(14, 6))
    plt.xlabel('Word Pair')
    plt.ylabel('Word Pair Count')

    plt.title(label='Most Common Word Pair with stop words (Bigrams)',
              fontweight=10,
              pad='7.0')
    plt.tight_layout()

    mpld3.save_html(fig, "static/bigram_stopwords.html")


def get_top_n_bigram_wo_stop_words(corpus, n_print=None):
    corpus = preprocess(corpus)

    a = corpus
    padalu = []
    fig = figure()
    ax = fig.gca()

    for word in a.lower().split():
        word = word.replace(".", "")
        word = word.replace(",", "")
        word = word.replace(":", "")
        word = word.replace("\"", "")
        word = word.replace("!", "")
        word = word.replace("â€œ", "")
        word = word.replace("â€˜", "")
        word = word.replace("*", "")
        if word not in stopwords:
            padalu.append(word)
    bigrams = zip(padalu, padalu[1:])
    counts = Counter(bigrams)
    # print(counts.most_common())

    lst = counts.most_common(n_print)
    another_lst = []

    for i in lst:
        another_lst.append((i[0][0] + " " + i[0][1], i[1]))

    lst = another_lst

    df = pd.DataFrame(lst, columns=['Word', 'Count'])
    df.plot.bar(x='Word', y='Count', ax=ax, figsize=(14, 6))
    plt.xlabel('Word Pair')
    plt.ylabel('Word Pair Count')

    plt.title(label='Most Common Word Pair with out stop words (Bigrams)',
              fontweight=10,
              pad='7.0')
    plt.tight_layout()
    mpld3.save_html(fig, "static/bigram_wo_stopwords.html")


def get_top_n_trigram_stopwords(corpus, n_print=None):
    corpus = preprocess(corpus)
    a = corpus
    fig = figure()
    ax = fig.gca()

    for word in a.lower().split():
        word = word.replace(".", "")
        word = word.replace(",", "")
        word = word.replace(":", "")
        word = word.replace("\"", "")
        word = word.replace("!", "")
        word = word.replace("â€œ", "")
        word = word.replace("â€˜", "")
        word = word.replace("*", "")

    padalu = a.split()
    trigrams = zip(padalu, padalu[1:], padalu[2:])
    counts = Counter(trigrams)
    # print(counts.most_common())

    lst = counts.most_common(n_print)
    another_lst = []

    for i in lst:
        another_lst.append((i[0][0] + " " + i[0][1] + " " + i[0][2], i[1]))

    lst = another_lst

    df = pd.DataFrame(lst, columns=['Word', 'Count'])
    df.plot.bar(x='Word', y='Count', ax=ax, figsize=(14, 6))
    plt.xlabel('Word Pair')
    plt.ylabel('Word Pair Count')

    plt.title(label='Most Common Word trio with stop words (trigrams)',
              fontweight=10,
              pad='7.0')
    plt.tight_layout()

    mpld3.save_html(fig, "static/trigram_stopwords.html")


def get_top_n_trigram_wo_stop_words(corpus, n_print=None):
    corpus = preprocess(corpus)

    fig = figure()
    ax = fig.gca()

    a = corpus
    padalu = []
    for word in a.lower().split():
        word = word.replace(".", "")
        word = word.replace(",", "")
        word = word.replace(":", "")
        word = word.replace("\"", "")
        word = word.replace("!", "")
        word = word.replace("â€œ", "")
        word = word.replace("â€˜", "")
        word = word.replace("*", "")
        if word not in stopwords:
            padalu.append(word)
    trigrams = zip(padalu, padalu[1:], padalu[2:])
    counts = Counter(trigrams)
    # print(counts.most_common())

    lst = counts.most_common(n_print)
    another_lst = []

    for i in lst:
        another_lst.append((i[0][0] + " " + i[0][1] + " " + i[0][2], i[1]))

    lst = another_lst

    df = pd.DataFrame(lst, columns=['Word', 'Count'])
    df.plot.bar(x='Word', y='Count', ax=ax, figsize=(14, 6))
    plt.xlabel('Word trio')
    plt.ylabel('Word trio Count')

    plt.title(label='Most Common Word trio with out stop words (trigrams)',
              fontweight=10,
              pad='7.0')
    plt.tight_layout()
    mpld3.save_html(fig, "static/trigram_wo_stopwords.html")


def plot_pos(corpus):
    blob = TextBlob(corpus)
    fig = figure()
    ax = fig.gca()

    df = pd.DataFrame(blob.tags, columns=['word', 'pos'])
    df = df.pos.value_counts()[:20]
    df.plot.bar(x='word', y='pos', ax=ax, figsize=(14, 6))
    plt.xlabel('Parts Of Speech')
    plt.ylabel('Tags Count')

    plt.title(label='Top 20 Part-of-speech tagging for given text',
              fontweight=10,
              pad='7.0')
    plt.tight_layout()
    mpld3.save_html(fig, "static/pos.html")


def generate_wordcloud(corpus):
    fig = figure()
    ax = fig.gca()

    wordcloud = WordCloud(width=3000, height=2000, random_state=1, background_color='white', collocations=False,
                          stopwords=STOPWORDS).generate(corpus)
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout()
    plt.savefig("static/wordcloud.jpg")


def run(corpus):
    get_top_n_words_wo_stopwords(corpus, 20)
    get_top_n_words(corpus, 20)
    get_top_n_bigram_stopwords(corpus, 20)
    get_top_n_bigram_wo_stop_words(corpus, 20)
    get_top_n_trigram_stopwords(corpus, 20)
    get_top_n_trigram_wo_stop_words(corpus, 20)
    plot_pos(corpus)
    #generate_wordcloud(corpus)
