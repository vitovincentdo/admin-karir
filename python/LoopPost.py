from bs4 import BeautifulSoup
from Data_Handling import DataHandling
from paths import Path
import base64
import json
import os
import re


class loopingPOST(Path):
  def __init__(self):
    super().__init__()
    # self.__temp = {}
    # self.__temp2 = {}
    # self.__id = id
    # self.__content = content

  # def getTemp(self):
  #   return self.__temp
  #
  # def getTemp2(self):
  #   return self.__temp2

  def Diff(self, li1, li2):
    return (list(set(li1) - set(li2)))

  def ThumbImgToLocal(self, data, argument, selectedID):
    ImgToFile = DataHandling()

    tempIMG = []

    if argument == 'article':
      setPathToImage = self.pathArticleImage
    elif argument == 'thought':
      setPathToImage = self.pathThoughtImage
    elif argument == 'job':
      setPathToImage = self.pathJobImage

    pathArticleImageId = setPathToImage + '/' + str(selectedID)
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

  def ArticleToLocal(self, data, selectedID):
    ImgToFile = DataHandling()

    count = 1
    tempIMG = []
    tempSRC = []
    pathArticleImage = '../public/assets/content/articles/article-image'
    pathArticleImageId = pathArticleImage + '/' + str(selectedID)
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

  def TagToLocal(self, data, selectedID):
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
        unpackLoadData = [value['name'] for value in unpackTags if value['id'] == selectedID]
        compareDataValue = self.Diff(unpackLoadData, splitText)
        compareValueData = self.Diff(splitText, unpackLoadData)

        for dataDat in unpackTags[:]:
          if dataDat['id'] == selectedID:
            if dataDat['name'] in compareDataValue:
              unpackTags.remove(dataDat)

        for dataVal in compareValueData:
          tempDict = {}
          tempDict['name'] = dataVal
          tempDict['id'] = selectedID
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
          tempTag['id'] = selectedID
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
