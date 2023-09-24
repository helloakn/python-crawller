import json
from lxml.html import fromstring, etree
import requests

from configs import getConfig, getHeader

class ThaiSpider:
  THAI_SITE_URL = getConfig('THAI_SITE_URL')
  HEADERS = getHeader()
  #SELECTOR_MAIN_VIDEO_ATAG = '//li[@class="wallet"]/a/@href'
  SELECTOR_MAIN_VIDEO_ATAG = '//li[@class="wallet"]/a'
  SELECTOR_MAIN_VIDEO_TIME = '//a/div/div[@class="domina nymph"]'
  SELECTOR_DETAIL_VIDEO_ATAG = '//video'
  SELECTOR_PAGINATION = '//div[@id="pagination"]/span/a[@target="_self"][text()!="Next"][last()]'
  DATA = []

  def purifyUrl(self,url):
    return url.replace('//','/').replace(':/','://')
  
  def retrieveCategory(self,htmlElement):
    categories = htmlElement.xpath('//div[@class="captures"]/a')
    categoryList = []
    for category in categories:
      categoryList.append(category.text)
    return categoryList

  def outJsonFile(self):
    with open('data.json', 'w') as file:
      json.dump(self.DATA, file)
    
  def detailPage(self,detailPage,videoLength):
    detailPageUrl = self.purifyUrl(self.THAI_SITE_URL + detailPage)
    print("   detail page => "+detailPageUrl)
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
            videoLength = videoLength,
            categories = categories
        )
        self.DATA.append(x)

  def paginationPage(self,pageNum):
    siteUrl = self.purifyUrl(self.THAI_SITE_URL+"/"+str(pageNum))
    print("page at => "+ siteUrl)
    pageRes = requests.get(siteUrl,headers=self.HEADERS)

    htmlElement = fromstring(pageRes.text)
    aTags = htmlElement.xpath(self.SELECTOR_MAIN_VIDEO_ATAG) 
    for detailPageElement in aTags:
      vElement = fromstring(etree.tostring(detailPageElement))
      self.detailPage(detailPageElement.attrib['href'],vElement.xpath(self.SELECTOR_MAIN_VIDEO_TIME)[0].text)

  def mainPage(self):
    siteUrl = self.THAI_SITE_URL
    htmlResponse = requests.get(siteUrl,headers=self.HEADERS)
    htmlElement = fromstring(htmlResponse.text)
    paginationElements = htmlElement.xpath(self.SELECTOR_PAGINATION) 
    for x in range(1,int(paginationElements[0].text)+1):
      self.paginationPage(x)

  def crawl(self):
    self.mainPage()
    # siteUrl = self.THAI_SITE_URL
    # pageRes = requests.get(siteUrl,headers=self.HEADERS)

    # htmlElement = fromstring(pageRes.text)
    # aTags = htmlElement.xpath(self.SELECTOR_MAIN_VIDEO_ATAG) 
    # for detailPageUrl in aTags:
    #   self.detailPage(detailPageUrl)
    self.outJsonFile()
