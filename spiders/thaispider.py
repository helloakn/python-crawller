import json
from lxml.html import fromstring
import requests

from configs import getConfig, getHeader

class ThaiSpider:
  THAI_SITE_URL = getConfig('THAI_SITE_URL')
  HEADERS = getHeader()
  SELECTOR_MAIN_VIDEO_ATAG = '//li[@class="wallet"]/a/@href'
  SELECTOR_DETAIL_VIDEO_ATAG = '//video'
  DATA = []

  def retrieveCategory(self,htmlElement):
    categories = htmlElement.xpath('//div[@class="captures"]/a')
    categoryList = []
    for category in categories:
      categoryList.append(category.text)
    return categoryList

  def outJsonFile(self):
    # tmpJson = json.dumps(self.DATA)
    # print(tmpJson)
    with open('data.json', 'w') as file:
      json.dump(self.DATA, file)
    
  def detailPage(self,detailPage):
    detailPageUrl = self.THAI_SITE_URL + detailPage
    pageRes = requests.get(detailPageUrl,headers=self.HEADERS)
    htmlElement = fromstring(pageRes.text)
    videoTags = htmlElement.xpath(self.SELECTOR_DETAIL_VIDEO_ATAG) 
    detailTitle = htmlElement.xpath('//title') 
    categories = self.retrieveCategory(htmlElement)
    for videoElement in videoTags:
      videoSourceElement = videoElement.xpath('//source')
      for source in videoSourceElement:
        x = dict(
            title = detailTitle[0].text, 
            poster = videoElement.attrib['poster'], 
            detailUrl =  detailPageUrl, 
            source =  source.attrib['src'],
            categories = categories
        )
        self.DATA.append(x)
    
  def crawl(self):
    siteUrl = self.THAI_SITE_URL
    pageRes = requests.get(siteUrl,headers=self.HEADERS)

    htmlElement = fromstring(pageRes.text)
    aTags = htmlElement.xpath(self.SELECTOR_MAIN_VIDEO_ATAG) 
    for detailPageUrl in aTags:
      self.detailPage(detailPageUrl)
    self.outJsonFile()
