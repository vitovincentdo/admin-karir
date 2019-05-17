import EmberRouter from '@ember/routing/router';
import config from './config/environment';

const Router = EmberRouter.extend({
  location: config.locationType,
  rootURL: config.rootURL
});

Router.map(function() {
  this.route('routes', { path: '/' }, function() {
    this.route('admin', function() {
      this.route('article', function() {
        this.route('insert-article');
        this.route('list-article');
        this.route('edit-article', {path: '/:article_id/edit'});
      });

      this.route('thought', function() {
        this.route('insert-thought');
        this.route('list-thought');
        this.route('edit-thought', {path: '/:thought_id/edit'});
      });

      this.route('job', function() {
        this.route('insert-job');
        this.route('list-job');
        this.route('edit-job', {path: '/:job_id/edit'});
      });
      this.route('counter');
    });
  });
});

export default Router;
