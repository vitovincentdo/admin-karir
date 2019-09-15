from LoopPost import loopingPOST

class post(loopingPOST):

  def __init__(self, id, content):
    super().__init__()
    self.__temp = {}
    self.__temp2 = {}
    self.__id = id
    self.__content = content

  def getTemp(self):
    return self.__temp

  def getTemp2(self):
    return self.__temp2

  def forThumbImage(self, key, value, argument):
    if argument == 'article':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument, self.__id)
      self.__temp[key] = returnedData
      self.__temp2[key] = returnedData

    elif argument == 'thought':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument, self.__id)
      self.__temp[key] = returnedData

    elif argument == 'job':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument, self.__id)
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
          self.__temp2[key2] = self.ArticleToLocal(value2, self.__id)
        elif key2 == 'tag':
          returnedData = self.TagToLocal(value2, self.__id)
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
