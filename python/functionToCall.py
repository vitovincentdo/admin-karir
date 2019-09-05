from ForEachLoop import looping
from switcher import Switcher
# from Data_Handling import DataHandling
import os
import json

def forArticle(content, argument):
  forSwitching = Switcher()

  forSwitching.setContent(content)

  if argument == 'articleExist':
    forSwitching.properties('articleExist')
  elif argument == 'articleNotExist':
    forSwitching.properties('articleNotExist')

  forLooping = looping(forSwitching.getID(), forSwitching.getContent())
  forLooping.loopData()

  if not os.path.isdir(forSwitching.pathFolderArticle+'/article'):
    os.mkdir(forSwitching.pathFolderArticle+'/article')
  else:
    pass

  file = open(forSwitching.pathArticleData, 'r+')
  innerFile = open(forSwitching.pathFolderArticle+'/article/'+str(forSwitching.getID())+'.json', 'w')

  try:
    data = json.load(file)
    unloadArticles = data['articles']
    unloadArticles.append(forLooping.getTemp())
    tempToList = unloadArticles
    print("masuk situ")
  except:
    print("masuk sini")
    tempToList = [forLooping.getTemp()]

  print(tempToList)
  tempDict = dict(articles=tempToList)
  tempDict2 = dict(article=forLooping.getTemp2())

  file.seek(0)
  file.truncate()
  file.write(json.dumps(tempDict))

  innerFile.write(json.dumps(tempDict2))

  file.close()
  innerFile.close()
