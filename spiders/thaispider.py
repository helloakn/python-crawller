from lxml.html import fromstring
import requests

from configs import getConfig

class ThaiSpider:
  THAI_SITE_URL = getConfig('THAI_SITE_URL')
  def crawl(self):
    print(self.THAI_SITE_URL)