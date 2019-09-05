from bs4 import BeautifulSoup
from Data_Handling import DataHandling
import base64
import json
import os
import re


class looping():
  def __init__(self, id, content):
    self.__temp = {}
    self.__temp2 = {}
    self.__id = id
    self.__content = content

  def getTemp(self):
    return self.__temp

  def getTemp2(self):
    return self.__temp2

  def Diff(self, li1, li2):
    return (list(set(li1) - set(li2)))

  def ThumbImgToLocal(self, data):
    ImgToFile = DataHandling()

    tempIMG = []
    pathArticleImage = '../public/assets/content/articles/article-image'
    pathArticleImageId = pathArticleImage + '/' + str(self.__id)
    pathArticleImageIdThumb = pathArticleImageId + '/thumbnail-image.jpg'
    ImgToFile.setPath(pathArticleImageIdThumb)

    soup = BeautifulSoup(data, "html.parser")
    html_img_tags = soup.findAll("img")
    if not html_img_tags:
      value = None
    else:
      if not os.path.isdir(pathArticleImage):
        os.mkdir(pathArticleImage)
      if not os.path.isdir(pathArticleImageId):
        os.mkdir(pathArticleImageId)
      for tag in html_img_tags:
        tempIMG.append(tag['src'])
      img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
      decodeData = base64.b64decode(img[0])
      ImgToFile.setData(decodeData)
      ImgToFile.SaveIMGToLocal()
      splitSource = re.findall(r'public(.*)', pathArticleImageIdThumb, re.I | re.M)
      value = splitSource[0]
    return value

  def ArticleToLocal(self, data):
    ImgToFile = DataHandling()

    count = 1
    tempIMG = []
    tempSRC = []
    pathArticleImage = '../public/assets/content/articles/article-image'
    pathArticleImageId = pathArticleImage + '/' + str(self.__id)
    pathArticleImageIdImages = pathArticleImageId + '/image'

    if data:
      soup = BeautifulSoup(data, "html.parser")
      html_img_tags = soup.findAll("img")
      if not html_img_tags:
        value = data
      else:
        if not os.path.isdir(pathArticleImage):
          os.mkdir(pathArticleImage)
        if not os.path.isdir(pathArticleImageId):
          os.mkdir(pathArticleImageId)

        for tag in html_img_tags:
          tempIMG.append(tag['src'])

        for toLocal in tempIMG:
          pathForImages = pathArticleImageIdImages + str(count) + '.jpg'
          ImgToFile.setPath(pathForImages)
          img = re.findall(r'base64,(.*)', toLocal, re.I | re.M)
          decodeData = base64.b64decode(img[0])
          ImgToFile.setData(decodeData)
          ImgToFile.SaveIMGToLocal()

          splitSource = re.findall(r'public/(.*)', pathForImages, re.I | re.M)
          tempSRC.append(splitSource)
          count += 1
        for iterHTML, iterSRC in zip(html_img_tags, tempSRC):
          iterHTML['src'] = iterSRC
        value = str(soup)
    else:
      value = None
    return value

  def TagToLocal(self, data):
    path = '../public/assets/content/articles/tag.json'
    tempListTag = []
    if data:
      try:
        openTag = open(path, 'r+')
        loadData = json.load(openTag)
        unpackTags = loadData['tags']
        try:
          splitText = data.split(',')
        except IOError:
          splitText = data
        unpackLoadData = [value['name'] for value in unpackTags if value['id'] == self.__id]
        compareDataValue = self.Diff(unpackLoadData, splitText)
        compareValueData = self.Diff(splitText, unpackLoadData)

        for dataDat in unpackTags[:]:
          if dataDat['id'] == self.__id:
            if dataDat['name'] in compareDataValue:
              unpackTags.remove(dataDat)

        for dataVal in compareValueData:
          tempDict = {}
          tempDict['name'] = dataVal
          tempDict['id'] = self.__id
          unpackTags.append(tempDict)

        tempDictTag = dict(tags=unpackTags)
        openTag.seek(0)
        openTag.truncate()
        openTag.write(json.dumps(tempDictTag))
        openTag.close()
      except IOError:
        openTag = open(path, 'w')
        try:
          splitText = data.split(',')
        except IOError:
          splitText = data
        for x in splitText:
          tempTag = {}
          tempTag['name'] = x
          tempTag['id'] = self.__id
          tempListTag.append(tempTag)
        tempDictTag = dict(tags=tempListTag)
        openTag.write(json.dumps(tempDictTag))
        openTag.close()
      value = data
    else:
      value = None
    return value

  def forThumbImage(self, key, value):
    self.__temp[key] = self.ThumbImgToLocal(value)
    self.__temp2[key] = self.ThumbImgToLocal(value)

  def forArticle(self, key, value):
    self.__temp2[key] = self.ArticleToLocal(value)

  def forTag(self, key, value):
    self.__temp[key] = self.TagToLocal(value)
    self.__temp2[key] = self.TagToLocal(value)

  def forOther(self, key, value):
    self.__temp[key] = value
    self.__temp2[key] = value

  def loopData(self):
    for key, value in self.__content.items():
      for key2, value2 in value.items():
        if key2 == 'thumbImage':
          self.forThumbImage(key2, value2)
        elif key2 == 'article':
          self.forArticle(key2, value2)
        elif key2 == 'tag':
          self.forTag(key2, value2)
        else:
          self.forOther(key2, value2)
