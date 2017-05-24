'use strict';
import StorageUtil from 'utils/storage';

const checkStatus = (nextState, replace) => {
  let user = StorageUtil.get('user'),
      token = StorageUtil.get('token');

  if (!user && !token) {
    replace({ pathname: '/goto' });
  }
};

export default checkStatus;
