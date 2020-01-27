from POST.LoopPost import loopingPOST
from Component.Data_Handling import DataHandling
import os

class post(loopingPOST):
  """
  This class is used for creating article, thought, or job.

=============================================================================================
  Example creating article/thought/job:

  ```python
  from POST.POST import post  #import post

  forHandlingData = post()  #declare post

  1. forHandlingData.POSTArticle(articleID, ArticleContent, 'article')
  2. forHandlingData.POSThought(ThoughtID, ThoughtContent, 'thought')
  3. forHandlingData.POSTJob(JobID, JobContent, 'job')
  From above, number 1-3 are the examples of creating/post some article/thought/job, this function require three parameters. The first parameter is the ID for the article/thought/job, the second parameter is the article/thought/job content that want to be created, and the third parameter is the argument to be thrown it could be 'article'/'thought'/'job'.
===============================================================================================================================
  there also forThumbImage and forOther functions in this class, it is used in the POSTArticle, POSTThought, and POSTJob for handling image data or text data.
  Example on using forThumbImage/forOther:

  self.forThumbImage(key2, value2, id, argument)  #self is used for using function/variable in the child/same class. this function require four parameters. The first parameter and second parameter is the key('thumbImage'/'thumbThought'/'thumbJob') and value(the image data in base64 decoded string) as in python dictionaries, then the third is the id of the article/thought/job, and the fourth parameter is the argumen to be thrown('article'/'thought'/'job')

  self.forOther(key2, value2, argument)  #this is used for handling all data except the image data. the different from above is it dont need the third parameter which is the id.
===============================================================================================================================
  """
  def __init__(self):
    super().__init__()
    self.__temp = {}
    self.__temp2 = {}


  def POSTArticle(self, id, content, argument):
    forData = DataHandling()
    for key, value in content.items():
      for key2, value2 in value.items():
        if key2 == 'thumbImage':
          self.forThumbImage(key2, value2, id, argument)
        elif key2 == 'article':
          self.__temp2[key2] = self.ArticleToLocal(value2, id)
        elif key2 == 'tag':
          returnedData = self.TagToLocal(value2, id)
          self.__temp[key2] = returnedData
          self.__temp2[key2] = returnedData
        else:
          self.forOther(key2, value2, argument)

    if not os.path.isdir(self.pathFolderArticle + '/article'):
      os.mkdir(self.pathFolderArticle + '/article')
    else:
      pass

    forData.writeeOuter(self.pathArticleData, self.__temp, 'article')
    forData.writeInner(self.pathFolderArticle+'/article/'+str(id)+'.json', self.__temp2)

  def POSThought(self, id, content, argument):
    forData = DataHandling()

    for key, value in content.items():
      for key2, value2 in value.items():
        if key2 == 'thought':
          self.__temp[key2] = self.thoughtToLocal(value2)
        elif key2 == 'thumbThought':
          self.forThumbImage(key2, value2, id, argument)
        else:
          self.forOther(key2, value2, argument)

    forData.writeeOuter(self.pathThoughtData, self.__temp, argument)

  def POSTJob(self, id, content,  argument):
    forData = DataHandling()

    for key, value in content.items():
      for key2, value2 in value.items():
        if key2 == 'thumbJob':
          self.forThumbImage(key2, value2, id, argument)
        elif key2 == 'featured':
          self.__temp[key2] = value2
        else:
          self.forOther(key2, value2, argument)

    forData.writeeOuter(self.pathJobData, self.__temp, argument)

  def forThumbImage(self, key, value, id, argument):
    if argument == 'article':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument, id)
      self.__temp[key] = returnedData
      self.__temp2[key] = returnedData

    elif argument == 'thought':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument, id)
      self.__temp[key] = returnedData

    elif argument == 'job':
      if value == None:
        returnedData = value
      else:
        returnedData = self.ThumbImgToLocal(value, argument, id)
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
