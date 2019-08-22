import json
import os
path = '../public/assets/content/articles/data.json'
path2 = '../public/assets/content/articles/'
path = '../public/assets/content/articles'
tempListTag = []
collectionOfList = []
text = "News,coba"

if not os.path.exists(path):
  os.mkdir(path)
else:
  print("udah ada")

# def Diff(li1, li2):
#   return(list(set(li1) - set(li2)))
#
# def Same(li1, li2):
#   return (list(set(li1) & set(li2)))
#
# id = 1
#
# with open(path, 'r+') as read_file:
#   data = json.load(read_file)
#   unpackTags = data['tags']
#   splitText = text.split(',')
#   print(unpackTags)
#   # unpackLoadData = [value['name'] for value in unpackTags if value['id'] == id]
#   compareDataValue = Diff(unpackLoadData, splitText)
#   compareValueData = Diff(splitText, unpackLoadData)
#
#   print(compareDataValue)
#   print(compareValueData)
#
#   # copiedData = unpackTags.copy()
#
#   for dataDat in unpackTags[:]:
#     if dataDat['id'] == id:
#       if dataDat['name'] in compareDataValue:
#         unpackTags.remove(dataDat)
#
#   for dataVal in compareValueData:
#     tempDict = {}
#     tempDict['name'] = dataVal
#     tempDict['id'] = id
#     unpackTags.append(tempDict)
#
#   print(unpackTags)
  # combine = unpackLoadData + compareList
  # print(unpackLoadData)
  # print(compareList)
  # print(combine)
  # print(unpackLoadData)
  # print(unpackTags)
  # print(splitText)
  # print(compareDataValue)

  # for value in splitText:
  #   tempTag = {}
  #   tempTag['name'] = value
  #   tempTag['id'] =
  # for value in combine:
  #   tempTag = {}
  #   tempTag['name'] = value
  #   tempTag['id'] = content['article']['id']
  #   tempListTag.append(tempTag)
  # data = json.load(read_file)
  # for value in data['articles']:
  #   getTag = value.get('tag')
  #   # getTag.split(',')
  #   if getTag not :
  #     print(getTag)
  #   # for key,value2 in value.items():
  #   #   print(value2.get)
  # try:
  #   openTag = open(path, 'r+')
  #   data = json.load(openTag)
  #   unpackTags = data['tags']
  #   splitText = text.split(',')
  #   unpackLoadData = [value['name'] for value in unpackTags]
  #   compareListDiff = Diff(splitText, unpackLoadData)
  #   compareListSame = Same(splitText, unpackLoadData)
  #   combine = compareListSame + compareListDiff
  #
  #   print(splitText)
  #   print(unpackLoadData)
  #   print(compareListDiff)
  #   print(compareListSame)
  #   print(combine)
  # except:
  #   print("test")
