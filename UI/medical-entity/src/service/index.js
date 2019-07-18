import axios from 'axios';
import {BASE_URL} from '../constant';

export const getEntityData = (path) => {
  return axios.get(BASE_URL, {
    params: {
      url: path
    }
  }).then(resp => {
    return resp;
  }, err => {
    return err;
  });
}