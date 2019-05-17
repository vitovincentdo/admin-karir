import Controller from '@ember/controller';

export default Controller.extend({
  NewEmployeeCount:'',
  actions:{
    saveCount(){
      const employCount = this.get('NewEmployeeCount');
      const newCount = this.get('store').createRecord('counter',{
        employCount
      })
      newCount.save();
      this.set('NewEmployeeCount', '');
    }
  }
});
