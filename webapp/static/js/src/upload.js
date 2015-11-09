/*
		HTML5 file upload
		ajax
*/
define('Upload', function(){

	function Upload(formname){
		this.form = document.getElementById(formname);
	}


	Upload.prototype.Uploadfile = function(func){
		var aForm = this.form;

		if( aForm["file"].files.length > 0 )
		{
			var file = aForm["file"].files[0];
			console.log(file);
			//build formdata object
			var formData = new FormData();
			formData.append('file', file);
			

			var xhr = new XMLHttpRequest();
			// var upload = xhr.upload;

			// var p = document.createElement('p');
			// p.textContent = "0%";
			// progressbar.appendChild(p);
			// upload.progressbar = progressbar;
			xhr.open("POST", aForm.action);
			//add upload file evnet function

			xhr.addEventListener("progress", function(event){
				console.log("profress" + this);
				var progressbar = document.getElementById("progressbar");
				if(event.lengthComputable)
				{
					progressbar.innerHTML = "Received " + event.position + " of " + event.totalSize + "bytes";
				}
			}, false);

			xhr.addEventListener("load", function(){
				if( (xhr.status >= 200 && xhr.status < 300) || xhr.status == 304 )
				{
					var successMsg = document.createElement('p');
					var text = document.createTextNode("Upload Success! Skipping page.");
					successMsg.appendChild(text);
					aForm.appendChild(successMsg);
					func();
				}
				else
				{
					var failMsg = document.createElement('p');
					var text = document.createTextNode("Upload Fail! Please Try it again.");
					successMsg.appendChild(text);
					aForm.appendChild(successMsg);
				}
			}, false);

			xhr.addEventListener("error", Upload.Error, false);

			//upload file
			
			xhr.overrideMimeType("application/octet-stream");
			xhr.send(formData);
		}
		else
		{
			var msg = document.createElement('p');
			msg.appendChild("Plese choose a file");
			aForm.appendChild(p);
		}
	};


	return Upload;
});