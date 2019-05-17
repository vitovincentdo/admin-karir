import Controller from '@ember/controller';

export default Controller.extend({
    newTitle: '',
    newDate: '',
    newImage: '',
    newContent: '',
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
    },
    actions:{
        saveArticle(){
            const title = this.get('newTitle');
            const date = this.get('newDate');
            const thumbImage = this.get('newImage');
            const article = this.get('newContent');

            const newArticle = this.get('store').createRecord('article',{
                title: title,
                date: date,
                article: article,
                thumbImage:thumbImage
            })
            // newArticle.save().catch(() => {});
            newArticle.save();

            this.set('newTitle', '');
            this.set('newDate', '');
            this.set('newContent', '');
            this.set('newImage', '');
        }
    }
});
