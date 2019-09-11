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
    self.pathArticleImage = '../public/assets/content/articles/article-image'
    self.pathThoughtImage = '../public/assets/content/thoughts/thoughts-image'
    self.pathJobImage = '../public/assets/content/jobs/job-image'

  def getTemp(self):
    return self.__temp

  def getTemp2(self):
    return self.__temp2

  def Diff(self, li1, li2):
    return (list(set(li1) - set(li2)))

  def ThumbImgToLocal(self, data, argument):
    ImgToFile = DataHandling()

    tempIMG = []

    if argument == 'article':
      setPathToImage = self.pathArticleImage
    elif argument == 'thought':
      setPathToImage = self.pathThoughtImage
    elif argument == 'job':
      setPathToImage = self.pathJobImage

    pathArticleImageId = setPathToImage + '/' + str(self.__id)
    pathArticleImageIdThumb = pathArticleImageId + '/thumbnail-image.jpg'
    ImgToFile.setPath(pathArticleImageIdThumb)

    soup = BeautifulSoup(data, "html.parser")
    html_img_tags = soup.findAll("img")
    if not html_img_tags:
      value = None
    else:
      if not os.path.isdir(setPathToImage):
        os.mkdir(setPathToImage)
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

  def thoughtToLocal(self, data):
      soup = BeautifulSoup(data, 'html.parser')
      onlyText = soup.get_text()
      onlyText = onlyText.replace('\n', ' ')
      return onlyText

  def forThumbImage(self, key, value, argument):
    if argument == 'article':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument)
      self.__temp[key] = returnedData
      self.__temp2[key] = returnedData

    elif argument == 'thought':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument)
      self.__temp[key] = returnedData

    elif argument == 'job':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument)
      self.__temp[key] = returnedData

  def forOther(self, key, value, argument):
    if argument == 'article':
      self.__temp[key] = value
      self.__temp2[key] = value
    elif argument == 'thought' or argument == 'job':
      if value == '':
        self.__temp[key] = None
      else:
        self.__temp[key] = value

  def loopDataArticle(self, argument):
    for key, value in self.__content.items():
      for key2, value2 in value.items():
        if key2 == 'thumbImage':
          self.forThumbImage(key2, value2, argument)
        elif key2 == 'article':
          self.__temp2[key2] = self.ArticleToLocal(value2)
        elif key2 == 'tag':
          returnedData = self.TagToLocal(value2)
          self.__temp[key2] = returnedData
          self.__temp2[key2] = returnedData
        else:
          self.forOther(key2, value2, argument)

  def loopDataThought(self, argument):
    for key, value in self.__content.items():
      for key2, value2 in value.items():
        if key2 == 'thought':
          self.__temp[key2] = self.thoughtToLocal(value2)
        elif key2 == 'thumbThought':
          self.forThumbImage(key2, value2, argument)
        else:
          self.forOther(key2, value2, argument)

  def looopDataJob(self, argument):
    for key, value in self.__content.items():
      for key2, value2 in value.items():
        if key2 == 'thumbJob':
          self.forThumbImage(key2, value2, argument)
        elif key2 == 'featured':
          self.__temp[key2] = value2
        else:
          self.forOther(key2, value2, argument)
