from paths import Path
from bs4 import BeautifulSoup
import os
import re
import base64
import json

class loopingPUT(Path):

  def __init__(self):
    super().__init__()
    self.__countCurrent = 0
    self.__ImageCount = []
    self.__ImageExcNew = []
    self.__tempSRC = []
    self.__tempListTag = []


  def Diff(self, li1, li2):
    return (list(set(li1) - set(li2)))

  def forArticle(self, data, pathIMG):
    soup = BeautifulSoup(data, 'html.parser')
    html_img_tags = soup.find_all('img')

    listExcThumb = [x for x in os.listdir(pathIMG) if x != 'thumbnail-image.jpg']

    if not html_img_tags:
      for item in listExcThumb:
        os.remove(os.path.join(pathIMG, item))
      return str(soup)
    else:
      tempIMG = [tag['src'] for tag in html_img_tags]

      for found in tempIMG:
        founded = re.search('/(image(\d+).\w+)', found)
        if founded != None:
          self.__ImageExcNew.append(founded.group(1))
          self.__ImageCount.append(int(founded.group(2)))

      diffImage = self.Diff(listExcThumb, self.__ImageExcNew)

      for item in diffImage:
        os.remove(os.path.join(pathIMG, item))

      if(self.__ImageCount):
        self.__countCurrent = max(self.__ImageCount)

      for toLocal in tempIMG:
        img = re.findall(r'base64,(.*)', toLocal, re.I | re.M)
        if not toLocal.startswith('data:image'):
          toLocal = re.search(r'../(\w+.*)', toLocal)
          toLocal = toLocal.group(1)
          toLocal = 'assets/' + toLocal
          self.__tempSRC.append(toLocal)
        elif img:
          self.__countCurrent += 1
          decodeData = base64.b64decode(img[0])
          source = pathIMG + "image" + str(self.__countCurrent) + ".jpg"
          splitSource = re.findall(r'public/(.*)', source, re.I | re.M)
          self.__tempSRC.append(splitSource)
          image_result = open(source, 'wb')
          image_result.write(decodeData)
          image_result.close()

      for iterHTML, iterSRC in zip(html_img_tags, self.__tempSRC):
        iterHTML['src'] = iterSRC
      return str(soup)

  def forThumbImage(self, data, pathFolder, pathIMG):
    soup = BeautifulSoup(data, 'html.parser')
    html_img_tags = soup.find_all('img')

    if not html_img_tags:
      for item in os.listdir(pathIMG):
        if 'thumbnail-image' in item:
          os.remove(pathIMG + 'thumbnail-image.jpg')
    else:
      tempIMG = [tag['src'] for tag in html_img_tags]
      img = re.findall(r'base64,(.*)', tempIMG[0], re.I|re.M)

      if img:
        if not os.path.isdir(pathFolder):
          os.mkdir(pathFolder)

        if not os.path.isdir(pathIMG):
          os.mkdir(pathIMG)

        for item in os.listdir(pathIMG):
          if 'thumbnail-image' in item:
            os.remove(pathIMG + 'thumbnail-image.jpg')

        decodeData = base64.b64decode(img[0])
        source = pathIMG + 'thumbnail-image.jpg'
        splitSource = re.findall(r'public(.*)', source, re.I | re.M)
        image_result = open(source, 'wb')
        image_result.write(decodeData)
        image_result.close()
        return splitSource[0]
      else:
        return tempIMG[0]

  def forTag(self, data, reqID):
    try:
      openTag = open(self.pathArticleTag, 'r+')
      loadData = json.load(openTag)
      splitText = data.split(',')
      unpackLoadData = [x['name'] for x in loadData['tags'] if x['id'] == reqID]
      compareDataValue = self.Diff(unpackLoadData, splitText)
      compareValueData = self.Diff(splitText, unpackLoadData)

      for dataDat in loadData['tags'][:]:
        if dataDat['id'] == reqID:
          if dataDat['name'] in compareDataValue:
            loadData['tags'].remove(dataDat)

      for dataVal in compareValueData:
        tempDict = {}
        tempDict['name'] = dataVal
        tempDict['id'] = reqID
        loadData['tags'].append(tempDict)

      tempDictTag = dict(tags=loadData['tags'])
      openTag.seek(0)
      openTag.truncate()
      openTag.write(json.dumps(tempDictTag))
      openTag.close()
    except IOError:
      openTag = open(self.pathArticleTag, 'w')
      splitText = data.split(',')
      for x in splitText:
        tempTag = {}
        tempTag['name'] = x
        tempTag['id'] = reqID
        self.__tempListTag.append(tempTag)
      tempDictTag = dict(tags=self.__tempListTag)
      openTag.write(json.dumps(tempDictTag))
      openTag.close()

    return data

  def forThought(self, data):
    soup = BeautifulSoup(data, "html.parser")
    onlyText = soup.get_text()
    onlyText = onlyText.replace('\n', ' ')
    return onlyText
