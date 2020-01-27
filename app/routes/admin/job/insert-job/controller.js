import Controller from '@ember/controller';

export default Controller.extend({
  jobName: '',
  jobSpecialization: '',
  jobLocation: '',
  newImgJob: '',
  jobDescription: '',
  jobQualification: '',
  flagFeatured: false,
  jobUrl: '',
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
  actions: {
    valueChanged(value) {
      this.set('flagFeatured', value);
    },
    saveJob() {
      const name = this.get('jobName');
      const specialization = this.get('jobSpecialization');
      const location = this.get('jobLocation');
      const description = this.get('jobDescription');
      const qualification = this.get('jobQualification');
      const thumbJob = this.get('newImgJob');
      const featured = this.get('flagFeatured');
      const url = this.get('jobUrl');

      const newJob = this.get('store').createRecord('job', {
        name: name,
        specialization: specialization,
        location: location,
        description: description,
        qualification: qualification,
        thumbJob: thumbJob,
        featured: featured,
        url: url
      })
      // newArticle.save().catch(() => {});
      newJob.save();

      this.set('jobName', '');
      this.set('jobSpecialization', '');
      this.set('jobLocation', '');
      this.set('jobDescription', '');
      this.set('jobQualification', '');
      this.set('newImgJob', '');
      this.set('flagFeatured', '');
      this.set('jobUrl', '');
    }
  }
});
