import Controller from '@ember/controller';

export default Controller.extend({
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
      plugins: 'paste code print preview searchreplace autolink directionality visualblocks visualchars fullscreen image link media template codesample table charmap hr pagebreak nonbreaking anchor toc insertdatetime advlist lists textcolor wordcount imagetools colorpicker textpattern help',
      toolbar: 'formatselect | bold italic strikethrough forecolor backcolor | link | alignleft aligncenter alignright alignjustify  | numlist bullist outdent indent | removeformat | image code | paste',
      paste_data_images: true,
      image_advtab: true,
      height: 400,
  }
});
