from bs4 import BeautifulSoup
import requests

BASE_URL = "http://www.imdb.com"
imdb = []

def getHTML(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def getmoviedetails(soup, input):
    retval = ""
    if input == 'summary':
        summary = soup.find('div', class_='summary_text')
        retval = summary.text.strip()
    if input == 'genre':
        inputdata = soup.find_all('div', class_='see-more inline canwrap')[1]
        retval = inputdata.a.text.strip()
    if input == 'duration':
        durationdata = soup.find('div', class_='subtext')
        retval = durationdata.time.text.strip()
    return retval

def getIMDBData(URL, N):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    moviescontent = soup.select('td.titleColumn')
    movie = [a.text for a in soup.select('td.titleColumn a')]
    movie_release_year = [span.text for span in soup.select('td.titleColumn span')]
    links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
    rating = [strong.text for strong in soup.select('td.ratingColumn strong')]
    counter = 0
    for index in range(0, len(moviescontent)):
        if counter == N:
            break
        else:
            counter += 1
            data = {}
            data['title'] = movie[index]
            data['movie_release_year'] = movie_release_year[index]
            data['rating'] = rating[index]
            moviedetails = getHTML(BASE_URL+links[index])
            data['summary'] = getmoviedetails(moviedetails,'summary')
            data['genre'] = getmoviedetails(moviedetails,'genre')
            data['duration'] = getmoviedetails(moviedetails, 'duration')
            imdb.append(data)

    return(imdb)

URL, y = [URL for URL in input("Enter URL and datacount: ").split(",")]
try:
    N = int(y)
    print(getIMDBData(URL, N))
except Exception as e:
    print('Invalid input or network error')

