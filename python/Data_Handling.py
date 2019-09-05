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

  def writeToFile(self, path, data):
    writeTF = open(path, 'w')
    writeTF.write(json.dumps(data))
    writeTF.close()
