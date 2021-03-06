from bs4 import BeautifulSoup
import requests
import re
import os
import csv
import unittest

def get_titles_from_search_results(filename): 
    with open(filename, 'r') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        tags = soup.find_all('a', class_ ='bookTitle')
        titles = []
        for tag in tags:
            titles.append(tag.text.strip())
        authors = []
        for author in soup.find_all('span', itemprop="author"):
            authors.append(author.find('span', itemprop="name").text.strip())
    final = []
    for i in range(0, len(titles)):
        tup = (titles[i], authors[i])
        final.append(tup)
    return final
    
    


def get_search_links():

    url = "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    links = []
    for link in soup.find_all('a', attrs = {'href' : re.compile(r'/book/show/')}):
        links.append("https://www.goodreads.com" + link.get('href'))
    final = links[0:10]
    return final

    """
    Write a function that creates a BeautifulSoup object after retrieving content from
    "https://www.goodreads.com/search?q=fantasy&qid=NwUsLiA2Nc". Parse through the object and return a list of
    URLs for each of the first ten books in the search using the following format:

    ['https://www.goodreads.com/book/show/84136.Fantasy_Lover?from_search=true&from_srp=true&qid=NwUsLiA2Nc&rank=1', ...]

    Notice that you should ONLY add URLs that start with "https://www.goodreads.com/book/show/" to 
    your list, and , and be sure to append the full path to the URL so that the url is in the format 
    “https://www.goodreads.com/book/show/kdkd".

    """

   


def get_book_summary(book_url):
    url = book_url
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    tup = ()
    title = soup.find('h1', id="bookTitle")
    tup = tup + (title.text.strip(),)
    author = soup.find('div', class_ = "authorName__container")
    tup = tup + (author.text.strip(),)
    pages = soup.find('span', itemprop = "numberOfPages")
    add = pages.text.split()
    tup = tup + (int(add[0]),)
    return tup
    """
    Write a function that creates a BeautifulSoup object that extracts book
    information from a book's webpage, given the URL of the book. Parse through
    the BeautifulSoup object, and capture the book title, book author, and number 
    of pages. This function should return a tuple in the following format:

    ('Some book title', 'the book's author', number of pages)

    HINT: Using BeautifulSoup's find() method may help you here.
    You can easily capture CSS selectors with your browser's inspector window.
    Make sure to strip() any newlines from the book title and number of pages.
    """



def summarize_best_books(filepath):
    
    with open(filepath, 'r') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        tags = soup.find_all('h4', class_ ='category__copy')
        genres = []
        for tag in tags:
            genres.append(tag.text.strip())
        titles = []
        for title in soup.find_all('img', class_ ='category__winnerImage'):
            titles.append(title.get('alt'))
        links = []
        for link in soup.find_all('a', attrs = {'href' : re.compile(r'https://www.goodreads.com/choiceawards/best-[c-z]')}):
            links.append(link.get('href'))
        links.pop(0)
        final = []
        for i in range(0,len(genres)):
            tup = (genres[i], titles[i], links[i])
            final.append(tup)
    return final
 
    """
    Write a function to get a list of categories, book title and URLs from the "BEST BOOKS OF 2020"
    page in "best_books_2020.htm". This function should create a BeautifulSoup object from a 
    filepath and return a list of (category, book title, URL) tuples.
    
    For example, if the best book in category "Fiction" is "The Testaments (The Handmaid's Tale, #2)", with URL
    https://www.goodreads.com/choiceawards/best-fiction-books-2020, then you should append 
    ("Fiction", "The Testaments (The Handmaid's Tale, #2)", "https://www.goodreads.com/choiceawards/best-fiction-books-2020") 
    to your list of tuples.
    """



def write_csv(data, filename):
    file = open(filename, 'w', newline ='') 
    with file: 
        columns = ['Book title', 'Author Name']
        writer = csv.DictWriter(file, fieldnames = columns) 
        writer.writeheader()
        for t in data:
            writer.writerow({columns[0] : t[0], columns[1] : t[1]}) 


def extra_credit(filepath):
     with open(filepath, 'r') as html_file:
        soup = BeautifulSoup(html_file, 'lxml')
        tags = soup.find("span", id="freeText4791443123668479528")
        list = re.findall(r'(?:[A-Z][a-z]{2,100000}\s*){2,100000}', tags.text)
        return list


