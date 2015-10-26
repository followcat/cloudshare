define(function(){
	var validation = {};

 	validation.ValidateAccount = function(str){
 		var reg = /^\w{1,20}$/;

		if(!reg.test(str))
		{
			return false;
		}
			
		return true;
 	}

 	validation.ValidatePassword = function(str){
 		var reg = /^\w{6,15}$/;

	    if(!reg.test(str))
	    {
	    	return false;
	    }
	    return true;
 	}

 	validation.ComparePassword = function(pwd, cofpwd){

 		if(pwd === cofpwd)
 		{
 			return true;

 		}else{
 			return false;
 		}
 	}

 	return validation;
})