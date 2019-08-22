import Controller from '@ember/controller';

export default Controller.extend({
    newName: '',
    newPosition:'',
    newDate: '',
    newImgPerson: '',
    newThought: '',
    imageOptions:{
      plugins:'paste code',
      branding:false,
      menubar: false,
      toolbar: false,
      paste_data_images: true,
      image_advtab: true,
      height: 300,
  },
    ownOptions:{
        branding: false,
        plugins: 'code print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount imagetools colorpicker textpattern help',
        toolbar: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent | removeformat',
        image_advtab: true,
        height: 400
    },
    actions:{
        saveThought(){
            const name = this.get('newName');
            const position = this.get('newPosition');
            const date = this.get('newDate');
            const thought = this.get('newThought');
            const thumbThought = this.get('newImgPerson');

            const newThought = this.get('store').createRecord('thought',{
                name: name,
                position: position,
                date: date,
                thought: thought,
                thumbThought: thumbThought
            });
            // newArticle.save().catch(() => {});
            newThought.save();

            this.set('newName', '');
            this.set('newPosition', '');
            this.set('newDate', '');
            this.set('newThought', '');
            this.set('newImgPerson','');
        }
    }
});
