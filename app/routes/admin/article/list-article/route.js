import Route from '@ember/routing/route';

export default Route.extend({
  model(){
    return this.get('store').findAll('article');
  },

  actions:{
    deleteArticle(article){
      let confirmation = confirm('Are you sure?');

      if(confirmation){
        article.destroyRecord();
      }
    }
  }
});