class TestCases(unittest.TestCase):
    # call get_search_links() and save it to a static variable: search_urls
    search_urls = get_search_links()

    def test_get_titles_from_search_results(self):
        # call get_titles_from_search_results() on search_results.htm and save to a local variable
        titles_authors = get_titles_from_search_results('search_results.htm')
        # check that the number of titles extracted is correct (20 titles)
        self.assertEqual(len(titles_authors), 20) 
        # check that the variable you saved after calling the function is a list
        self.assertEqual(isinstance(titles_authors, list), True) 
        # check that each item in the list is a tuple
        for i in range(0, len(titles_authors)):
            self.assertEqual(isinstance(titles_authors[i], tuple), True) 
        # check that the first book and author tuple is correct (open search_results.htm and find it)
        self.assertEqual(titles_authors[0], ('Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'))
        # check that the last title is correct (open search_results.htm and find it)
        self.assertEqual(titles_authors[-1], ('Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'))
    
    def test_get_search_links(self):
        # check that TestCases.search_urls is a list
        search_links = get_search_links()
        # check that the length of TestCases.search_urls is correct (10 URLs)
        self.assertEqual(len(search_links), 10) 
        # check that each URL in the TestCases.search_urls is a string
        for i in range(0, len(search_links)):
            self.assertEqual(isinstance(search_links[i], str), True)         
        # check that each URL contains the correct url for Goodreads.com followed by /book/show/
        for link in search_links:
            if re.compile(r'https://www.goodreads.com/book/show/'):
                answer = True
            else:
                answer = False
            self.assertEqual(answer, True)
    
    def test_get_book_summary(self):
        # create a local variable – summaries – a list containing the results from get_book_summary()
        summaries = []
        for url in TestCases.search_urls:
            answer = get_book_summary(url)
            summaries.append(answer)
        # for each URL in TestCases.search_urls (should be a list of tuples)          
        # check that the number of book summaries is correct (10)
        self.assertEqual(len(summaries), 10)
            # check that each item in the list is a tuple
        for i in range(0, len(summaries)):
            self.assertEqual(isinstance(summaries[i], tuple), True)
            # check that each tuple has 3 elements
            self.assertEqual(len(summaries[i]), 3)
            # check that the first two elements in the tuple are string
            self.assertEqual(isinstance(summaries[i][0], str), True)
            self.assertEqual(isinstance(summaries[i][1], str), True)
            # check that the third element in the tuple, i.e. pages is an int
            self.assertEqual(isinstance(summaries[i][2], int), True)
            # check that the first book in the search has 337 pages
        self.assertEqual(summaries[0][2], 337)
    
    def test_summarize_best_books(self):
       
        # call summarize_best_books and save it to a variable
        base_path = os.path.abspath(os.path.dirname(__file__))
        full_path = os.path.join(base_path, "best_books_2020.htm")
        best_books = summarize_best_books(full_path)
        # check that we have the right number of best books (20)
        self.assertEqual(len(best_books), 20)
        for i in range(0, len(best_books)):
            # assert each item in the list of best books is a tuple
            self.assertEqual(isinstance(best_books[i], tuple), True)
            # check that each tuple has a length of 3
            self.assertEqual(len(best_books[i]), 3)
        # check that the first tuple is made up of the following 3 strings:'Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'
        self.assertEqual(best_books[0], ('Fiction', "The Midnight Library", 'https://www.goodreads.com/choiceawards/best-fiction-books-2020'))
        # check that the last tuple is made up of the following 3 strings: 'Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'
        self.assertEqual(best_books[19],('Picture Books', 'Antiracist Baby', 'https://www.goodreads.com/choiceawards/best-picture-books-2020'))


    def test_write_csv(self):
        
        # call get_titles_from_search_results on search_results.htm and save the result to a variable
        data = get_titles_from_search_results("search_results.htm")
        # call write csv on the variable you saved and 'test.csv'
        write_csv(data, 'test.csv')
        # read in the csv that you wrote (create a variable csv_lines - a list containing all the lines in the csv you just wrote to above)
        f = open('test.csv', 'r')
        csv_reader = csv.reader(f, delimiter=',')
        lines = [r for r in csv_reader]
        f.close()
        # check that there are 21 lines in the csv
        self.assertEqual(len(lines), 21)
        # check that the header row is correct
        self.assertEqual(lines[0], ['Book title', 'Author Name'])
        # check that the next row is 'Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'
        self.assertEqual(lines[1], ['Harry Potter and the Deathly Hallows (Harry Potter, #7)', 'J.K. Rowling'])
        # check that the last row is 'Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'
        self.assertEqual(lines[-1], ['Harry Potter: The Prequel (Harry Potter, #0.5)', 'J.K. Rowling'])

if __name__ == '__main__':
    
   print(extra_credit("extra_credit.htm"))
   unittest.main(verbosity=2)