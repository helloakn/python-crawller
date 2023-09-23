import os
from dotenv import load_dotenv
load_dotenv()

def getConfig(configName):
  return os.getenv(configName)