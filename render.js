document.getElementById("displaytext").style.display = "none";

function searchPhoto() {
  var image_message = document.getElementById("note-textarea").value; 
  console.log(image_message);
  
  const Http = new XMLHttpRequest();
  var url='https://39jsof67kd.execute-api.us-east-1.amazonaws.com/dev/search?q='+image_message;
  Http.open("GET", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    if (Http.readyState == 4 && Http.status == 200){
      console.log(Http.responseText)
      var response_data = JSON.parse(Http.responseText);
      console.log(response_data);
      console.log(typeof(response_data))
      length_of_response = response_data.length;
      console.log(length_of_response)

      if (length_of_response == 0) {
        document.getElementById("displaytext").innerHTML = "No Images Found"
        document.getElementById("displaytext").style.display = "block";
      }
      
      response_data.forEach(function (obj) {
      var img = new Image();
      img.src = obj;
      img.setAttribute("class", "banner-img");
      img.setAttribute("alt", "effy");
      img.setAttribute("width", "170");
      img.setAttribute("height", "170");
      document.getElementById("displaytext").innerHTML = "Images"
      document.getElementById("img-container").appendChild(img);
      document.getElementById("displaytext").style.display = "block";
      })
    }    
  }
}

function searchPhotoVoice() {
  var image_message = document.getElementById("action").innerHTML; 
  console.log(image_message);
  
  const Http = new XMLHttpRequest();
  var url='https://39jsof67kd.execute-api.us-east-1.amazonaws.com/dev/search?q='+image_message;
  Http.open("GET", url);
  Http.send();

  Http.onreadystatechange = (e) => {
    if (Http.readyState == 4 && Http.status == 200){
      console.log(Http.responseText)
      var response_data = JSON.parse(Http.responseText);
      console.log(response_data);
      length_of_response = response_data.length;
      console.log(length_of_response)

      if (length_of_response == 0) {
        document.getElementById("displaytext").innerHTML = "No Images Found"
        document.getElementById("displaytext").style.display = "block";
      }
      
      response_data.forEach(function (obj) {
      var img = new Image();
      img.src = obj;
      img.setAttribute("class", "banner-img");
      img.setAttribute("alt", "effy");
      img.setAttribute("width", "170");
      img.setAttribute("height", "170");
      document.getElementById("displaytext").innerHTML = "Images"
      document.getElementById("img-container").appendChild(img);
      document.getElementById("displaytext").style.display = "block";
      })
    }
  }
}

function getBase64(file) {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      let encoded = reader.result.replace(/^data:(.*;base64,)?/, '');
      if ((encoded.length % 4) > 0) {
        encoded += '='.repeat(4 - (encoded.length % 4));
      }
      resolve(encoded);
    };
    reader.onerror = error => reject(error);
  });
}

function uploadPhoto() {
  var file = document.getElementById('file_path').files[0];
  const reader = new FileReader();

  if(document.getElementById("customlabels") != null){
    var customLabels = customlabels.value;
    console.log(customLabels)
  }
  console.log(file)

  var file_data;
  var encoded_image = getBase64(file).then(
    data => {
      console.log(data)
      console.log("after data")
      var apigClient = apigClientFactory.newClient({
        apiKey: "L9VpvG6pDG4qZeiUtsl8964hZTi2AE2D6uLjNsYo",
		    defaultContentType: "image/jpeg",
        defaultAcceptType: "image/jpeg",
      });
      var body = data;
      var params = {
        'x-amz-meta-customLabels': customLabels,
        "bucket": "b--2",
        "filename": file.name,
        "Content-Type" : "image/jpg;base64",
      };
      var additionalParams = {
      };

	    apigClient.uploadBucketFilenamePut(params, body, additionalParams).then(function (result) {
		  console.log(result)
		  console.log('success OK');
		  console.log(result.data);
      document.getElementById("uploadText").innerHTML = "Image Upload Successful"
		  }).catch(function (result) {
			  console.log(result);
			  })
	});
}
