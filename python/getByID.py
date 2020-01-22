from paths import Path
from bs4 import BeautifulSoup
import json

class getById(Path):
  """
  This class is used for getting data from desired requested id.

  Example:

  ```python
  from getByID import getById

  getFromID = getById() #declare getByID
  getFromID.setID(article_id)  #set the desired id, pass it through the parameter in the parentheses
  data = getFromID.getByIdOuter('article')  #get the data based on the id that has been set, pass the argument in the parentheses. the available arguments are 'article', ''thought', or 'job'.
  """

  def __init__(self):
    super().__init__()
    self.innerArticles = self.pathFolderArticle + '/article/'
    self.__id = None
    self.__dictData = None
    self.__selectedUser = None
    self.__data = None

  def setID(self, value):
    self.__id = value

  def getByIdInnerArticle(self):
    count = self.__selectedUser['id']
    read_inner = open(self.innerArticles+str(count)+'.json', 'r')
    dataLoad = json.load(read_inner)
    outFromDict = dataLoad['article']
    for key, value in outFromDict.items():
      if key == 'thumbImage':
        if value != None:
          outFromDict[key] = '<p><img src="' + value + '"/></p>'
        else:
          pass
      elif key == 'article':
        soup = BeautifulSoup(value, "html.parser")
        for img in soup.findAll('img'):
          img['src'] = '/' + img['src']
        outFromDict[key] = str(soup)
    read_inner.close()
    return outFromDict

  def getByIdOuter(self, argument):
    if argument == 'article':
      read_file = open(self.pathArticleData, 'r')
    elif argument == 'thought':
      read_file = open(self.pathThoughtData, 'r')
    elif argument == 'job':
      read_file = open(self.pathJobData, 'r')

    dataLoad = json.load(read_file)

    if argument == 'article':
      self.__dictData = dataLoad['articles']
    elif argument == 'thought':
      self.__dictData = dataLoad['thoughts']
    elif argument == 'job':
      self.__dictData = dataLoad['jobs']

    self.__selectedUser = [item for item in self.__dictData if item['id'] == self.__id]
    self.__selectedUser = self.__selectedUser[0]

    if argument == 'article':
      try:
        self.__data = self.getByIdInnerArticle()
      except:
        pass
    elif argument == 'thought':
      for key, value in self.__selectedUser.items():
        if key == 'thumbThought':
          if value != None:
            self.__selectedUser[key] = '<p><img src="'+value+'"/></p>'
    elif argument == 'job':
      for key, value in self.__selectedUser.items():
        if key == 'thumbJob':
          if value != None:
            self.__selectedUser[key] = '<p><img src="'+value+'"/></p>'

    if(self.__data):
      self.__selectedUser.update(self.__data)

    read_file.close()
    if argument == 'article':
      forResp = dict(articles=self.__selectedUser)
    elif argument == 'thought':
      forResp = dict(thoughts=self.__selectedUser)
    elif argument == 'job':
      forResp = dict(jobs=self.__selectedUser)
    return forResp
