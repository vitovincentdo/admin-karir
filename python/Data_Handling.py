import json

class DataHandling:
  """
  This class is used for saving data into the path folder.

=============================================================================================
  Example saving image:

  ```python
  from Data_Handling import dataHandling

  imgToFile = dataHandling() #declare dataHandling
  imgToFile.setPath(pathToImage) #set the path to image file
  imgToFile.setData(dataImageToBeWrittenToImage) set the base64 encoded data to be written
  imgToFile.saveIMGToLocal() #write the data to file
=============================================================================================
  Example saving data to json:

  ```python
  from Data_handling import dataHandling

  forData = dataHandling()  #declare dataHandling

  forData.writeOuter(pathToOuterJsonData, data, 'article')  #write to outer argument folder. the first parameter is the path to the folder, second parameter is the data to be written, and the last parameter is the argument to thrown it could be 'article', 'thought', or 'job'.

  forData.writeInner(pathToInnerJsonData, data)  #write to inner article folder. the first parameter is the path to article folder, and the second parameter is the data to be written
  =============================================================================================
  """
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
