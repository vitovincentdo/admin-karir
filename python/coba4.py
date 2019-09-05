from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import os, shutil
import base64
import re
from bs4 import BeautifulSoup
import functionToCall

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins":"*"}})

# POST article Data
@app.route('/api/article/post', methods=['POST'])
def postJsonArticleHandler():
    content = request.get_json()
    if os.path.exists('../public/assets/content/articles/data.json'):
      argument = 'articleExist'
      functionToCall.forArticle(content,argument)
    else:
      argument = 'articleNotExist'
      functionToCall.forArticle(content, argument)

    tempID = dict(id=1)
    tempResponse = dict(articles=tempID)
    js = json.dumps(tempResponse)
    resp = Response(js, status=201, mimetype='application/json')
    # resp.headers['Link'] = 'http://localhost:81'
    return resp

# GET Article By ID
@app.route('/api/article/get/<int:article_id>', methods=['GET'])
def articleByID(article_id):
  with open('../public/assets/content/articles/data.json', 'r') as read_file:
    data = json.load(read_file)
    dictData = data['articles']
    try:
      for loop in dictData:
        if article_id == loop['id']:
          selectedUser = loop
      count = selectedUser['id']
      f = open('../public/assets/content/articles/article/'+str(count)+'.json', 'r')
      data2 = json.load(f)
      outDict = data2['article']
      for secondLoop, value in outDict.items():
        if secondLoop == 'thumbImage':
          outDict[secondLoop] = '<p><img src="'+value+'"/></p>'
        elif secondLoop == 'article':
          soup = BeautifulSoup(value, "html.parser")
          for img in soup.findAll('img'):
            img['src'] = '/'+img['src']
          outDict[secondLoop] = str(soup)
      selectedUser.update(outDict)
      f.close()
      forResp = dict(articles=selectedUser)
      resp = jsonify(forResp)
    except:
      resp = jsonify("ID Not Found")
  return resp

#GET All article Data
@app.route('/api/article/list', methods=['GET'])
def allArticleList():
  with open('../public/assets/content/articles/data.json', 'r') as read_file:
    data = json.load(read_file)
    return jsonify(data)

