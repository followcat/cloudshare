define(['jquery','formvalidate'], function($,validation) {
	var account, password;

	describe("Test the input of text type: ", function(){
		it("The text is Chinese", function(){
			account =  validation.ValidateAccount("中文");
			expect(account).toEqual(false);
		});

		it("The text is more than 20 lengths", function(){
			account =  validation.ValidateAccount("123456789123456789123");
			expect(account).toEqual(false);
		});

		it("The text is null", function(){
			account = validation.ValidateAccount("");
			expect(account).toEqual(false);
		});

		it("The text has special symbol likes @!#$%", function(){
			account = validation.ValidateAccount("!@1234");
			expect(account).toEqual(false);
			account = validation.ValidateAccount("@!#$%");
			expect(account).toEqual(false);
			account = validation.ValidateAccount("asojhgfa%");
			expect(account).toEqual(false);
		});

		it("The text consisted of underline or number or letter" ,function(){
			account = validation.ValidateAccount("_hello1010");
			expect(account).toEqual(true);
		});

		it("The text consisted of number or letter" ,function(){
			account = validation.ValidateAccount("hello1010");
			expect(account).toEqual(true);
		});

		it("The text consisted of number" ,function(){
			account = validation.ValidateAccount("20151020");
			expect(account).toEqual(true);
		});

		it("The text consisted of letter" ,function(){
			account = validation.ValidateAccount("helloworld");
			expect(account).toEqual(true);
		});

	});


	describe("Test the form of password type", function(){
		it("The password is Chinese", function(){
			password =  validation.ValidatePassword("中文");
			expect(password).toEqual(false);
		});

		it("The password is more than 15 lengths or less than 6 lengths", function(){
			password =  validation.ValidatePassword("12345678912345678");
			expect(password).toEqual(false);
			password =  validation.ValidatePassword("12345");
			expect(password).toEqual(false);
		});

		it("The password is between 6 and 15 length", function(){
			password =  validation.ValidatePassword("12345156asd");
			expect(password).toEqual(true);
		});

		it("The password is null", function(){
			password = validation.ValidatePassword("");
			expect(password).toEqual(false);
		});

		it("The password has special symbol likes @!#$%", function(){
			password = validation.ValidatePassword("!@1234");
			expect(password).toEqual(false);
			password = validation.ValidatePassword("@!#$%");
			expect(password).toEqual(false);
			password = validation.ValidatePassword("asojhgfa%");
			expect(password).toEqual(false);
		});

		it("The password consisted of underline or number or letter" ,function(){
			password = validation.ValidatePassword("_hello1010");
			expect(password).toEqual(true);
		});

		it("The password consisted of number or letter" ,function(){
			password = validation.ValidatePassword("hello1010");
			expect(password).toEqual(true);
		});

		it("The password consisted of number" ,function(){
			password = validation.ValidatePassword("20151020");
			expect(password).toEqual(true);
		});

		it("The password consisted of letter" ,function(){
			password = validation.ValidatePassword("helloworld");
			expect(password).toEqual(true);
		});

	});
		
	describe("Test the confirm password", function(){
		var pwd, cofpwd, result;

		it("The confirm password is different to password", function(){
			pwd = "pwd951159";
			cofpwd = "8794513213";
			result = validation.ComparePassword(pwd, cofpwd);
			expect(result).toEqual(false);
		});

		it("The confirm password is the same to password", function(){
			pwd = "hello753";
			cofpwd = "hello753";
			result = validation.ComparePassword(pwd, cofpwd);
			expect(result).toEqual(true);
		});

	});

	describe("Test the blank input", function(){
		var text, result;

		it("The text is null", function(){
			text = "";
			result = validation.ValidateBlank(text);
			expect(result).toEqual(true);
			text = { value : "     "};
			expect(result).toEqual(true);
		});


	});

});