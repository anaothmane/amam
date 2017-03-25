"""
Author:Bret Nestor
Project: Sustaware Sentient Mapping

This is the section of code that defines the spider and text extractor to array.
The start and allowed domains are contained within the script
The site-specific scraping may need to be changed to suit the different websites.

From command prompt navigate to root folder.
Once in the root folder, the command is is scrapy crawl 'name'

Work remaining:
1) scrape comments and create a dictionary of name, comment, location (if present), time, number of likes, number of dislikes
2) Modify the Dict so that it only contains information on Refugee stories
3) pass Dict to Goslate library.

"""

import numpy
import Sentiment
import time
import urllib
# import requests
import json
import csv

#from scrapy.spider import BaseSpider
from scrapy.spiders import CrawlSpider, Rule
#from scrapy.selector import HtmlXPathSelector
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
#from refugee_scrape.items import RefugeeScrapeItem

Location_ref={} #define the global dictionary


"""
This function finds articles that meet the criteria for comments based on the Dailymail URL
"""
def FindArticle(str):
  index = 0
  while index < len(str):
    if str[index:index+5] == 'reute': #specific for daily mail. Reuters articles do not have comments
      return -1
    if str[index:index+5] == 'icle-':
      return str[index+5:index+12]
    index = index + 1
  return -1


"""
Class which defines the spider name and parameters in the html
"""
class MySpider(CrawlSpider):
  name="Dailymail" #this is the name you must use to execute the script
  allowed_domains=["dailymail.co.uk"]
  start_urls=["http://www.dailymail.co.uk/home/search.html?sel=site&searchPhrase=refugee"]
  filters_or=['refugee', 'migrant']#regex refugee?
  rules=(Rule(LinkExtractor(allow=filters_or),callback='parse_item'),)
  dateCreated = []
  message = []
  userLocation = []
  replies = []
  #  print 'yaaay:)'
  """
  Dailymail has a api for its comments to simplify the scraping.
  Take the article ID # and plug it into the API
  """
  def parse_item(self, response):
    hxs=Selector(response)#deprecated function use scrapy.Selector instead
    self.logger.info('%s',response.url)
    articleforapi=FindArticle(response.url)
    if articleforapi==-1:
      return
    url_var="http://www.dailymail.co.uk/reader-comments/p/asset/readcomments/xxxxxxx?max=500&order=desc"
    URL_scrape=url_var[:64]+str(articleforapi)+url_var[71:]
    x=urllib.urlopen(URL_scrape)
    jsonResponse=json.loads(x.read())
    responses = jsonResponse["payload"]["page"] #creates a list does this append?
    for response in responses:
      #print"**************************     start    ***********************************"
      dateCreated=response["dateCreated"]
      message=response["message"]
      userLocation=response["userLocation"]
      voteRating=response["voteRating"]
      voteCount=response["voteCount"]
      assetHeadline=response["assetHeadline"]
      assetUrl=response["assetUrl"]
      
      #print response

      dateCreated=dateCreated.replace('-','/').replace('T',',') #format the time stamp
      assetHeadline=assetHeadline.replace(',','').replace(':',' ') #filter so that csv file will be successful
      message=message.replace(',','').replace('\n',' ').replace('\r\n',' ')
      userLocation=userLocation.replace(',','')
      row=str(dateCreated)+ "," + str(message)+ "," + str(userLocation)+ "," + str(voteRating)+ "," + str(voteCount)+ "," + str(assetHeadline)+ "," + str(assetUrl)

      f=open(r'C:\Python27\refugee_scrape\refugee_scrape\spiders\sentimentfile.csv','a+') #write file to this directory FOR BRETS CPU
      f.write(str(row)+'\n')
      f.close


      """
The remaining code was implemented in a new script file so that we can try multiple sentiment analysis techniques
"""
##      splitter = Sentiment.Splitter()
##      postagger = Sentiment.POSTagger()
##      dicttagger = Sentiment.DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml', 'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])
##      splitted_sentences = splitter.split(message)
##      # pprint(splitted_sentences)
##
##      pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
##      # pprint(pos_tagged_sentences)
##
##      dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
##      # pprint(dict_tagged_sentences)
##
##      print("analyzing sentiment...")
##      score = Sentiment.sentiment_score(dict_tagged_sentences)
##      print(score)
      #Import file for relevance library.
      #test if library words are in the comment or story
      #if true apply NLP to comment string
      #Apply weighting
      #Call geo coding library
      #extract GPS coordinatess
      #end
      #apply localization and regional weighting techniques
      #record sample average standard deviation and population?
      #How do we normalize opinions?
      #append the final matrix to be exported
      #export Panda format. servers? temporary maps?
      #print response["userAlias"]
      #print "****************************    end    ***********************************"
      #file output into .csv
      ##geovis.SetMapZoom(x2x=[0,180],y2y=[0,90])
      ### 2 DATA
      ##countrylayer = geovis.Layer("C:/polygons_shapefile.shp")
      ##countrylayer.AddClassification(symboltype="fillcolor", valuefield="pop_est", symbolrange=[geovis.Color("white"),geovis.Color("red", intensity=0.9, brightness=0.8),geovis.Color("red", intensity=0.9, brightness=0.5)], classifytype="natural breaks", nrclasses=3)
      ### 3 MAP
      ##newmap = geovis.NewMap()
      ##newmap.AddToMap(countrylayer)
      ##newmap.AddLegend(countrylayer, upperleft=(0.03,0.15), bottomright=(0.6,0.4))
      ##newmap.AddText(relx=0.5, rely=0.05, text="Population, by Country", textsize=0.1, textanchor="n", textboxfillcolor=geovis.Color("white"))
      ##newmap.ViewMap()