# PUT Article Data
@app.route('/api/article/update/<int:article_id>', methods=['PUT'])
def updateArticle(article_id):
  updateContent = request.get_json()
  unloadUpdate = updateContent['article']
  path = '../public/assets/content/articles/'
  pathIMG = '../public/assets/content/articles/article-image/' + str(article_id) + '/'
  temp = {}
  tempResponse = {}
  id = article_id
  with open(path+'data.json', 'r+') as read_file:
    with open(path+'article/'+str(article_id)+'.json', 'r+') as read_inner_file:
      data = json.load(read_file)
      dataPerId = json.load(read_inner_file)
      temp2 = data.copy()
      loadDict = temp2['articles']
      loadInner = dataPerId['article']
      try:
        for loop in loadDict:
            if article_id == loop['id']:
              selectedArticle = loop
        for loopNewData, value in unloadUpdate.items():
          if loopNewData == 'article':
            soup = BeautifulSoup(value, "html.parser")
            html_img_tags = soup.findAll("img")
            if not html_img_tags:
              listExcThumb = [x for x in os.listdir(pathIMG) if x != 'thumbnail-image.jpg']
              for item in listExcThumb:
                os.remove(os.path.join(pathIMG, item))
              temp[loopNewData] = str(soup)

            else:
              listExcThumb = [x for x in os.listdir(pathIMG) if x != 'thumbnail-image.jpg']
              tempIMG = []
              tempSRC = []
              for tag in html_img_tags:
                tempIMG.append(tag['src'])

              tempExcNew = [x for x in tempIMG if not x.startswith('data:image')]
              tempIMGLast = [x[-1:-11:-1] for x in tempExcNew]
              reverseTempIMGLast = [x[::-1] for x in tempIMGLast]
              diffImage = Diff(listExcThumb, reverseTempIMGLast)

              for item in diffImage:
                os.remove(os.path.join(pathIMG,item))

              countCurrent = 0
              for item in reverseTempIMGLast:
                if int(item[-5]) > countCurrent:
                  countCurrent = int(item[-5])

              for toLocal in tempIMG:
                if not toLocal.startswith('data:image'):
                  toLocal = re.search(r'../(\w+.*)',toLocal)
                  toLocal = toLocal.group(1)
                  toLocal = 'assets/'+toLocal
                  tempSRC.append(toLocal)

                img = re.findall(r'base64,(.*)', toLocal, re.I | re.M)
                if img:
                  countCurrent += 1
                  decodeData = base64.b64decode(img[0])
                  source = pathIMG + "image" + str(countCurrent) + ".jpg"
                  splitSource = re.findall(r'public/(.*)', source, re.I | re.M)
                  tempSRC.append(splitSource)
                  image_result = open(source, 'wb')
                  image_result.write(decodeData)
                  image_result.close()

              for iterHTML, iterSRC in zip(html_img_tags, tempSRC):
                iterHTML['src'] = iterSRC
              temp[loopNewData] = str(soup)
          elif loopNewData == 'thumbImage':
            soup = BeautifulSoup(value, "html.parser")
            html_img_tags = soup.findAll("img")
            if not html_img_tags:
              listFile = os.listdir(pathIMG)
              for i in listFile:
                if "thumbnail-image" in i:
                  os.remove(pathIMG + "thumbnail-image.jpg")
            else:
              tempIMG = []
              for tag in html_img_tags:
                tempIMG.append(tag['src'])
              img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
              if img:
                listFile = os.listdir(pathIMG)
                for i in listFile:
                  if "thumbnail-image" in i:
                    os.remove(pathIMG + "thumbnail-image.jpg")
                decodeData = base64.b64decode(img[0])
                source = pathIMG + 'thumbnail-image.jpg'
                splitSource = re.findall(r'public(.*)', source, re.I | re.M)
                image_result = open(source, 'wb')
                image_result.write(decodeData)
                image_result.close()
                temp[loopNewData] = splitSource[0]
                selectedArticle[loopNewData] = splitSource[0]
              else:
                temp[loopNewData] = loadInner[loopNewData]
                # soup2 = BeautifulSoup(str(value), 'html.parser')
                # image = soup2.find('img')
                # print(image['src'])
                # reformat = '/'+image['src']
                # temp[loopNewData] = reformat
          elif loopNewData == 'tag':
            path = '../public/assets/content/articles/tag.json'
            tempListTag = []
            try:
              openTag = open(path, 'r+')
              data = json.load(openTag)
              unpackTags = data['tags']
              splitText = value.split(',')
              unpackLoadData = [value['name'] for value in unpackTags if value['id'] == article_id]
              compareDataValue = Diff(unpackLoadData, splitText)
              compareValueData = Diff(splitText, unpackLoadData)

              for dataDat in unpackTags[:]:
                if dataDat['id'] == article_id:
                  if dataDat['name'] in compareDataValue:
                    unpackTags.remove(dataDat)

              for dataVal in compareValueData:
                tempDict = {}
                tempDict['name'] = dataVal
                tempDict['id'] = article_id
                unpackTags.append(tempDict)

              tempDictTag = dict(tags=unpackTags)
              openTag.seek(0)
              openTag.truncate()
              openTag.write(json.dumps(tempDictTag))
              openTag.close()
            except IOError:
              openTag = open(path, 'w')
              splitText = value.split(',')
              for x in splitText:
                tempTag = {}
                tempTag['name'] = x
                tempTag['id'] = article_id
                tempListTag.append(tempTag)
              tempDictTag = dict(tags=tempListTag)
              openTag.write(json.dumps(tempDictTag))
              openTag.close()
            temp[loopNewData] = value
            selectedArticle[loopNewData] = value
          # elif loopNewData == 'date':
          #   path = '../public/assets/content/articles/date.json'
          #   try:
          #     openDate = open(path, 'r+')
          #     dateContentToDict = {}
          #     dataDate = json.load(openDate)
          #     unpackDate = dataDate['dates']
          #
          #     contentFormatted = datetime.strptime(value, '%Y-%m-%d').date()
          #     date = contentFormatted.replace(day=1)
          #     dateToString = date.strftime('%Y-%m-%d')
          #
          #     if not any(d['name'] == dateToString for d in unpackDate):
          #       dateContentToDict['name'] = dateToString
          #
          #     if (dateContentToDict):
          #       unpackDate.append(dateContentToDict)
          #
          #     tempDict = dict(dates=unpackDate)
          #     openDate.seek(0)
          #     openDate.truncate()
          #     openDate.write(json.dumps(tempDict))
          #     openDate.close()
          #   except IOError:
          #     openDate = open(path, 'w')
          #     contentFormatted = datetime.strptime(value, '%Y-%m-%d').date()
          #     date = contentFormatted.replace(day=1)
          #     dateToString = date.strftime('%Y-%m-%d')
          #     toDict = dict(name=dateToString)
          #     toList = [toDict]
          #     tempDict = dict(dates=toList)
          #     openDate.write(json.dumps(tempDict))
          #     openDate.close()
          #   temp[loopNewData] = value
          #   selectedArticle[loopNewData] = value
          elif loopNewData == 'title':
            temp[loopNewData] = value
            selectedArticle[loopNewData] = value
          elif loopNewData == 'date':
            temp[loopNewData] = value
            selectedArticle[loopNewData] = value
        tempResponse['articles']['id'] = article_id
        resp = Response(json.dumps(tempResponse), status=201, mimetype='application/json')
      except:
        resp = jsonify("ID Not Found")
      temp = dict(article=temp)
      # print(temp)
      temp['article']['id'] = article_id
      read_inner_file.seek(0)
      read_inner_file.truncate()
      read_inner_file.write(json.dumps(temp))
    read_file.seek(0)
    read_file.truncate()
    # print(temp2)
    read_file.write(json.dumps(temp2))
  return resp

# DELETE Article Data
@app.route('/api/article/delete/<int:article_id>', methods=['DELETE'])
def deleteArticle(article_id):
  path = '../public/assets/content/articles/'
  with open(path+'data.json', 'r+') as read_file:
    data = json.load(read_file)
    loadDict = data['articles']

    filterData = [item for item in loadDict if item['id'] != article_id]
    existsInnerData = os.path.isfile(path+'article/'+str(article_id)+'.json')
    existImageDir = os.path.isdir(path+'article-image/'+str(article_id))
    if existsInnerData:
      os.remove(path + 'article/' + str(article_id) + '.json')
    if existImageDir:
      shutil.rmtree(path+'article-image/'+str(article_id))

    openTag = open(path+'tag.json', 'r+')
    data = json.load(openTag)
    unpackTags = data['tags']
    filterTag = [item for item in unpackTags if item['id'] != article_id]
    filteredTag = dict(tags=filterTag)
    filteredData = dict(articles=filterData)
    openTag.seek(0)
    openTag.truncate()
    openTag.write(json.dumps(filteredTag))
    openTag.close()
    read_file.seek(0)
    read_file.truncate()
    read_file.write(json.dumps(filteredData))
    resp = Response(status=200)
  return resp

