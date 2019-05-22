import { HOST, ENVIRONMENT } from 'karir-admin/utils/properties';
import { get } from 'karir-admin/utils/short';

export default function host(key) {

  const host = HOST[ENVIRONMENT];

  const list = {
    'article':{
      create: `${host}/api/article/post`,
      search: `${host}/api/article/list`,
      find: `${host}/api/article/get/:id`,
      update: `${host}/api/article/update`,
      delete: `${host}/api/article/delete/:id`
    },
    'thought':{
      create: `${host}/api/thought/post`,
      search: `${host}/api/thought/list`,
      find: `${host}/api/thought/get/:id`,
      update: `${host}/api/thought/update`,
      delete: `${host}/api/thought/delete/:id`
    },
    'job':{
      create: `${host}/api/job/post`,
      search: `${host}/api/job/list`,
      find: `${host}/api/job/get/:id`,
      update: `${host}/api/job/update`,
      delete: `${host}/api/job/delete/:id`
    },
    'counter':{
      create: `${host}/api/counter/post`,
    }
    // 'person':{
    //   search: `${host}/rest/JDBC_Tutorial/test_retrieve`
    // }
  }

  return get(list, key);
}
