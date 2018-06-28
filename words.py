### KELSEY'S WORD COLLECTION ###
import sqlite3

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



# MAIN PART OF CODE:
make_db()

# interacive word part
print('\n')
print('Welcome to Kelsey\'s Word Collection!')
print('This project was rooted in Kelsey\'s summer boredom, and a memory from high school:')
print('When I was in high school, I really wanted to have a larger vocabulary.')
print('More to my vernacular, if you will (see what I did there? big word!)')
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

print('\n')
print('Here we go:')
print('\n')
user_input = input('Please enter a word: ')
print('You entered \'' + user_input + '\'.')

base_or_no = check_database_for_word(user_input)

if base_or_no == True:
    print('This word is already in the collection!')
    print('If you\'d like to see the definition of this word, type \'definition\'.')
    print('If you\'d like to enter another word, type \'more words\'.')

if base_or_no == False:
    print('This is a new word! Adding it to the collection now.')
    print('If you\'d like to see the definition of this word, type \'definition\'.')
    print('If you\'d like to enter another word, type \'more words\'.')

# while user_input != 'exit':
#     if user_input == 'definition':

# populating the database
definition = 'oops'     # still need to figure this whole part out
length = len(user_input)

conn = sqlite3.connect('words.db')
cur = conn.cursor()
insertion = (None, user_input, definition, length)
statement = 'INSERT INTO \'Words\' '
statement += 'VALUES (?, ?, ?, ?)'
cur.execute(statement, insertion)
conn.commit()
