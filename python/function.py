# from classes import
from bs4 import BeautifulSoup
import os
import re
import base64
import json

class Json:
  def __init__(self, path, data):
    self.path = path
    self.data = data
  def SaveIMGToLocal(self):
    image_result = open(self.path, 'wb')
    image_result.write(self.data)
    image_result.close()
  def writeToFile(self):
    writeTF = open(self.path, 'w')
    writeTF.write(json.dumps(self.data))
    writeTF.close()


# class forLoop:
#   def __init__(self, temp, temp2, id):
#     # self.content = content
#     self.temp = temp
#     self.temp2 = temp2
#     self.id = id
#   def forThumbImage(self, key, value):
#     if key == 'thumbImage':
#       self.temp[key] = ThumbImgToLocal(value, self.id)
#       self.temp2[key] = ThumbImgToLocal(value, self.id)
#   def forArticle(self, key, value):
#     if key == 'article':
#       self.temp2[key] = ArticleToLocal(value, self.id)
#   def forTag(self, key, value):
#     if key == 'tag':
#       self.temp[key] = TagToLocal(value, self.id)
#       self.temp2[key] = TagToLocal(value, self.id)
#   def forOther(self, key, value):
#     if key != 'thumbImage' and key != 'article' and key != 'tag':
#       self.temp[key] = value
#       self.temp2[key] = value

def loopData(content, temp, temp2, id):
  declareObj = forLoop(temp, temp2, id)
  for key, value in content.items():
    for key2, value2 in value.items():
      declareObj.forThumbImage(key2,value2)
      declareObj.forArticle(key2, value2)
      declareObj.forTag(key2, value2)
      declareObj.forOther(key2, value2)
