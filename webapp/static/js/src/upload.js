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
			var progressmsg = document.getElementById("progressmsg");
			xhr.addEventListener('loadstart', function(event){
				var img = document.createElement("img");
				img.src = "/static/images/uploading.gif";
				img.alt = "loading";
				var span = document.createElement("span");
				span.innerHTML = "Uploading";
				progressmsg.appendChild(img);
				progressmsg.appendChild(span);

				var a = document.createElement("a");
				a.href = "javascript:;";
				a.innerHTML = "cancel";
				progressmsg.appendChild(a);
				a.onclick = function(){
					xhr.abort();
					xhr = null;
				};
			}, false);

			xhr.addEventListener('abort', function(){
				progressmsg.innerHTML = "";
			}, false);

			xhr.addEventListener("progress", function(event){

				if(event.lengthComputable)
				{
					progressmsg.innerHTML = "Received " + event.loaded + " of " + event.total + " bytes" + "<br>";
				}
			}, false);

			xhr.addEventListener("load", function(){
				if( (xhr.status >= 200 && xhr.status < 300) || xhr.status == 304 )
				{
					var img = document.createElement("img");
					img.src = "/static/images/yes.png";
					img.alt = "yes";
					var successMsg = document.createElement('span');
					var text = document.createTextNode("Upload Success! Skipping page.");
					successMsg.appendChild(text);
					progressmsg.appendChild(img);
					progressmsg.appendChild(successMsg);
					func();
				}
				else
				{
					var img = document.createElement("img");
					img.src = "/static/images/no.png";
					img.alt = "no";
					var failMsg = document.createElement('span');
					var text = document.createTextNode("Upload Fail! Please Try it again.");
					failMsg.appendChild(text);
					progressmsg.appendChild(img);
					progressmsg.appendChild(failMsg);
				}
			}, false);

			xhr.addEventListener("error", function(event){
				console.log(event);
				progressmsg.innerHTML = "Error." + Upload.Error;
			}, false);

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