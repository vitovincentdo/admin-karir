from POST import post
from switcher import Switcher
from Data_Handling import DataHandling
from getByID import getById
import os


def toReturnID():
  forSwitching = Switcher()
  return forSwitching.getID()

def forArticle(content, argument):
  forSwitching = Switcher()
  forData = DataHandling()

  forSwitching.setContent(content)
  forSwitching.properties(argument)

  forLooping = post(forSwitching.getID(), forSwitching.getContent())
  forLooping.loopDataArticle('article')

  if not os.path.isdir(forSwitching.pathFolderArticle+'/article'):
    os.mkdir(forSwitching.pathFolderArticle+'/article')
  else:
    pass

  forData.writeeOuter(forSwitching.pathArticleData, forLooping.getTemp(), 'article')
  forData.writeInner(forSwitching.pathFolderArticle+'/article/'+str(forSwitching.getID())+'.json', forLooping.getTemp2())


def forThought(content, argument):
  forSwitching = Switcher()
  forData = DataHandling()

  forSwitching.setContent(content)
  forSwitching.properties(argument)


  forLooping = post(forSwitching.getID(), forSwitching.getContent())
  forLooping.loopDataThought('thought')

  forData.writeeOuter(forSwitching.pathThoughtData, forLooping.getTemp(), 'thought')

def forJob(content, argument):
  forSwitching = Switcher()
  forData = DataHandling()

  forSwitching.setContent(content)
  forSwitching.properties(argument)

  forLooping = post(forSwitching.getID(), forSwitching.getContent())
  forLooping.looopDataJob('job')

  forData.writeeOuter(forSwitching.pathJobData, forLooping.getTemp(), 'job')

def getDataById(id, argument):
  getfromId = getById()
  getfromId.setID(id)

  resp = getfromId.getByIdOuter(argument)

  return resp
