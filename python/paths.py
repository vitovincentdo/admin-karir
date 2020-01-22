
"""
This class is only used for declaring path to file or to folder

Example:

```python
from paths import Path

retrievePath = Path() #declare Path
read_file = open(retrievePath.pathArticleData, 'r') #open a file data.json inside article folder
"""

class Path():

  def __init__(self):
    self.pathArticleTag = '../public/assets/content/articles/tag.json'
    self.pathArticleData = '../public/assets/content/articles/data.json'
    self.pathFolderArticle = '../public/assets/content/articles'
    self.pathThoughtData = '../public/assets/content/thoughts/data.json'
    self.pathFolderThought = '../public/assets/content/thoughts'
    self.pathJobData = '../public/assets/content/jobs/data.json'
    self.pathFolderJob = '../public/assets/content/jobs'
    self.pathArticleImage = '../public/assets/content/articles/article-image'
    self.pathThoughtImage = '../public/assets/content/thoughts/thoughts-image'
    self.pathJobImage = '../public/assets/content/jobs/job-image'
