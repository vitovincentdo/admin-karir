from LoopPut import loopingPUT
import json

class put(loopingPUT):

  def __init__(self, id, content):
    super().__init__()
    self.__temp = {}
    self.__temp2 = {}
    self.__id = id
    self.__updateContent = content

  def getID(self):
    return self.__id


  def updateArticle(self):
    pathImageById = self.pathArticleImage + '/' + str(self.__id) + '/'

    read_file_outer = open(self.pathArticleData, 'r+')
    dataArticleOuter = json.load(read_file_outer)['articles']

    read_file_inner = open(self.pathFolderArticle + '/article/' + str(self.__id) + '.json', 'r+')
    dataArticleInner = json.load(read_file_inner)

    selected_article = next((index for (index, d) in enumerate(dataArticleOuter) if d['id'] == self.__id))

    for key, value in self.__updateContent['article'].items():
      if key == 'article':
        self.__temp2[key] = self.forArticle(value, pathImageById)
      elif key == 'thumbImage':
        returnedData = self.forThumbImage(value, pathImageById)
        self.__temp[key] = returnedData
        self.__temp2[key] = returnedData
      elif key == 'tag':
        returnedData = self.forTag(value, self.__id)
        self.__temp[key] = returnedData
        self.__temp2[key] = returnedData
      else:
        self.__temp[key] = value
        self.__temp2[key] = value

    self.__temp['id'] = self.__id
    self.__temp2['id'] = self.__id

    dataArticleOuter[selected_article] = self.__temp
    dataArticleInner['article'] = self.__temp2

    tempDict = dict(articles=dataArticleOuter)

    read_file_outer.seek(0)
    read_file_outer.truncate()
    read_file_outer.write(json.dumps(tempDict))
    read_file_outer.close()

    read_file_inner.seek(0)
    read_file_inner.truncate()
    read_file_inner.write(json.dumps(dataArticleInner))
    read_file_inner.close()
