import os
from dotenv import load_dotenv
load_dotenv()

def getHeader():
  return {'User-Agent': 'Mozilla/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)'}

def getConfig(configName):
  return os.getenv(configName)