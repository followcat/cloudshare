'use strict';
const checkResponse = function(response) {
    if (response.status >= 200 && response.status < 300) {
      return response;
    } 
    else{
    if(response.status == 401){
    	location.href = '/index';
    }
      let error = new Error(response.statusText);
      error.response = response;
      throw error;
    }
};
export default checkResponse ;