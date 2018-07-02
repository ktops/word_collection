### KELSEY'S WORD COLLECTION ###
import sqlite3
import json
import requests
from bs4 import BeautifulSoup
# import plotly.plotly as py
# import plotly.graph_objs as go
import sys
import codecs
import csv
import webbrowser

# caching for definitions info
CACHE_FNAME = 'definitions_cache.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()
except:
    CACHE_DICTION = {}

def get_unique_key(url):
  return url

def make_request_using_cache(url):
    unique_ident = get_unique_key(url)

    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    else:
        # print("Making a request for new data...")
        resp = requests.get(url)
        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close()
        return CACHE_DICTION[unique_ident]

# this function creates the database that the words are kept in
# it should only be run the very first time the program is run, or all the words will disappear!!!
def make_db():
    # creating new database
    conn = sqlite3.connect('words.db')
    cur = conn.cursor()

    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Words';
    '''
    cur.execute(statement)
    conn.commit()

    # make new table
    statement = '''
        CREATE TABLE 'Words' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Word' TEXT,
            'Definition' TEXT,
            'Length' INTEGER
        );
    '''
    cur.execute(statement)
    conn.commit()

    conn.close()

# this function checks the database to see if the word is already in there or not
def check_database_for_word(word):
    conn = sqlite3.connect('words.db')
    cur = conn.cursor()

    statement = 'SELECT COUNT(*) '
    statement += 'FROM Words '
    statement += 'WHERE Word = \'' + word + '\' '
    outcome = cur.execute(statement)
    conn.commit()

    outcome = outcome.fetchone()[0]

    if outcome == 1:
        return True
    else:
        return False

# this funciton will get scrape the definition of the word from online and put it the database
# and print it out for the user when asked (?)
def get_definition(word):
    # getting to the right page for each word
    dict_url = 'http://www.dictionary.com/browse/' + word + '?s=t'

    # getting the first definition
    defs_page_text = make_request_using_cache(dict_url)
    defs_page_soup = BeautifulSoup(defs_page_text, 'html.parser')
    defs1 = defs_page_soup.find('div', id='root')
    defs2 = defs1.find('div', id='initial-load-content')
    defs3 = defs2.find('main', class_='css-d5e8ah e1fub8bm3')
    defs4 = defs3.find('section', class_='css-dfjnxh e8xvxkb0')
    defs5 = defs4.find('section', class_='css-1li42on e1hj943x0')
    defs6 = defs5.find('section', class_='css-1748arg e1wu7xq20')
    defs8 = defs6.find('section', class_='css-1sdcacc e10vl5dg0')

    defs9 = defs8.find_all('li')
    defs10 = defs9[0]
    defs11 = defs10.find('span', class_='css-9sn2pa e10vl5dg6').text

    word_def = defs11[:-1]
    return word_def


def entering_a_word(word):
    base_or_no = check_database_for_word(word)

    if base_or_no == True:
        print('This word is already in the collection!')

    if base_or_no == False:
        print('This is a new word! Adding it to the collection now.')

        # populating the database
        definition = get_definition(word)
        length = len(word)

        conn = sqlite3.connect('words.db')
        cur = conn.cursor()
        insertion = (None, word, definition, length)
        statement = 'INSERT INTO \'Words\' '
        statement += 'VALUES (?, ?, ?, ?)'
        cur.execute(statement, insertion)
        conn.commit()

# MAIN PART OF CODE:
make_db()

# interacive word part
print('\n')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')
print('Welcome to Kelsey\'s Word Collection!')
print('This project was rooted in Kelsey\'s summer boredom, and a memory from high school:')
print('When I was in high school, I really wanted to have a larger vocabulary.')
print('More to my vernacular, if you will (see what I did there? big word!) I hope I used it correctly.')
print('I started to write down every word that I saw that I either didn\'t know or couldn\'t remember the meaning of.')
print('How cool was I? I was creating my own personal dictionary.')
print('Soon, I had this massive list of words I didn\'t know, and I was losing track of duplicates.')
print('When I got to college, I stopped, as the list was too long and I was wasting time writing down words every time I saw them.')
print('But guess what? I know how to create databases now, and I\'m bored.')
print('\n')
print('Anyways, enough about me, let\'s do this.')

print('\n')
print('A quick overview of what we can do here:')
print('To input a word into the collection, simply type the word.')
print('If the word is already in the database, you will be notified, if not, it will add the word.')
print('After that, you will have the option to add another word or see the definiton of the word you just entered.')
print('If you just want to see the definiton of a word, type in the word and then choose to see the definiton.')
print('Please try to make sure that you spell the word correctly - we don\'t want fake words in the database!')
print('To exit the program, just type \'exit\'.')
print('- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -')

print('\n')
print('Here we go:')
print('\n')
user_input = input('Please enter a word: ')
print('You entered \'' + user_input + '\'.')

while user_input != 'exit':
    entering_a_word(user_input)

    user_input_after_word = input('If you\'d like to see the definition of this word, type \'definition\'. If you\'d like to enter another word, type \'more words\'. ')

    if user_input_after_word == 'definition':
        conn = sqlite3.connect('words.db')
        cur = conn.cursor()

        statement = 'SELECT Definition '
        statement += 'FROM Words '
        statement += 'WHERE Word = \'' + user_input + '\' '
        outcome = cur.execute(statement)
        conn.commit()

        outcome = outcome.fetchone()[0]

        print('Definition for \'' + user_input + '\': ' + outcome)
        print('\n')

    if user_input_after_word == 'more words':
        user_input = input('Please enter a word: ')
        print('You entered \'' + user_input + '\'.')
        user_input_after_word = input('If you\'d like to see the definition of this word, type \'definition\'. If you\'d like to enter another word, type \'more words\'. ')
        entering_a_word(user_input)

    user_input = input('Please enter a word: ')
    print('You entered \'' + user_input + '\'.')

print('\n')
print('Bye! Have a good day!')
