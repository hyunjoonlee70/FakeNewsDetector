# This file extracts the main text of the article given the url to the article.
import requests
from bs4 import BeautifulSoup
import string
import os

# Given a link, returns a list of paragraphs.
def extractor(link):
    page = requests.get(link)

    if page.status_code is not 200:
        print "Failed to get the article."
        return

    content = page.content

    soup = BeautifulSoup(page.content, 'html.parser')
    # Isolating the type list. Storing the information in
    # a certain article page by simply checking the tags.
    type_list = [type(item) for item in list(soup.children)]
    soup = BeautifulSoup(page.content, 'html.parser')
    # p_list = soup.find_all('p', class_='story-body-text story-content')
    p_list = soup.find_all('p')
    result = []
    for i in p_list:
        temp_string = ""
        for c in i.get_text():
            if c in string.printable:
                temp_string += c
        result.append(temp_string)

    return result


def addAllParagraphs(p_list):
    result = ""

    for i in p_list:
        result += i

    # after getting the result, we need to write it to another file.
    fd = open("out.txt", "w")
    fd.write(result.rstrip('\n\p'))
    fd.close()

def main():
	fd = open("url.txt", "r")
	url = fd.read()
	fd.close()
	os.remove("url.txt")
	result = extractor(url)
	addAllParagraphs(result)

if __name__ == '__main__':
    main()
    os.system("python fakenewsAnalysis.py")
    with open('result.txt', 'r') as myfile:
		boolean = myfile.read()
    if boolean == "True":
        os.system("javac FakeNewsPop.java")
        os.system("java FakeNewsPop")
