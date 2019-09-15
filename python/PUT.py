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
        returnedData = self.forThumbImage(value, self.pathArticleImage, pathImageById)
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

  def updateThought(self):
    pathImageById = self.pathThoughtImage + '/' + str(self.__id) + '/'

    read_file_outer = open(self.pathThoughtData, 'r+')
    dataThoughtOuter = json.load(read_file_outer)['thoughts']

    selectedThought = next((index for (index, d) in enumerate(dataThoughtOuter) if d['id'] == self.__id))

    for key, value in self.__updateContent['thought'].items():
      if key == 'thumbThought':
        returnedData = self.forThumbImage(value, self.pathThoughtImage, pathImageById)
        self.__temp[key] = returnedData
      elif key == 'thought':
        self.__temp[key] = self.forThought(value)
      else:
        self.__temp[key] = value

    self.__temp['id'] = self.__id

    dataThoughtOuter[selectedThought] = self.__temp

    tempDict = dict(thoughts=dataThoughtOuter)

    read_file_outer.seek(0)
    read_file_outer.truncate()
    read_file_outer.write(json.dumps(tempDict))
    read_file_outer.close()


  def updateJob(self):
    pathImageById = self.pathJobImage + '/' + str(self.__id) + '/'

    read_file_outer = open(self.pathJobData, 'r+')
    dataJobOuter = json.load(read_file_outer)['jobs']

    selectedJob = next((index for (index, d) in enumerate(dataJobOuter) if d['id'] == self.__id))

    for key, value in self.__updateContent['job'].items():
      if key == 'thumbJob':
        if value == None:
          returnedData = value
        else:
          returnedData = self.forThumbImage(value, self.pathJobImage, pathImageById)
        self.__temp[key] = returnedData
      elif key == 'description' or key == 'qualification':
        pass
      elif key == 'specialization':
        value = value.lower()
        self.__temp[key] = value
      else:
        self.__temp[key] = value

    self.__temp['id'] = self.__id

    dataJobOuter[selectedJob] = self.__temp

    tempDict = dict(jobs=dataJobOuter)

    read_file_outer.seek(0)
    read_file_outer.truncate()
    read_file_outer.write(json.dumps(tempDict))
    read_file_outer.close()
