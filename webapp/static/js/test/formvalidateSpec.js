define(['jquery','formvalidate'], function($,validation) {
	var result;
	describe("Test the form of ValidateAccount: ", function(){
		it("The text is Chinese", function(){
			result =  validation.ValidateAccount("中文");
			expect(result).toEqual(false);
		});

		it("The text is more than 20 lengths", function(){
			result =  validation.ValidateAccount("123456789123456789123");
			expect(result).toEqual(false);
		});

		it("The text is null", function(){
			result = validation.ValidateAccount("");
			expect(result).toEqual(false);
		});

		it("The text has special symbol likes @!#$%", function(){
			result = validation.ValidateAccount("!@1234");
			expect(result).toEqual(false);
			result = validation.ValidateAccount("@!#$%");
			expect(result).toEqual(false);
			result = validation.ValidateAccount("asojhgfa%");
			expect(result).toEqual(false);
		});

		it("The text consisted of underline or number or letter" ,function(){
			result = validation.ValidateAccount("_hello1010");
			expect(result).toEqual(true);
		})

		it("The text consisted of number or letter" ,function(){
			result = validation.ValidateAccount("hello1010");
			expect(result).toEqual(true);
		})

		it("The text consisted of number" ,function(){
			result = validation.ValidateAccount("20151020");
			expect(result).toEqual(true);
		})

		it("The text consisted of letter" ,function(){
			result = validation.ValidateAccount("helloworld");
			expect(result).toEqual(true);
		})

	});


	describe("Test the form of ValidatePassword", function(){
		
	})
		

});