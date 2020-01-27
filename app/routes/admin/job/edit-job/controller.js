import Controller from '@ember/controller';

export default Controller.extend({
  ownOptions: {
    branding: false,
    plugins: 'code print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount imagetools colorpicker textpattern help',
    toolbar: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent | removeformat',
    image_advtab: true,
    height: 400,
    readonly: 1,
  },
  jobImageOptions: {
    plugins: 'paste code',
    branding: false,
    menubar: false,
    toolbar: false,
    paste_data_images: true,
    image_advtab: true,
    height: 300,
    readonly: 1,
  },
  actions:{
    valueHasChanged(value){
        this.set('model.featured', value);
    }
}
});
