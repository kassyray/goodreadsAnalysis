#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pandas as pd
import sys

URL = sys.argv[1]
nameOut = sys.argv[2]

# URL = 'https://www.goodreads.com/list/show/2.The_Worst_Books_of_All_Time'
# URL = 'https://www.goodreads.com/list/show/1.Best_Books_Ever'


# Initiate variables 
nPage = 0
books = []
booklinks = []
bookIDs = []

# I am only interested in the first couple pages of the list 
while nPage != 2:
	# Create url for page of interest 
	url = URL + str(nPage)
	page = requests.get(URL)
	# Make soup! 
	soup = BeautifulSoup(page.content, 'html.parser')
	# Look for book titles 
	results = soup.find_all('a', attrs={'class': 'bookTitle'})

	for book in results:
		# Get the name of the book, the link to the book on GoodReads 
		bookname = book.get_text()
		booklink = book['href']
		# Isolate just the book ID 
		start = booklink.find('show/') + len('show/')
		
		if booklink.find('.') != -1: 
			end = booklink.find('.')
		elif booklink.rfind('-'):
			end = booklink.find('-')

		bookid = booklink[start:end]
		books.append(bookname)
		booklinks.append(booklink)
		bookIDs.append(bookid)

	nPage = nPage + 1 

# Add book names and book links to a pandas dataframe
output = pd.DataFrame(list(zip(books, booklinks, bookIDs)), columns = ['BookTitle','BookLink','bookIDs'] )

# Remove new line characters
output['BookTitle'] = output['BookTitle'].replace('\\n','',regex=True)

output.to_csv(nameOut)







        
