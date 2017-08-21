'use strict';
const checkToken = function(response) {
    if (response.status >= 200 && response.status < 300) {
      return response;
    } 
    else{
    if(response.status == 404){
    	location.href = '/goto';
    }
      let error = new Error(response.statusText);
      error.response = response;
      throw error;
    }
};
export default checkToken ;