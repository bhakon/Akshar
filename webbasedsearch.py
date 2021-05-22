import urllib
from fake_useragent import UserAgent
import re
from urllib.request import Request, urlopen
import wptools
import requests
import nltk
from bs4 import BeautifulSoup
import HelperTools as ht
import ExtractiveTextSum as ets


def get_google_box(query):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
    r = requests.get('https://www.google.com/search?q=' + query, headers=headers)

    soup = BeautifulSoup(r.text, 'lxml')

    result = soup.find('div', class_='Z0LcW')
    # result = soup.find('div', class_='gL9Hy')

    return (result.text)


def spelling_corrector(query):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'}
        r = requests.get('https://www.google.com/search?q=' + query, headers=headers)

        soup = BeautifulSoup(r.text, 'lxml')
        result = soup.find('a', class_='gL9Hy')
        return (result.text)
    except:
        pass


def google_results(keyword, n_results):
    query = keyword
    query = urllib.parse.quote_plus(query)  # Format into URL encoding
    number_result = n_results
    ua = UserAgent()
    google_url = "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result = soup.find_all('div', attrs={'class': 'ZINbbc'})
    results = [re.search('\/url\?q\=(.*)\&sa', str(i.find('a', href=True)['href'])) for i in result if "url" in str(i)]
    links = [i.group(1) for i in results if i != None]
    # remove youtube links
    sublinks = []
    for link in links:
        if link.find('www.youtube.com') == -1:
            sublinks.append(link)
    return (sublinks)


def infobox(item):
    so = wptools.page(item).get_parse()
    infobox = so.data['infobox']
    return infobox


def wikiresult(query):
    dic = infobox(query)
    for i in dic.keys():
        print(i, " : ", dic[i])


def mainu(query):
    flag = query[-1]
    query = query[:len(query) - 1]
    links = google_results(query, 10)
    for link in links:
        index = link.find("en.wikipedia.org/wiki/")
        if flag != '$' and index != -1:
            wiki = link[index + 22:]
            return infobox(wiki)

    else:
        try:
            return {query: get_google_box(query)}
        except:
            total_text = ""
            for link in links:
                try:

                    total_text += ht.get_text_from_link(link)
                except:
                    pass
            return {query: ets.Word_weight(total_text)}
