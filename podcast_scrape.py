from bs4 import BeautifulSoup
import requests
import sys
import xlrd
import sys
import xlwt
import urllib2
import re
import urllib3


# import requests.packages.urllib3
# requests.packages.urllib3.disable_warnings()


class Scrape:
    def __init__(self):
        episode_title = []
        episode_description = []
        episode_release_date = []

    Soup = BeautifulSoup

    episode_title = []
    episode_description = []
    episode_release_date = []

    link1 = 'http://www.itunescharts.net/us/charts/podcasts/2017/10/17'
    soup1 = BeautifulSoup(requests.get(link1).text, "lxml")

    def find_podcast(self, podcast_title, soup=soup1):

        pod = soup.find('a', text=podcast_title, href=True)
        pod['href']

        # Episode Title
        print pod.string
        self.episode_title.append(pod.string)

        # Episode Release Date
        release = "http://www.itunescharts.net" + pod['href']
        soup = BeautifulSoup(requests.get(release).text, "lxml")
        release_date = soup.find(text=re.compile('Release date: '))
        release_date = release_date.find_parents('li')
        print release_date[0].find('span').contents[0]
        self.episode_release_date.append(release_date[0].find('span').contents[0])

        # Episode Description

        if (soup.find(text=re.compile('About This Podcast'))):
            about = soup.find(text=re.compile('About This Podcast'))
            description = about.find_next("div").contents[1].contents[0]

        elif (soup.find(text=re.compile('Summary:'))):
            about = soup.find(text=re.compile('Summary:'))
            description = about.find_parents('strong')[0].find_parent("div").find('p').contents[1]

        print description
        self.episode_description.append(description)
        return 0

    def export_podcast(self):
        book = xlwt.Workbook(encoding="utf-8")
        sheet1 = book.add_sheet("Form 4 Data")

        # Label destination sheet the same way SEC form 4s are labeled
        sheet1.write(0, 0, "Episode Title")
        sheet1.write(0, 1, "Episode Description")
        sheet1.write(0, 2, "Episode Release Date")

        n = 0
        while n < len(self.episode_title):
            sheet1.write(n + 1, 0, self.episode_title[n])
            sheet1.write(n + 1, 1, self.episode_description[n])
            sheet1.write(n + 1, 2, self.episode_release_date[n])
            n += 1

        book.save("/media/mokeam/Drive 25/PodSource/podcasts.xls")

        print "Printing Finished!"


scrape = Scrape()
scrape.find_podcast('Snap Judgment Presents: Spooked')
scrape.find_podcast('The Hilarious World of Depression')
scrape.find_podcast('Dan Carlin\'s Hardcore History')
scrape.find_podcast('Happiness Podcast')
scrape.find_podcast('WTF with Marc Maron Podcast')
scrape.find_podcast('The Tim Ferriss Show')
scrape.find_podcast('Up and Vanished')
scrape.find_podcast('The Dave Ramsey Show')
scrape.find_podcast('Something You Should Know')
scrape.find_podcast('Sword and Scale')
# scrape.find_podcast('Oprah&#8217;s SuperSoul Conversations')
scrape.export_podcast()
