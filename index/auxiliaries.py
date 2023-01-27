import json
from collections import defaultdict
from nltk.tokenize import word_tokenize
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep


def load_data(file_name):
    """
    Function used to load the data

    Args:
        file_name: path to the file to load

    Returns:
        the data loaded from a json file in python

    """

    with open(file_name, "r") as f:
        data = json.load(f)
    return data

def create_index(data, stemmer):
    """
    Function used to compute the index

    Args:
        data: the data loaded by the load_data() function
        stemmer : the stemmer initialised earlier

    Returns:
        index : the negative index to dump as dictionnary
        pos_index : the positive index to dump as dictionnary
        stats : the statistics to be dumped (number of docs ...)

    Raises:
        TimeoutError: When an URL took too long to be reached
        TooManyRedirectsError : When an URL was responsible for to many redirections
        RequestsError : When the requests package threw an exception with that url
    """

    index = defaultdict(list)
    pos_index = defaultdict(lambda: defaultdict(list))
    num_docs = 0
    num_tokens = 0

    #Loop on all URLs with progressBar

    for i in tqdm(range(len(data))):
        url = data[i]

        try:
            
            page = requests.get(url, timeout=3)
            soup = BeautifulSoup(page.content, 'html.parser')
            title = soup.find('title').get_text()
            tokens = word_tokenize(title)
            stemmed_tokens = [stemmer.stem(token) for token in tokens]
            num_docs += 1
            num_tokens += len(tokens)

            # Write index

            for i, token in enumerate(tokens):
                index[token].append(url)
                pos_index[token][url].append(i)
            for i, stemmed_token in enumerate(stemmed_tokens):
                index[stemmed_token].append(url)

        #Exceptions to reaching urls :

        except requests.exceptions.Timeout:
            print(f'Timeout occurred for url: {url}')
        except requests.exceptions.TooManyRedirects:
            print(f'TooManyRedirects occurred for url: {url}')
        except requests.exceptions.RequestException as e:
            print(f'RequestException occurred for url: {url}')
            print(e)
        except :
            sleep(1)
    
    #Computing statistics

    avg_tokens_per_doc = num_tokens / num_docs
    stats = {
        "num_docs": num_docs,
        "num_tokens": num_tokens,
        "avg_tokens_per_doc": avg_tokens_per_doc
    }

    return index, pos_index, stats

def save_index(index, file_name):
    """
    Function used to save the index as JSON file

    Args:
        index : the dictionnary to dump
        file_name: the name of the file created
    """
    with open(file_name, "w") as f:
        json.dump(index, f)

def save_stats(stats, file_name):
    """
    Function used to load the data

    Args:
        stats : the stats to dump as a dictionnary
        file_name: the name of the file created

    """
    with open(file_name, "w") as f:
        json.dump(stats, f)