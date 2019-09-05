import json
import os

class Switcher():

  def __init__(self):
    self.pathArticleData = '../public/assets/content/articles/data.json'
    self.pathFolderArticle = '../public/assets/content/articles'
    self.__id = None
    self.__content = None

  def properties(self, argument):
    method_name = argument
    
    # Get the method from 'self'. Default to a lambda.
    method = getattr(self, method_name, lambda: "Invalid month")
    
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
