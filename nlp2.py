# -*- coding: utf-8 -*-
"""PranjalArora_102003402_NLP in Python - 2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/15ThQmRjqCWYpSVknKaMFqtaopifHkd3j

# Data Cleaning

` Data cleaning is a time consuming and unenjoyable task, yet it's a very important one. Keep in mind, "garbage in, garbage out".`

#### Feeding dirty data into a model will give us results that are meaningless.

### Objective:

1. Getting the data 
2. Cleaning the data 
3. Organizing the data - organize the cleaned data into a way that is easy to input into other algorithms

### Output :
#### cleaned and organized data in two standard text formats:

1. Corpus - a collection of text
2. Document-Term Matrix - word counts in matrix format

## Problem Statement

Look at transcripts of various comedians and note their similarities and differences and find if the stand up comedian of your choice has comedy style different than other comedian.

## Getting The Data

You can get the transcripts of some comedian from [Scraps From The Loft](http://scrapsfromtheloft.com). 

You can take help of IMDB and select only 10 or 20 comedian having highest rating.



"""

# Web scraping, pickle imports
import requests
#makes HTTP requests using simple API
from bs4 import BeautifulSoup 
# Beautiful Soup is a Python package for parsing HTML and XML documents. 
#It creates a parse tree for parsed pages that can be used to extract data from nested tags of 
#HTML, which is useful for web scraping. 
import pickle  
#“Pickling” is the process whereby a Python object hierarchy is converted into a byte stream, 
#and “unpickling” is the inverse operation, whereby a byte stream (from a binary file or bytes-like object) 
#is converted back into an object hierarchy.



# Scrapes transcript data from scrapsfromtheloft.com
def url_to_transcript(url):
    '''Returns transcript data specifically from scrapsfromtheloft.com.'''
    page = requests.get(url).text # get ALL data from the url
    soup = BeautifulSoup(page, "lxml")  #HTML document
    text = [p.text for p in soup.find(class_="elementor-widget-container").find_all('p')]
    print(url)
    return text

# URLs of transcripts in scope
urls = ['http://scrapsfromtheloft.com/2017/05/06/louis-ck-oh-my-god-full-transcript/',
        'http://scrapsfromtheloft.com/2017/04/11/dave-chappelle-age-spin-2017-full-transcript/',
        'http://scrapsfromtheloft.com/2018/03/15/ricky-gervais-humanity-transcript/',
        'http://scrapsfromtheloft.com/2017/08/07/bo-burnham-2013-full-transcript/',
        'http://scrapsfromtheloft.com/2017/05/24/bill-burr-im-sorry-feel-way-2014-full-transcript/',
        'http://scrapsfromtheloft.com/2017/04/21/jim-jefferies-bare-2014-full-transcript/',
        'http://scrapsfromtheloft.com/2017/08/02/john-mulaney-comeback-kid-2015-full-transcript/',
        'http://scrapsfromtheloft.com/2017/10/21/hasan-minhaj-homecoming-king-2017-full-transcript/',
        'http://scrapsfromtheloft.com/2017/09/19/ali-wong-baby-cobra-2016-full-transcript/',
        'http://scrapsfromtheloft.com/2017/08/03/anthony-jeselnik-thoughts-prayers-2015-full-transcript/',
        'http://scrapsfromtheloft.com/2018/03/03/mike-birbiglia-my-girlfriends-boyfriend-2013-full-transcript/',
        'http://scrapsfromtheloft.com/2017/08/19/joe-rogan-triggered-2016-full-transcript/']

# Comedian names
comedians = ['louis', 'dave', 'ricky', 'bo', 'bill', 'jim', 'john', 'hasan', 'ali', 'anthony', 'mike', 'joe']

# # Actually request transcripts (takes a few minutes to run)
transcripts = [url_to_transcript(u) for u in urls]

# # Pickle files for later use

# # Make a new directory to hold the text files
# !mkdir transcripts

# for i, c in enumerate(comedians):
#     with open("transcripts/" + c + ".txt", "wb") as file:
#         pickle.dump(transcripts[i], file)

# Load pickled files
data = {}
for i, c in enumerate(comedians):
    with open( "/content/sample_data/transcripts/"+c+".txt","rb") as file:
        data[c] = pickle.load(file)

# Double check to make sure data has been loaded properly
data.keys()

# More checks
data['louis'][:2]

"""## Cleaning The Data

When dealing with numerical data, data cleaning often involves removing null values and duplicate data, dealing with outliers, etc. With text data, there are some common data cleaning techniques, which are also known as text pre-processing techniques.

With text data, this cleaning process can go on forever. There's always an exception to every cleaning step. So, we're going to follow the MVP (minimum viable product) approach - start simple and iterate.
### Assignment:
1. Perform the following data cleaning on transcripts:
i) Make text all lower case
ii) Remove punctuation
iii) Remove numerical values
iv) Remove common non-sensical text (/n)
v) Tokenize text
vi) Remove stop words
"""

#MVP:- The MVP does not meet all (or even most) of the stakeholder needs. 
#However, it should provide enough functionality with sufficient quality to 
#engage and learn from consumers.


# Let's take a look at our data again
next(iter(data.keys()))  #return first iterator in the dictionary

# Notice that our dictionary is currently in key: comedian, value: list of text format
next(iter(data.values()))

# We are going to change this to 
#key: comedian
#value: string format

