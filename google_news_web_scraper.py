"""
This script scrapes article titles from a Google News topic page, filters the titles based on a list of keywords,
and then creates a bar chart showing the number of articles that contain each keyword. It also saves the filtered
article titles to an Excel file.

Dependencies:
- pandas
- requests
- BeautifulSoup
- matplotlib

Usage:
1. Call the `scrape_and_analyze` function with the following arguments:
    - url (str): The URL of the Google News topic page you want to scrape.
    - key_words (list of str): A list of keywords you want to filter for.
    - max_article (int): The maximum number of articles to scrape.

Output:
- A tuple containing the following elements:
    - A list of the filtered article titles.
    - A dictionary showing the number of articles that contain each keyword.
- A bar chart showing the number of articles that contain each keyword.
- An Excel file containing the filtered article titles.

Example:

url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen'
key_words = ['bank', 'crisis', 'economy']
max_article = 50

titles, word_count = scrape_and_analyze(url, key_words, max_article)
"""

import pandas as pd
import requests as requests
from bs4 import BeautifulSoup
from matplotlib import pyplot as plt

url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US' \
      '%3Aen'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
key_words = ['bank', 'crisis', 'economy']
max_article = 50
titles = []


def create_empty_dict(key_list):
    """
    Create a dictionary with keys from the provided list and values set to None.

    Args:
        key_list (list): A list of keys to use in the dictionary.

    Returns:
        dict: A dictionary with keys from the provided list and values set to None.
    """
    dictionary = {key: None for key in key_list}
    return dictionary


def contains_keywords(item_searched, items_searched_for):
    """
    Check if a given string contains any of the provided keywords.

    Args:
        item_searched (str): The string to search for keywords in.
        items_searched_for (list): A list of keywords to search for in the given string.

    Returns:
        bool: True if the given string contains any of the provided keywords, False otherwise.
    """
    contains_keyword = any(keyword in item_searched for keyword in items_searched_for)
    return contains_keyword


def get_title(article, tag):
    """
    Get the text of the specified tag in the given BeautifulSoup article object and convert it to lowercase.

    Args:
        article (bs4.element.Tag): A BeautifulSoup article object.
        tag (str): The tag to search for in the article object.

    Returns:
        str: The text of the specified tag in the given article object, converted to lowercase.
    """
    article_title = article.find(tag).text
    return article_title.lower()


def get_articles_soup(url):
    """
    Get the BeautifulSoup object of a given Google News topic URL.

    Args:
        url (str): The URL of the Google News topic page.

    Returns:
        bs4.BeautifulSoup: A BeautifulSoup object containing the parsed HTML of the Google News topic page.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def get_filtered_titles(soup, key_words, max_article):
    """
     Get a list of filtered article titles from a BeautifulSoup object based on provided keywords.

     Args:
         soup (bs4.BeautifulSoup): A BeautifulSoup object containing the parsed HTML of the Google News topic page.
         key_words (list of str): A list of keywords to filter the article titles.
         max_article (int): The maximum number of article titles to return.

     Returns:
         list of str: A list of filtered article titles containing the specified keywords.
     """
    titles = []

    for articles in soup.find_all('article'):
        try:
            title = get_title(articles, 'h4')
            if contains_keywords(title, key_words):
                titles.append(title)
        except AttributeError:
            continue

        if len(titles) == max_article:
            break

    return titles


def save_titles_to_excel(titles, filename='article_titles.xlsx'):
    """
    Save the filtered article titles to an Excel file.

    Args:
        titles (list of str): A list of filtered article titles.
        filename (str, optional): The name of the Excel file to save the titles. Defaults to 'article_titles.xlsx'.
    """
    df = pd.DataFrame(titles, columns=["Title"])
    df.to_excel(filename, index=False)


def create_bar_chart(word_count):
    """
    Create a bar chart showing the number of articles that contain each keyword.

    Args:
        word_count (dict): A dictionary containing the number of articles that contain each keyword.
    """
    plt.bar(word_count.keys(), word_count.values())
    plt.xlabel('Keywords')
    plt.ylabel('Number of Articles')
    plt.title('Article Counts by Keyword')
    plt.show()


def scrape_and_analyze(url, key_words, max_article):
    """
    Scrape article titles from a Google News topic page, filter them based on a list of keywords, and create
    a bar chart showing the number of articles that contain each keyword. Also saves the filtered article titles
    to an Excel file.

    Args:
        url (str): The URL of the Google News topic page.
        key_words (list of str): A list of keywords to filter the article titles.
        max_article (int): The maximum number of article titles to return.

    Returns:
        tuple: A tuple containing the following elements:
            - A list of the filtered article titles.
            - A dictionary showing the number of articles that contain each keyword.
    """
    soup = get_articles_soup(url)
    titles = get_filtered_titles(soup, key_words, max_article)
    save_titles_to_excel(titles)
    word_count = {key: sum(contains_keywords(title, [key]) for title in titles) for key in key_words}
    create_bar_chart(word_count)

    return titles, word_count


if __name__ == "__main__":
    url = 'https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US' \
          '&ceid=US%3Aen'
    key_words = ['bank', 'crisis', 'economy']
    max_article = 50

    titles, word_count = scrape_and_analyze(url, key_words, max_article)

    print("Filtered article titles:")
    for title in titles:
        print(title)

    print("\nNumber of filtered articles:", len(titles))
    print("\nArticle count by keyword:", word_count)
