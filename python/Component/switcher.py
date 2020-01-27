from Component.paths import Path
import json
import os

class Switcher(Path):
  """
  This class is used for setting an id between the data that exist and not exist.

  Example:

  ```python
  from POST.switcher import Switcher

  forSwitching = Switcher()  #declare Switcher function

  forSwitching.setContent(data)  #setting the data that want to be POST
  forSwitching.properties('articleExist/articleNotExist')  #if the thrown argument is 'article/thought/jobExist' it will set the id to the last known id in the article/thought/job data plus 1. if the thrown argument is 'article/thought/jobNotExist' it will set the id to 1

  forSwitching.getID()  #call the id that has been set by the properties
  forSwitching.getContent()  #call the content value that have been set

  """

  def __init__(self):
    super().__init__()
    self.__id = None
    self.__content = None

  def properties(self, argument):
    method_name = argument
    
    # Get the method from 'self'. Default to a lambda.
    method = getattr(self, method_name, lambda: "Invalid Argument")
    
    # Call the method as we return it
    return method()


  def setContent(self, value):
    self.__content = value

  def getContent(self):
    return self.__content

  def getID(self):
    return self.__id

  def articleExist(self):
    file = open(self.pathArticleData,'r')
    data = json.load(file)
    unloadArticles = data['articles']

    lookID = []
    try:
      for loop in unloadArticles:
        lookID.append(loop['id'])
      self.__content['article']['id'] = max(lookID) + 1
    except:
      self.__content['article']['id'] = 1

    self.__id = self.__content['article']['id']

    file.close()


  def articleNotExist(self):
    if not os.path.isdir(self.pathFolderArticle):
      os.mkdir(self.pathFolderArticle)

    file = open(self.pathArticleData, 'w')
    self.__content['article']['id'] = 1
    self.__id = self.__content['article']['id']

    file.close()

  def thoughtExist(self):
    file = open(self.pathThoughtData, 'r')
    data = json.load(file)
    unloadThoughts = data['thoughts']

    lookID = []
    try:
      for loop in unloadThoughts:
        lookID.append(loop['id'])
      self.__content['thought']['id'] = max(lookID) + 1
    except:
      self.__content['thought']['id'] = 1

    self.__id = self.__content['thought']['id']

    file.close()

  def thoughtNotExist(self):
    if not os.path.isdir(self.pathFolderThought):
      os.mkdir(self.pathFolderThought)

    file = open(self.pathThoughtData, 'w')
    self.__content['thought']['id'] = 1
    self.__id = self.__content['thought']['id']

    file.close()

  def jobExist(self):
    file = open(self.pathJobData, 'r')
    data = json.load(file)
    unloadJobs = data['jobs']

    lookID = []
    try:
      for loop in unloadJobs:
        lookID.append(loop['id'])
      self.__content['job']['id'] = max(lookID) + 1
    except:
      self.__content['job']['id'] = 1

    self.__id = self.__content['job']['id']

    file.close()

  def jobNotExist(self):
    if not os.path.isdir(self.pathFolderJob):
      os.mkdir(self.pathFolderJob)

    file = open(self.pathJobData, 'w')
    self.__content['job']['id'] = 1
    self.__id = self.__content['job']['id']

    file.close()