# POST Thought Data
@app.route('/api/thought/post', methods=['POST'])
def postJsonThoughtHandler():
    content = request.get_json()
    if os.path.exists('../public/assets/content/thoughts/data.json'):
      with open('../public/assets/content/thoughts/data.json', 'r+') as file:
        temp = {}
        # temp2 = {}
        data = json.load(file)
        loadData = data['thoughts']
        try:
          for loop in loadData:
            count = loop['id']
          content['thought']['id'] = count+1
        except:
          content['thought']['id'] = 1
        for key, value in content.items():
          for key2, value2 in value.items():
            # if key2 == 'name':
            #   temp[key2] = value2
            #   # temp2[key2] = value2
            if key2 == 'thought':
              soup = BeautifulSoup(value2, "html.parser")
              onlyText = soup.get_text()
              onlyText = onlyText.replace('\n',' ')
              temp[key2] = onlyText
              # temp2[key2] = onlyText
            elif key2 == 'thumbThought':
              soup = BeautifulSoup(value2, "html.parser")
              html_img_tags = soup.findAll("img")
              if not html_img_tags:
                pass
              else:
                if not os.path.isdir("../public/assets/content/thoughts/thoughts-image/" + str(content['thought']['id'])):
                  os.mkdir("../public/assets/content/thoughts/thoughts-image/" + str(content['thought']['id']))
                else:
                  pass
                tempIMG = []
                for tag in html_img_tags:
                  tempIMG.append(tag['src'])
                img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
                decodeData = base64.b64decode(img[0])
                source = "../public/assets/content/thoughts/thoughts-image/" + str(
                  content['thought']['id']) + '/thumbnail-image.jpg'
                splitSource = re.findall(r'public(.*)', source, re.I | re.M)
                image_result = open(source, 'wb')
                image_result.write(decodeData)
                image_result.close()
                temp[key2] = splitSource[0]
                # temp2[key2] = splitSource[0]
            else:
              temp[key2] = value2
              # temp2[key2] = value2

        loadData.append(temp)
        tempDict = dict(thoughts=loadData)
        # tempDict2 = dict(thought=temp2)
        file.seek(0)
        file.truncate()
        file.write(json.dumps(tempDict))
        # f = open('../public/assets/content/thoughts/thought/' + str(content['thought']['id']) + '.json', 'w')
        # f.write(json.dumps(tempDict2))
        # f.close()
    else:
      if not os.path.exists('../public/assets/content/thoughts'):
        os.mkdir('../public/assets/content/thoughts')
      with open('../public/assets/content/thoughts/data.json', 'w') as createThoughts:
        temp = {}
        # temp2 = {}
        content['thought']['id'] = 1
        for key, value in content.items():
          for key2, value2 in value.items():
            # if key2 == 'name':
            #   temp[key2] = value2
              # temp2[key2] = value2
            if key2 == 'thought':
              soup = BeautifulSoup(value2, "html.parser")
              onlyText = soup.get_text()
              onlyText = onlyText.replace('\n', ' ')
              temp[key2] = onlyText
              # temp2[key2] = onlyText
            elif key2 == 'thumbThought':
              soup = BeautifulSoup(value2, "html.parser")
              html_img_tags = soup.findAll("img")
              if not html_img_tags:
                pass
              else:
                if not os.path.isdir("../public/assets/content/thoughts/thoughts-image"):
                  os.mkdir("../public/assets/content/thoughts/thoughts-image")
                if not os.path.isdir("../public/assets/content/thoughts/thoughts-image/" + str(content['thought']['id'])):
                  os.mkdir("../public/assets/content/thoughts/thoughts-image/" + str(content['thought']['id']))
                else:
                  pass
                tempIMG = []
                for tag in html_img_tags:
                  tempIMG.append(tag['src'])
                img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
                decodeData = base64.b64decode(img[0])
                source = "../public/assets/content/thoughts/thoughts-image/" + str(
                  content['thought']['id']) + '/thumbnail-image.jpg'
                splitSource = re.findall(r'public(.*)', source, re.I | re.M)
                image_result = open(source, 'wb')
                image_result.write(decodeData)
                image_result.close()
                temp[key2] = splitSource[0]
                # temp2[key2] = splitSource[0]
            else:
              temp[key2] = value2
              # temp2[key2] = value2

        temp = [temp]
        tempDict = dict(thoughts=temp)
        # tempDict2 = dict(thought=temp2)

        createThoughts.write(json.dumps(tempDict))
        # f = open('../public/assets/content/thoughts/thought/'+str(content['thought']['id'])+'.json', 'w')
        # f.write(json.dumps(tempDict2))
        # f.close()

    tempID = {}
    tempResponse = {}
    for key, value in content.items():
      for key2, value2 in value.items():
        if key2 == 'id':
          tempID[key2] = value2

    tempResponse['thoughts'] = tempID
    js = json.dumps(tempResponse)
    resp = Response(js, status=201, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:81'
    return resp

# GET Thought By ID
@app.route('/api/thought/get/<int:thought_id>', methods=['GET'])
def thoughtByID(thought_id):
  with open('../public/assets/content/thoughts/data.json', 'r') as read_file:
    data = json.load(read_file)
    dictData = data['thoughts']
    filterData = [item for item in dictData if item['id'] == thought_id]
    for item in filterData:
      for key, value in item.items():
        if key == 'thumbThought':
          item[key] = '<p><img src="'+value+'"/></p>'
    forResp = dict(thoughts=filterData)
    resp = jsonify(forResp)
    # try:
    #   for loop in dictData:
    #     if thought_id == loop['id']:
    #       selectedUser = loop
    #   count = selectedUser['id']
    #   f = open('../public/assets/content/thoughts/thought/'+str(count)+'.json', 'r')
    #   data2 = json.load(f)
    #   outDict = data2['thought']
    #   for secondLoop, value in outDict.items():
    #     if secondLoop == 'thumbThought':
    #       outDict[secondLoop] = '<p><img src="'+value+'"/></p>'
    #   selectedUser.update(outDict)
    #   f.close()
    #   forResp = dict(thoughts=selectedUser)
    #   resp = jsonify(forResp)
    # except:
    #   resp = jsonify("ID Not Found")
  return resp

#GET All Thought Data
@app.route('/api/thought/list', methods=['GET'])
def allThoughtList():
  with open('../public/assets/content/thoughts/data.json', 'r') as read_file:
    data = json.load(read_file)
    return jsonify(data)

# PUT Thought Data
@app.route('/api/thought/update/<int:thought_id>', methods=['PUT'])
def updateThought(thought_id):
  updateContent = request.get_json()
  unloadUpdate = updateContent['thought']
  path = '../public/assets/content/thoughts/'
  pathIMG = '../public/assets/content/thoughts/thoughts-image/' + str(thought_id) + '/'
  temp = {}
  tempResponse = {}
  with open(path+'data.json', 'r+') as read_file:
    # with open(path+'thought/'+str(thought_id)+'.json', 'r+') as read_inner_file:
    data = json.load(read_file)
    # dataPerId = json.load(read_inner_file)
    temp2 = data.copy()
    loadDict = temp2['thoughts']
    # loadInner = dataPerId['thought']
    try:
      for loop in loadDict:
          if thought_id == loop['id']:
            selectedThought = loop
      for loopNewData, value in unloadUpdate.items():
        if loopNewData == 'thumbThought':
          if not os.path.isdir('../public/assets/content/thoughts/thoughts-image'):
            os.mkdir('../public/assets/content//thoughts/thoughts-image')
          soup = BeautifulSoup(value, "html.parser")
          html_img_tags = soup.findAll("img")
          if not html_img_tags:
            listFile = os.listdir(pathIMG)
            for i in listFile:
              if "thumbnail-image" in i:
                os.remove(pathIMG + "thumbnail-image.jpg")
            for item in loadDict:
              item.pop("thumbThought")
          else:
            if not os.path.isdir('../public/assets/content/thoughts/thoughts-image/' + str(thought_id)):
              os.mkdir('../public/assets/content/thoughts/thoughts-image/' + str(thought_id))
            tempIMG = []
            for tag in html_img_tags:
              tempIMG.append(tag['src'])
            img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
            if img:
              listFile = os.listdir(pathIMG)
              for i in listFile:
                if "thumbnail-image" in i:
                  os.remove(pathIMG + "thumbnail-image.jpg")
              decodeData = base64.b64decode(img[0])
              source = pathIMG + 'thumbnail-image.jpg'
              splitSource = re.findall(r'public(.*)', source, re.I | re.M)
              image_result = open(source, 'wb')
              image_result.write(decodeData)
              image_result.close()
              # temp[loopNewData] = splitSource[0]
              selectedThought[loopNewData] = splitSource[0]
            # else:
              # temp[loopNewData] = loadInner[loopNewData]
              # soup2 = BeautifulSoup(str(value), 'html.parser')
              # image = soup2.find('img')
              # print(image['src'])
              # reformat = '/'+image['src']
              # temp[loopNewData] = reformat
        elif loopNewData == 'thought':
          soup = BeautifulSoup(value, "html.parser")
          onlyText = soup.get_text()
          onlyText = onlyText.replace('\n', ' ')
          selectedThought[loopNewData] = onlyText
        else:
          # temp[loopNewData] = value
          selectedThought[loopNewData] = value
        # elif loopNewData == 'name':
        #   # temp[loopNewData] = value
        #   selectedThought[loopNewData] = value
        # elif loopNewData == 'thought':
        #   # temp[loopNewData] = value
        #   selectedThought[loopNewData] = value
        # elif loopNewData == 'date':
        #   # temp[loopNewData] = value
        #   selectedThought[loopNewData] = value
      tempResponse['thoughts']['id'] = thought_id
      resp = Response(json.dumps(tempResponse), status=201, mimetype='application/json')
    except:
      resp = jsonify("ID Not Found")
    # temp = dict(thought=temp)
    # temp['thought']['id'] = thought_id
    # read_inner_file.seek(0)
    # read_inner_file.truncate()
    # read_inner_file.write(json.dumps(temp))
    # read_inner_file.close()
    read_file.seek(0)
    read_file.truncate()
    read_file.write(json.dumps(temp2))
    read_file.close()
  return resp

# DELETE Thought Data
@app.route('/api/thought/delete/<int:thought_id>', methods=['DELETE'])
def deleteThought(thought_id):
  path = '../public/assets/content/thoughts/'
  with open(path+'data.json', 'r+') as read_file:
    data = json.load(read_file)
    loadDict = data['thoughts']

    filterData = [item for item in loadDict if item['id'] != thought_id]
    existsInnerData = os.path.isfile(path+'thought/'+str(thought_id)+'.json')
    existImageDir = os.path.isdir(path+'thoughts-image/'+str(thought_id))
    if existsInnerData:
      os.remove(path + 'thought/' + str(thought_id) + '.json')
    if existImageDir:
      shutil.rmtree(path+'thoughts-image/'+str(thought_id))

    filteredData = dict(thoughts=filterData)
    read_file.seek(0)
    read_file.truncate()
    read_file.write(json.dumps(filteredData))
    read_file.close()
    resp = Response(status=200)
  return resp

# POST Jobs Data
@app.route('/api/job/post', methods=['POST'])
def postJsonJobHandler():
    content = request.get_json()
    if os.path.exists('../public/assets/content/jobs/data.json'):
      with open('../public/assets/content/jobs/data.json', 'r+') as file:
        temp = {}
        temp2 = {}
        data = json.load(file)
        loadData = data['jobs']
        try:
          for loop in loadData:
            count = loop['id']
          content['job']['id'] = count+1
        except:
          content['job']['id'] = 1
        for key, value in content.items():
          for key2, value2 in value.items():
            if key2 == 'name':
              temp[key2] = value2
              temp2[key2] = value2
            elif key2 == 'description':
              temp2[key2] = value2
            elif key2 == 'qualification':
              temp2[key2] = value2
            elif key2 == 'thumbJob':
              soup = BeautifulSoup(value2, "html.parser")
              html_img_tags = soup.findAll("img")
              if not html_img_tags:
                pass
              else:
                if not os.path.isdir("../public/assets/content/jobs/jobs-image/" + str(content['job']['id'])):
                  os.mkdir("../public/assets/content/jobs/jobs-image/" + str(content['job']['id']))
                else:
                  pass
                tempIMG = []
                for tag in html_img_tags:
                  tempIMG.append(tag['src'])
                img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
                decodeData = base64.b64decode(img[0])
                source = "../public/assets/content/jobs/jobs-image/" + str(
                  content['job']['id']) + '/thumbnail-image.png'
                splitSource = re.findall(r'public(.*)', source, re.I | re.M)
                image_result = open(source, 'wb')
                image_result.write(decodeData)
                image_result.close()
                temp[key2] = splitSource[0]
                temp2[key2] = splitSource[0]
            # elif key2 == 'location':
            #   splitLocation = value2.split(", ")
            #   temp[key2] = splitLocation
            elif key2 == 'specialization':
              value2 = value.lower()
              temp[key2] = value2
            else:
              temp[key2] = value2
              temp2[key2] = value2

        loadData.append(temp)
        tempDict = dict(jobs=loadData)
        tempDict2 = dict(job=temp2)
        file.seek(0)
        file.truncate()
        file.write(json.dumps(tempDict))
        # f = open('../public/assets/content/jobs/job/' + str(content['job']['id']) + '.json', 'w')
        # f.write(json.dumps(tempDict2))
        # f.close()
    else:
      if not os.path.exists('../public/assets/content/jobs'):
        os.mkdir('../public/assets/content/jobs')
      with open('../public/assets/content/jobs/data.json', 'w') as createJob:
        temp = {}
        temp2 = {}
        content['job']['id'] = 1
        for key, value in content.items():
          for key2, value2 in value.items():
            if key2 == 'name':
              temp[key2] = value2
              temp2[key2] = value2
            elif key2 == 'description':
              temp2[key2] = value2
            elif key2 == 'qualification':
              temp2[key2] = value2
            elif key2 == 'thumbJob':
              soup = BeautifulSoup(value2, "html.parser")
              html_img_tags = soup.findAll("img")
              if not html_img_tags:
                pass
              else:
                if not os.path.isdir("../public/assets/content/jobs/jobs-image"):
                  os.mkdir("../public/assets/content/jobs/jobs-image")
                if not os.path.isdir("../public/assets/content/jobs/jobs-image/" + str(content['job']['id'])):
                  os.mkdir("../public/assets/content/jobs/jobs-image/" + str(content['job']['id']))
                else:
                  pass
                tempIMG = []
                for tag in html_img_tags:
                  tempIMG.append(tag['src'])
                img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
                decodeData = base64.b64decode(img[0])
                source = "../public/assets/content/jobs/jobs-image/" + str(
                  content['job']['id']) + '/thumbnail-image.png'
                splitSource = re.findall(r'public(.*)', source, re.I | re.M)
                image_result = open(source, 'wb')
                image_result.write(decodeData)
                image_result.close()
                temp[key2] = splitSource[0]
                temp2[key2] = splitSource[0]
            # elif key2 == 'location':
            #   splitLocation = value2.split(", ")
            #   temp[key2] = splitLocation
            elif key2 == 'specialization':
              value2 = value.lower()
              temp[key2] = value2
            else:
              temp[key2] = value2
              temp2[key2] = value2

        temp = [temp]
        tempDict = dict(jobs=temp)
        tempDict2 = dict(job=temp2)

        createJob.write(json.dumps(tempDict))

        # if not os.path.isdir('../public/assets/content/jobs/job'):
        #   os.mkdir('../public/assets/content/jobs/job')
        # f = open('../public/assets/content/jobs/job/'+str(content['job']['id'])+'.json', 'w')
        # f.write(json.dumps(tempDict2))
        # f.close()

    tempID = {}
    tempResponse = {}
    for key, value in content.items():
      for key2, value2 in value.items():
        if key2 == 'id':
          tempID[key2] = value2

    tempResponse['jobs'] = tempID
    js = json.dumps(tempResponse)
    resp = Response(js, status=201, mimetype='application/json')
    resp.headers['Link'] = 'http://localhost:81'
    return resp

# GET Job By ID
@app.route('/api/job/get/<int:job_id>', methods=['GET'])
def jobByID(job_id):
  with open('../public/assets/content/jobs/data.json', 'r') as read_file:
    data = json.load(read_file)
    dictData = data['jobs']
    filterData = [item for item in dictData if item['id'] == job_id]
    # print(filterData)
    for item in filterData:
      for key, value in item.items():
        if key == 'thumbJob':
          if value != None:
            item[key] = '<p><img src="'+value+'"/></p>'
    forResp = dict(jobs=filterData)
    resp = jsonify(forResp)
    # try:
    #   for loop in dictData:
    #     if job_id == loop['id']:
    #       selectedUser = loop
    #   count = selectedUser['id']
    #   f = open('../public/assets/content/jobs/job/'+str(count)+'.json', 'r')
    #   data2 = json.load(f)
    #   outDict = data2['job']
    #   for secondLoop, value in outDict.items():
    #     if secondLoop == 'thumbJob':
    #       outDict[secondLoop] = '<p><img src="'+value+'"/></p>'
    #   selectedUser.update(outDict)
    #   f.close()
    #   forResp = dict(jobs=selectedUser)
    #   resp = jsonify(forResp)
    # except:
    #   resp = jsonify("ID Not Found")
  return resp

#GET All Job Data
@app.route('/api/job/list', methods=['GET'])
def allJobList():
  with open('../public/assets/content/jobs/data.json', 'r') as read_file:
    data = json.load(read_file)
    return jsonify(data)

# PUT Job Data
@app.route('/api/job/update/<int:job_id>', methods=['PUT'])
def updateJob(job_id):
  updateContent = request.get_json()
  unloadUpdate = updateContent['job']
  path = '../public/assets/content/jobs/'
  pathIMG = '../public/assets/content/jobs/jobs-image/' + str(job_id) + '/'
  temp = {}
  tempResponse = {}
  with open(path+'data.json', 'r+') as read_file:
    # with open(path+'job/'+str(job_id)+'.json', 'r+') as read_inner_file:
    data = json.load(read_file)
    # dataPerId = json.load(read_inner_file)
    temp2 = data.copy()
    loadDict = temp2['jobs']
    # loadInner = dataPerId['job']
    try:
      for loop in loadDict:
          if job_id == loop['id']:
            selectedJob = loop
      for loopNewData, value in unloadUpdate.items():
        # if loopNewData == 'article':
        #   soup = BeautifulSoup(value, "html.parser")
        #   html_img_tags = soup.findAll("img")
        #   countExist = 1
        #   if not html_img_tags:
        #     listFile = os.listdir(pathIMG)
        #     for i in listFile:
        #       if "image"+str(countExist) in i:
        #         os.remove(pathIMG + "image" + str(countExist) + ".jpg")
        #         countExist += 1
        #     temp[loopNewData] = value
        #
        #   else:
        #     tempIMG = []
        #     tempSRC = []
        #     for tag in html_img_tags:
        #       tempIMG.append(tag['src'])
        #
        #     count = 1
        #     for toLocal in tempIMG:
        #       img = re.findall(r'base64,(.*)', toLocal, re.I | re.M)
        #       if img:
        #         listFile = os.listdir(pathIMG)
        #         for i in listFile:
        #           if "image" + str(countExist) in i:
        #             os.remove(pathIMG + "image" + str(countExist) + ".jpg")
        #             # print(countDelFile)
        #             # countDelFile += 1
        #         decodeData = base64.b64decode(img[0])
        #         source = pathIMG + "image" + str(count) + ".jpg"
        #         splitSource = re.findall(r'public/(.*)', source, re.I | re.M)
        #         tempSRC.append(splitSource)
        #         image_result = open(source, 'wb')
        #         image_result.write(decodeData)
        #         image_result.close()
        #         count += 1
        #         countExist += 1
        #       else:
        #         reformat = toLocal[1:]
        #         tempSRC.append(reformat)
        #     for iterHTML, iterSRC in zip(html_img_tags, tempSRC):
        #       iterHTML['src'] = iterSRC
        #     temp[loopNewData] = str(soup)
        if loopNewData == 'thumbJob':
          if not os.path.isdir('../public/assets/content/jobs/jobs-image'):
            os.mkdir('../public/assets/content/jobs/jobs-image')
          soup = BeautifulSoup(value, "html.parser")
          html_img_tags = soup.findAll("img")
          if not html_img_tags:
            listFile = os.listdir(pathIMG)
            for i in listFile:
              if "thumbnail-image" in i:
                os.remove(pathIMG + "thumbnail-image.png")
            selectedJob[loopNewData] = None
          else:
            if not os.path.isdir('../public/assets/content/jobs/jobs-image/' + str(job_id)):
              os.mkdir('../public/assets/content/jobs/jobs-image/' + str(job_id))
            tempIMG = []
            for tag in html_img_tags:
              tempIMG.append(tag['src'])
            img = re.findall(r'base64,(.*)', tempIMG[0], re.I | re.M)
            if img:
              listFile = os.listdir(pathIMG)
              for i in listFile:
                if "thumbnail-image" in i:
                  os.remove(pathIMG + "thumbnail-image.png")
              decodeData = base64.b64decode(img[0])
              source = pathIMG + 'thumbnail-image.png'
              splitSource = re.findall(r'public(.*)', source, re.I | re.M)
              image_result = open(source, 'wb')
              image_result.write(decodeData)
              image_result.close()
              # temp[loopNewData] = splitSource[0]
              selectedJob[loopNewData] = splitSource[0]
            # else:
            #   temp[loopNewData] = loadInner[loopNewData]
              # soup2 = BeautifulSoup(str(value), 'html.parser')
              # image = soup2.find('img')
              # print(image['src'])
              # reformat = '/'+image['src']
              # temp[loopNewData] = reformat
        # elif loopNewData == 'name':
        #   temp[loopNewData] = value
        #   selectedJob[loopNewData] = value
        # elif loopNewData == 'specialization':
        #   temp[loopNewData] = value
        #   selectedJob[loopNewData] = value
        # elif loopNewData == 'featured':
        #   temp[loopNewData] = value
        #   selectedJob[loopNewData] = value
        # elif loopNewData == 'description':
        #   temp[loopNewData] = value
        # elif loopNewData == 'qualification':
        #   temp[loopNewData] = value
        # elif loopNewData == 'url':
        #   temp[loopNewData] = value
        # elif loopNewData == 'location':
        #   splitLocation = value.split(", ")
        #   # temp[loopNewData] = splitLocation
        #   selectedJob[loopNewData] = splitLocation
        elif loopNewData == 'description' or loopNewData == 'qualification':
          pass
        elif loopNewData == 'specialization':
          value = value.lower()
          selectedJob[loopNewData] = value
        elif loopNewData == 'name':
          selectedJob[loopNewData] = value
        else:
          # temp[loopNewData] = value
          selectedJob[loopNewData] = value
      tempResponse['jobs']['id'] = job_id
      resp = Response(json.dumps(tempResponse), status=201, mimetype='application/json')
    except:
      resp = jsonify("ID Not Found")

    # print(temp2)
    # temp = dict(job=temp)
    # temp['job']['id'] = job_id
    # read_inner_file.seek(0)
    # read_inner_file.truncate()
    # read_inner_file.write(json.dumps(temp))
    # read_inner_file.close()
    read_file.seek(0)
    read_file.truncate()
    read_file.write(json.dumps(temp2))
    read_file.close()
  return resp

# DELETE Job Data
@app.route('/api/job/delete/<int:job_id>', methods=['DELETE'])
def deleteJob(job_id):
  path = '../public/assets/content/jobs/'
  with open(path+'data.json', 'r+') as read_file:
    data = json.load(read_file)
    loadDict = data['jobs']

    filterData = [item for item in loadDict if item['id'] != job_id]
    existsInnerData = os.path.isfile(path+'job/'+str(job_id)+'.json')
    existImageDir = os.path.isdir(path+'jobs-image/'+str(job_id))
    if existsInnerData:
      os.remove(path + 'job/' + str(job_id) + '.json')
    if existImageDir:
      shutil.rmtree(path+'jobs-image/'+str(job_id))

    filteredData = dict(jobs=filterData)
    read_file.seek(0)
    read_file.truncate()
    read_file.write(json.dumps(filteredData))
    read_file.close()
    resp = Response(status=200)
  return resp


# POST counter Data
@app.route('/api/counter/post', methods=['POST'])
def postJsonCounterHandler():
    content = request.get_json()
    if not os.path.isdir('../public/assets/content/counter'):
      os.mkdir('../public/assets/content/counter')
    with open('../public/assets/content/counter/data.json', 'w') as createCounter:
      temp = {}
      content['counter']['id'] = 1
      for key, value in content.items():
        for key2, value2 in value.items():
          temp[key2] = value2

      temp = [temp]
      tempDict = dict(counters=temp)

      createCounter.write(json.dumps(tempDict))

      tempResponse = {}
      tempResponse['counters'] = content['counter']['id']
      js = json.dumps(tempResponse)
      resp = Response(js, status=201, mimetype='application/json')
      resp.headers['Link'] = 'http://localhost:81'
    return resp

# # DELETE Data
# @app.route('/api/data/delete/<int:user_id>', methods=['DELETE'])
# def deleteUser(user_id):
#   with open('../public/assets/content/articles/data.json', 'r+') as read_file:
#     newDict = {}
#     data = json.load(read_file)
#     loadDict = data['datas']
#     try:
#       for loop in loadDict:
#         if user_id == loop['id']:
#           selectedUser = loop
#
#       count = selectedUser['id']
#       os.remove('../public/assets/content/articles/article/' + str(count) + '.json')
#
#       loadDict.remove(selectedUser)
#       read_file.seek(0)
#       read_file.truncate()
#       newDict['datas'] = loadDict
#       read_file.write(json.dumps(newDict))
#       resp = jsonify(selectedUser)
#     except:
#       resp = jsonify("ID Not Found")
#   return resp

# # PUT Data
# @app.route('/api/job/update/<int:job_id>', methods=['PUT'])
# def updateJob(job_id):
#   updateContent = request.get_json()
#   unloadUpdate = updateContent['job']
#   with open('../public/assets/content/jobs/data.json', 'r+') as read_file:
#     data = json.load(read_file)
#     loadDict = data['jobs']
#     try:
#       for loop in loadDict:
#         if job_id == loop['id']:
#           selectedJob = loop
#
#       count = selectedJob['id']
#       f = open('../public/assets/content/jobs/job/' + str(count) + '.json', 'r+')
#       data2 = json.load(f)
#       loadDict2 = data2['job']
#       loadDict2.update(updateContent['job'])
#       newDict = dict(job=loadDict2)
#
#       f.seek(0)
#       f.truncate()
#       read_file.seek(0)
#       read_file.truncate()
#       f.write(json.dumps(newDict))
#       f.close()
#       unloadUpdate.pop("description")
#       for loop2 in loadDict:
#         if job_id == loop2['id']:
#           loop2.update(unloadUpdate)
#       newDict2 = dict(jobs=loadDict)
#       read_file.write(json.dumps(newDict2))
#       read_file.close()
#
#       tempResponse = {}
#       tempID = {}
#       tempID["id"] = job_id
#       tempResponse['jobs'] = tempID
#       js = json.dumps(tempResponse)
#       resp = Response(js, status=201, mimetype='application/json')
#     except:
#       resp = jsonify("ID Not Found")
#   return resp
  # return "success"

# # GET Job By ID
# @app.route('/api/job/get/<int:job_id>', methods=['GET'])
# def jobByID(job_id):
#   with open('../public/assets/content/jobs/data.json', 'r') as read_file:
#     data = json.load(read_file)
#     dictData = data['jobs']
#     try:
#       for loop in dictData:
#         if job_id == loop['id']:
#           selectedUser = loop
#       count = selectedUser['id']
#       f = open('../public/assets/content/jobs/job/'+str(count)+'.json', 'r')
#       data2 = json.load(f)
#       outDict = data2['job']
#       selectedUser.update(outDict)
#       f.close()
#       forResp = dict(jobs=selectedUser)
#       resp = jsonify(forResp)
#     except:
#       resp = jsonify("ID Not Found")
#   return resp

# #GET Latest article Data
# @app.route('/api/article/list', methods=['GET'])
# def latestArticleList():
#   with open('../public/assets/content/articles/data.json', 'r') as read_file:
#     data = json.load(read_file)
#     dictData = data['articles']
#     latestArticle = dictData[:]
#     temp = []
#     for loop in latestArticle:
#       count = loop['id']
#       f = open('../public/assets/content/articles/article/'+str(count)+'.json', 'r')
#       data2 = json.load(f)
#       outDict = data2['article']
#       loop.update(outDict)
#       f.close()
#
#     dictData.clear()
#     dictData.extend(latestArticle)
#     return jsonify(data)

# #GET Latest Thought Data
# @app.route('/api/thought/list', methods=['GET'])
# def latestThoughtList():
#   with open('../public/assets/content/thoughts/data.json', 'r') as read_file:
#     data = json.load(read_file)
#     dictData = data['thoughts']
#     latestThought = dictData[-6:]
#     temp = []
#     for loop in latestThought:
#       count = loop['id']
#       f = open('../public/assets/content/thoughts/thought/'+str(count)+'.json', 'r')
#       data2 = json.load(f)
#       outDict = data2['thought']
#       loop.update(outDict)
#       f.close()
#
#     dictData.clear()
#     dictData.extend(latestThought)
#     return jsonify(data)

# #GET Featured Jobs Data
# @app.route('/api/featjob/list', methods=['GET'])
# def featuredJobList():
#   with open('../public/assets/content/jobs/data.json', 'r') as read_file:
#     data = json.load(read_file)
#     dictData = data['jobs']
#     # latestThought = dictData[-6:]
#     temp = []
#     for loop in latestThought:
#       count = loop['id']
#       f = open('../public/assets/content/thoughts/thought/'+str(count)+'.json', 'r')
#       data2 = json.load(f)
#       outDict = data2['thought']
#       loop.update(outDict)
#       f.close()
#
#     dictData.clear()
#     dictData.extend(latestThought)
#     return jsonify(data)

# #GET Latest job Data
# @app.route('/api/job/list', methods=['GET'])
# def latestJobList():
#   with open('../public/assets/content/jobs/data.json', 'r') as read_file:
#     data = json.load(read_file)
#     dictData = data['jobs']
#     # print(dictData)
#     # latestJob = dictData[-6:]
#     # temp = []
#     # for loop in latestJob:
#     #   count = loop['id']
#     #   f = open('../public/assets/content/jobs/job/'+str(count)+'.json', 'r')
#     #   data2 = json.load(f)
#     #   outDict = data2['job']
#     #   loop.update(outDict)
#     #   f.close()
#     #
#     # dictData.clear()
#     # dictData.extend(latestJob)
#     return jsonify(data)

# #GET all jobs Data
# @app.route('/api/job/listall', methods=['GET'])
# def allJobList():
#   with open('../public/assets/content/jobs/data.json', 'r') as read_file:
#     data = json.load(read_file)
#     dictData = data['jobs']
#     print(dictData)
#     # temp = []
#     # for loop in latestNews:
#     #   count = loop['id']
#     #   f = open('../public/assets/content/articles/article/'+str(count)+'.json', 'r')
#     #   data2 = json.load(f)
#     #   outDict = data2['data']
#     #   loop.update(outDict)
#     #   f.close()
#     #
#     dictData.clear()
#     # dictData.extend(latestArticle)
#     # with open()
#     return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
