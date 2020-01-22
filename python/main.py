from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import json
import os
import shutil
from PUT.PUT import put
from switcher import Switcher
from POST.POST import post
from getByID import getById


"""This is the main python file, all the POST, PUT, DELETE, GET BY ID, and GET ALL request will be handled here by using flask microframework."""

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# POST article Data
@app.route('/api/article/post', methods=['POST'])
def postJsonArticleHandler():
  content = request.get_json()
  forSwitching = Switcher()
  forHandling = post()
  forSwitching.setContent(content)
  if os.path.exists('../public/assets/content/articles/data.json'):
    forSwitching.properties('articleExist')
    forHandling.POSTArticle(forSwitching.getID(), forSwitching.getContent(), 'article')
  else:
    forSwitching.properties('articleNotExist')
    forHandling.POSTArticle(forSwitching.getID(), forSwitching.getContent(), 'article')

  tempID = dict(id=forSwitching.getID())
  tempResponse = dict(articles=tempID)
  js = json.dumps(tempResponse)
  resp = Response(js, status=201, mimetype='application/json')
  return resp


# GET Article By ID
@app.route('/api/article/get/<int:article_id>', methods=['GET'])
def articleByID(article_id):
  getFromID = getById()
  getFromID.setID(article_id)
  data = getFromID.getByIdOuter('article')
  resp = jsonify(data)
  return resp


# GET All article Data
@app.route('/api/article/list', methods=['GET'])
def allArticleList():
  with open('../public/assets/content/articles/data.json', 'r') as read_file:
    data = json.load(read_file)
    return jsonify(data)


# PUT Article Data
@app.route('/api/article/update/<int:article_id>', methods=['PUT'])
def updateArticle(article_id):
  updateContent = request.get_json()
  executePUT = put(article_id, updateContent)
  executePUT.updateArticle()

  tempID = dict(id=executePUT.getID())
  tempResponse = dict(articles=tempID)
  js = json.dumps(tempResponse)
  resp = Response(js, status=200, mimetype='application/json')
  return resp


# DELETE Article Data
@app.route('/api/article/delete/<int:article_id>', methods=['DELETE'])
def deleteArticle(article_id):
  path = '../public/assets/content/articles/'
  with open(path + 'data.json', 'r+') as read_file:
    data = json.load(read_file)
    loadDict = data['articles']

    filterData = [item for item in loadDict if item['id'] != article_id]
    existsInnerData = os.path.isfile(path + 'article/' + str(article_id) + '.json')
    existImageDir = os.path.isdir(path + 'article-image/' + str(article_id))
    if existsInnerData:
      os.remove(path + 'article/' + str(article_id) + '.json')
    if existImageDir:
      shutil.rmtree(path + 'article-image/' + str(article_id))

    openTag = open(path + 'tag.json', 'r+')
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
  forSwitching = Switcher()
  forHandling = post()
  forSwitching.setContent(content)
  if os.path.exists('../public/assets/content/thoughts/data.json'):
    forSwitching.properties('thoughtExist')
    forHandling.POSThought(forSwitching.getID(), forSwitching.getContent(), 'thought')
  else:
    forSwitching.properties('thoughtNotExist')
    forHandling.POSThought(forSwitching.getID(), forSwitching.getContent(), 'thought')

  tempID = dict(id=forSwitching.getID())
  tempResponse = dict(thoughts=tempID)
  js = json.dumps(tempResponse)
  resp = Response(js, status=201, mimetype='application/json')
  # resp.headers['Link'] = 'http://localhost:81'
  return resp


# GET Thought By ID
@app.route('/api/thought/get/<int:thought_id>', methods=['GET'])
def thoughtByID(thought_id):
  getFromID = getById()
  getFromID.setID(thought_id)
  data = getFromID.getByIdOuter('thought')
  resp = jsonify(data)
  return resp


# GET All Thought Data
@app.route('/api/thought/list', methods=['GET'])
def allThoughtList():
  with open('../public/assets/content/thoughts/data.json', 'r') as read_file:
    data = json.load(read_file)
    return jsonify(data)


# PUT Thought Data
@app.route('/api/thought/update/<int:thought_id>', methods=['PUT'])
def updateThought(thought_id):
  updateContent = request.get_json()
  executePUT = put(thought_id, updateContent)
  executePUT.updateThought()

  tempID = dict(id=executePUT.getID())
  tempResponse = dict(articles=tempID)
  js = json.dumps(tempResponse)
  resp = Response(js, status=200, mimetype='application/json')
  return resp


# DELETE Thought Data
@app.route('/api/thought/delete/<int:thought_id>', methods=['DELETE'])
def deleteThought(thought_id):
  path = '../public/assets/content/thoughts/'
  with open(path + 'data.json', 'r+') as read_file:
    data = json.load(read_file)
    loadDict = data['thoughts']

    filterData = [item for item in loadDict if item['id'] != thought_id]
    existsInnerData = os.path.isfile(path + 'thought/' + str(thought_id) + '.json')
    existImageDir = os.path.isdir(path + 'thoughts-image/' + str(thought_id))
    if existsInnerData:
      os.remove(path + 'thought/' + str(thought_id) + '.json')
    if existImageDir:
      shutil.rmtree(path + 'thoughts-image/' + str(thought_id))

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
  forSwitching = Switcher()
  forHandling = post()
  forSwitching.setContent(content)
  if os.path.exists('../public/assets/content/jobs/data.json'):
    forSwitching.properties('jobExist')
    forHandling.POSTJob(forSwitching.getID(), forSwitching.getContent(), 'job')
  else:
    forSwitching.properties('jobNotExist')
    forHandling.POSTJob(forSwitching.getID(), forSwitching.getContent(), 'job')

  tempID = dict(id=forSwitching.getID())
  tempResponse = dict(jobs=tempID)
  js = json.dumps(tempResponse)
  resp = Response(js, status=201, mimetype='application/json')

  return resp


# GET Job By ID
@app.route('/api/job/get/<int:job_id>', methods=['GET'])
def jobByID(job_id):
  getFromID = getById()
  getFromID.setID(job_id)
  data = getFromID.getByIdOuter('job')
  resp = jsonify(data)
  return resp


# GET All Job Data
@app.route('/api/job/list', methods=['GET'])
def allJobList():
  with open('../public/assets/content/jobs/data.json', 'r') as read_file:
    data = json.load(read_file)
    return jsonify(data)


# PUT Job Data
@app.route('/api/job/update/<int:job_id>', methods=['PUT'])
def updateJob(job_id):
  updateContent = request.get_json()
  executePUT = put(job_id, updateContent)
  executePUT.updateJob()

  tempID = dict(id=executePUT.getID())
  tempResponse = dict(articles=tempID)
  js = json.dumps(tempResponse)
  resp = Response(js, status=200, mimetype='application/json')
  return resp


# DELETE Job Data
@app.route('/api/job/delete/<int:job_id>', methods=['DELETE'])
def deleteJob(job_id):
  path = '../public/assets/content/jobs/'
  with open(path + 'data.json', 'r+') as read_file:
    data = json.load(read_file)
    loadDict = data['jobs']

    filterData = [item for item in loadDict if item['id'] != job_id]
    existsInnerData = os.path.isfile(path + 'job/' + str(job_id) + '.json')
    existImageDir = os.path.isdir(path + 'jobs-image/' + str(job_id))
    if existsInnerData:
      os.remove(path + 'job/' + str(job_id) + '.json')
    if existImageDir:
      shutil.rmtree(path + 'jobs-image/' + str(job_id))

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


if __name__ == '__main__':
  app.run(debug=True)
