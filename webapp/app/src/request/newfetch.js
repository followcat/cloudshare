'use strict';

import checkResponse from 'utils/check-response';

const newFetch = (api,params) => {
  return fetch(api,params)
         .then(checkResponse)
};

export { newFetch };