#make a function "combine_text" to join the "value"s in the dictionary when 
#used in a for loop with iterator of the dictionary
def combine_text(list_of_text):
    '''Takes a list of text and combines them into one large chunk of text.'''
    combined_text = ' '.join(list_of_text)
    return combined_text

# Combine it!
#using combine_text to make one block of text called "data_combined"
data_combined = {key: [combine_text(value)] for (key, value) in data.items()}

data_combined

# We can either keep it in dictionary format or put it into a pandas dataframe
import pandas as pd
pd.set_option('max_colwidth',150)

#make a dataframe
data_df = pd.DataFrame.from_dict(data_combined).transpose()
data_df.columns = ['transcript']
data_df = data_df.sort_index()
data_df

# Let's take a look at the transcript for Ali Wong
data_df.transcript.loc['ali']

# Apply a FIRST round of TEXT CLEANING TECHNIQUES, like
#Make all the text lowercase
#remove the text in square brackets
#remove punctuation
#remove words containing numbers


import re  #regular expressions
import string


def clean_text_round1(text):
    '''Make text lowercase, remove text in square brackets, remove punctuation and remove words containing numbers.'''
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)  #replaces a string with replaced values
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text) #Return string with all non-alphanumerics backslashed
    text = re.sub('\w*\d\w*', '', text)
    return text

round1 = lambda x: clean_text_round1(x)  #defininf a lambda function. A lambda function is a small anonymous function
#A lambda function can take any number of arguments, but can only have one expression.

# Let's take a look at the updated text
#apply the round 1 of text cleaning
data_clean = pd.DataFrame(data_df.transcript.apply(round1))

data_clean

# Apply a SECOND round of TEXT CLEANING
def clean_text_round2(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub('\n', '', text)
    return text

round2 = lambda x: clean_text_round2(x)

# Let's take a look at the updated text
data_clean = pd.DataFrame(data_clean.transcript.apply(round2))
data_clean

"""## Organizing The Data

### Assignment:
1. Organized data in two standard text formats:
   a) Corpus - corpus is a collection of texts, and they are all put together neatly in a pandas dataframe here.
   b) Document-Term Matrix - word counts in matrix format

### Corpus: Example

A corpus is a collection of texts, and they are all put together neatly in a pandas dataframe here.
"""

# Let's take a look at our dataframe
data_df=data_clean

# Let's add the comedians' full names as well
full_names = ['Ali Wong', 'Anthony Jeselnik', 'Bill Burr', 'Bo Burnham', 'Dave Chappelle', 'Hasan Minhaj',
              'Jim Jefferies', 'Joe Rogan', 'John Mulaney', 'Louis C.K.', 'Mike Birbiglia', 'Ricky Gervais']

data_df['full_name'] = full_names
data_df

# Let's pickle it for later use
data_df.to_pickle("corpus.pkl")

"""### Document-Term Matrix: Example

For many of the techniques we'll be using in future assignment, the text must be tokenized, meaning broken down into smaller pieces. The most common tokenization technique is to break down text into words. We can do this using scikit-learn's ` CountVectorizer `, where every row will represent a different document and every column will represent a different word.

In addition, with ` CountVectorizer `, we can remove stop words. Stop words are common words that add no additional meaning to text such as 'a', 'the', etc.
"""

# We are going to create a document-term matrix using CountVectorizer, and exclude common English stop words
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer(stop_words='english') #emoving stop words helps build cleaner dataset with better features for machine learning model.
data_cv = cv.fit_transform(data_clean.transcript)
print(data_cv)
data_dtm = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names_out())
data_dtm.index = data_clean.index
print(data_dtm.shape)
data_dtm

# Let's pickle it for later use
data_dtm.to_pickle("dtm.pkl")

# Let's also pickle the cleaned data (before we put it in document-term matrix format) and the CountVectorizer object
data_clean.to_pickle('data_clean.pkl')
pickle.dump(cv, open("cv.pkl", "wb"))

"""## Additional Assignments:

1. Can you add an additional regular expression to the clean_text_round2 function to further clean the text?
"""

#ANSWER1

#ROUND 3- ADDITIONAL REGULAR EXPRESSIONS TO CLEAN AFTER ROUND 2
def clean_text_round3(text):
    '''Get rid of some additional punctuation and non-sensical text that was missed the first time around.'''
    text = re.sub('[‘’“”…]', '', text)
    text = re.sub(r'\d+', '', text) # remove all numbers
    text = re.sub(r'\b\w\b', '', text) #remove single characters
    return text

round3 = lambda x: clean_text_round3(x)

data_clean_more = pd.DataFrame(data_clean.transcript.apply(round3))
data_clean_more

"""2. Play around with CountVectorizer's parameters. What is ngram_range? What is min_df and max_df?"""

from sklearn.feature_extraction.text import CountVectorizer

cv2 = CountVectorizer(stop_words='english',analyzer='word', ngram_range=(1, 2))
##n -gram --All values of n such that min_n <= n <= max_n will be used.
#an ngram_range of (1, 1) means only unigrams
#(1, 2) means unigrams and bigrams
#(2, 2) means only bigrams.
# Only applies if analyzer is not callable.
data_cv2 = cv.fit_transform(data_clean.transcript)
data_dtm2 = pd.DataFrame(data_cv.toarray(), columns=cv.get_feature_names())
data_dtm2.index = data_clean.index
data_dtm2

#max df --- When building the vocabulary ignore terms that have a document 
#frequency strictly higher than the given threshold (corpus-specific stop words)

#min df --- When building the vocabulary ignore terms that have a document 
#frequency strictly lower than the given threshold.