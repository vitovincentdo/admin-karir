import Route from '@ember/routing/route';

export default Route.extend({
  model(){
    return this.get('store').findAll('thought');
  },

  actions:{
    deleteThought(thought){
      let confirmation = confirm('Are you sure?')

      if (confirmation){
        thought.destroyRecord();
      }
    }
  }
});
