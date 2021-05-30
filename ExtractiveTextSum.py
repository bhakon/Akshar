import heapq
import re
import nltk
from nltk.tokenize import sent_tokenize
import HelperTools as ht

nltk.download('punkt')
nltk.download('stopwords')
f = open('SmartStoplist.txt', 'r')

try:
    smartstoplist = f.read()
    # print(text)
except UnicodeDecodeError:
    pass

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(smartstoplist.split('\n'))
stopwords = set(stopwords)


def Word_weight(article_text, p, lang):
    count = 1
    try:
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)
        formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text)
        formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)
        # print(article_text)
        sentence_list = (sent_tokenize(article_text))
        # print(len(sentence_list))
        sentence_list = set(sentence_list)
        sentence_list = list(sentence_list)
        noofsentences = len(sentence_list)
        howmuch = p * noofsentences // 100

        new_list = []
        for sentence in sentence_list:
            new_list.append((str(count) + ' : ' + sentence))
            count += 1
        sentence_list = new_list

        word_frequencies = {}
        for word in nltk.word_tokenize(formatted_article_text):
            if word not in stopwords:
                if word not in word_frequencies.keys():
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1
        maximum_frequency = max(word_frequencies.values())

        for word in word_frequencies.keys():
            word_frequencies[word] = (word_frequencies[word] / maximum_frequency)
        sentence_scores = {}
        for sent in sentence_list:
            for word in nltk.word_tokenize(sent.lower()):
                if word in word_frequencies.keys():
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word]
                    else:
                        sentence_scores[sent] += word_frequencies[word]

        summary_sentences = heapq.nlargest(howmuch, sentence_scores, key=sentence_scores.get)

        summary_dict = {}
        for sent in summary_sentences:
            index = sent.find(':')
            summary_dict[int(sent[:index - 1])] = sent[index + 2:]

        order_details = sorted(summary_dict.keys())
        i = 1
        string = ''
        print(order_details)
        lst=[]
        if lang == 'en':

            '''for j in order_details:
                print(i, ' : ', summary_dict[j])
                string += str(i) + " : " + summary_dict[j] + "&#13;&#10;"
                i += 1'''
            for j in order_details:
                print(i, ' : ', summary_dict[j])
                lst.append( str(i) + " : " + summary_dict[j] )
                i += 1

        else:

            '''for j in order_details:
                print(i, ' : ', summary_dict[j])
                string += str(i) + " : " + ht.langtranslate(summary_dict[j], lang) + "&#13;&#10;"
                i += 1'''
            for j in order_details:
                print(i, ' : ', summary_dict[j])
                lst.append( str(i) + " : " + ht.langtranslate(summary_dict[j], lang))
                i += 1

    except ValueError:
        pass
    return lst
