import sys

from spiders import ThaiSpider
def switch(case):
    if case == "thai":
      thaispider = ThaiSpider()
      thaispider.crawl()

if __name__ == "__main__":  
  if len(sys.argv)>1:
    switch(sys.argv[1])