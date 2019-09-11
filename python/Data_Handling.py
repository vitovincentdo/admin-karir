import json

class DataHandling:
  def __init__(self):
    self.__path = None
    self.__data = None

  def properties(self, to, *params):
    return getattr(self, 'set'+to)(*params)

  def setPath(self, path):
    self.__path = path

  def setData(self, data):
    self.__data = data

  def SaveIMGToLocal(self):
    image_result = open(self.__path, 'wb')
    image_result.write(self.__data)
    image_result.close()

  def writeeOuter(self, path, content, argument):
    file = open(path, 'r+')

    try:
      data = json.load(file)
      if argument == 'article':
        unloadData = data['articles']
      elif argument == 'thought':
        unloadData = data['thoughts']
      elif argument == 'job':
        unloadData = data['jobs']
      unloadData.append(content)
      tempToList = unloadData
    except:
      tempToList = [content]

    if argument == 'article':
      tempDict = dict(articles=tempToList)
    elif argument == 'thought':
      tempDict = dict(thoughts=tempToList)
    elif argument == 'job':
      tempDict = dict(jobs=tempToList)

    file.seek(0)
    file.truncate()
    file.write(json.dumps(tempDict))
    file.close()

  def writeInner(self, path, content):
    innerFile = open(path, 'w')
    tempDict = dict(article=content)

    innerFile.write(json.dumps(tempDict))
    innerFile.close()
