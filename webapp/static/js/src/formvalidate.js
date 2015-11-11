define(function(){
	var validation = {};

 	validation.ValidateAccount = function(str){
 		var reg = /^\w{1,20}$/;

		if(!reg.test(str))
		{
			return false;
		}
			
		return true;
 	};

 	validation.ValidatePassword = function(str){
 		var reg = /^\w{6,15}$/;

	    if(!reg.test(str))
	    {
	    	return false;
	    }
	    return true;
 	};

 	validation.ComparePassword = function(pwd, cofpwd){

 		if(pwd === cofpwd)
 		{
 			return true;

 		}else{
 			return false;
 		}
 	};

 	validation.ValidateBlank = function(arg){
 		
 		var reg = /^\s*$/g;

 		if(typeof arg == "object"){
 			for(var i = 0, len = arg.len; i < len; i++){
 				if( arg[i].value == "" || reg.test(arg[i].value)){
 					return true;
 				}else{
 					return false
 				}
 			}
 		}else{
 			if( arg === "" || reg.test(arg)){
	 			return true;
	 		}else{
	 			return false;
	 		}
 		}	
 	};

 	return validation;
});
