import DS from 'ember-data';
import host from 'karir-admin/utils/host';
import { MODEL_PREFIX } from 'karir-admin/utils/properties';

export default DS.RESTAdapter.extend({
  urlForFindAll(modelName) {
    return host(`${this._removePrefix(modelName)}.search`);
  },

  urlForCreateRecord(modelName) {
      return host(`${this._removePrefix(modelName)}.create`);
  },

  urlForFindRecord(id, modelName) {
      return host(`${this._removePrefix(modelName)}.find`).replace(/:id/, id);
  },

  urlForUpdateRecord(id, modelName){
      const url = host(`${this._removePrefix(modelName)}.update`) + `/${id}`;
      return url
  },

  urlForDeleteRecord(id, modelName){
    return host(`${this._removePrefix(modelName)}.delete`).replace(/:id/, id);
  },

  _removePrefix(name) {
      return name.replace(`${MODEL_PREFIX}/`, '').replace(/\//g, '.');
  }
});
