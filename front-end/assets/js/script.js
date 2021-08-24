// Element variables definitions
// const inpFile = document.getElementById("input-image"); //ok
const previewImage = document.getElementById("preview-image"); //ok
const rawImage = document.getElementById("raw-image"); //ok
const resultImage = document.getElementById("processed-image"); //ok
const resultDefaultText = document.getElementById("output-count"); //ok
const inpUrl = document.getElementById("input-url"); //ok
const inputCard = document.getElementById("input-card"); //ok
const outputCard = document.getElementById("output-card"); //ok

var resultJson;
//const baseUrl = 'http://127.0.0.1:5000/process';
//const baseUrl = 'https://grain-count-flask-api.herokuapp.com/process'
const baseUrl = 'https://grain-count-api.herokuapp.com/process';

// Event listener for uploaded image input tag
//      encodes uploaded image
//      set preview image and raw image sources
// inpFile.addEventListener("change", () => {
//     const file = this.files[0];
//     if (file) {
//         const reader = new FileReader();

//         reader.addEventListener("load", () => {
//             console.log(this.result);

//             previewImage.style.display = "block";
//             previewImage.setAttribute("src", this.result);
//             rawImage.setAttribute("src", this.result);
//             console.log("previewImage.setAttribute(src, this.result); " + previewImage.src);
//         });

//         reader.readAsDataURL(file);
//     } else {
//         previewImage.style.display = null;
//         previewImage.setAttribute("src", "./processing.png");
//         rawImage.setAttribute("src", "./processing.png");
//         console.log("previewImage.src " + previewImage.src);
//     }
// });


// Result Image change function
//      called when respose is received
//      handles response image and creates URI
//      sets result count text, result image source
function resultImageChange(resultJson) {
    if (resultJson) {
        resultDefaultText.innerHTML = resultJson["count"];
        //resultImage.style.display = "block";
        let bytestring = resultJson["outputImage"];
        let image = bytestring.split('\'')[1];
        image = 'data:image/jpeg;base64,' + image;
        resultImage.setAttribute("src", image);
    } else {
        resultDefaultText.style.display = null;
        resultImage.style.display = null;
        resultImage.setAttribute("src", "./processing.png");
    }
};

// HTTP POST request
//      called on showResults function
function postRequest() {
    var Http = new XMLHttpRequest();
    var requestUrl = baseUrl;
    var requestBody = JSON.stringify({});
    console.log("previewImage.src: " + previewImage.src)

    // Setting request url
    if (inpUrl.value) {
        requestUrl = inpUrl.value;
    }

    // Setting request data
    if (!(previewImage.src.includes("processing.png"))) {
        requestBody = { 'inputImage': encodeURIComponent(previewImage.src) };
        requestBody = JSON.stringify(requestBody);
        //requestBody = "inputImage="+encodeURIComponent(previewImage.src);
    }

    // Sending request
    console.log("requestBody: " + JSON.stringify(requestBody));

    Http.open("POST", requestUrl);
    //Http.withCredentials = true;
    Http.setRequestHeader("Content-Type", "application/json");
    Http.send(requestBody);

    // Setting response
    Http.onreadystatechange = () => {
        if (this.readyState == 4 && this.status == 200) {
            var resultJson = JSON.parse(Http.response);
            resultImageChange(resultJson);
            console.log("get request finished: " + resultJson["name"]);
        }
    }
};

// Function to show results wrapper and call http request function
//      called onclick of input submit tag
function showResults() {

    //getRequest();
    postRequest();

    inputCard.style.display = 'none';
    outputCard.style.display = 'block';
}

// Funtion to reset everything possible
function resetResults() {

    resultDefaultText.innerHTML = "";
    previewImage.style.display = null;
    previewImage.setAttribute("src", "./processing.png");
    rawImage.setAttribute("src", "./processing.png");
    resultImage.setAttribute("src", "./processing.png");

    previewImage.style.display = null;
    previewImage.setAttribute("src", "./processing.png");

    inputCard.style.display = 'block';
    outputCard.style.display = 'none';
}

/*
// Deprecated get request
var getRequest = function () {
    var Http = new XMLHttpRequest();
    var requestUrl = "";
    console.log("previewImage.src: "+ previewImage.src)

    // Setting request url
    if (inpUrl.value){
        requestUrl = inpUrl.value;
    } else {
        requestUrl = baseUrl;
    }

    // Setting request data
    if (!(previewImage.src.includes("processing.png")) ){
        var requestUrlComplete = requestUrl + "?inputImage=" + encodeURIComponent(previewImage.src);
    } else {
        var requestUrlComplete = requestUrl;
    }

    // Sending request
    console.log("requestUrlComplete: "+requestUrlComplete);
    Http.open("GET", requestUrlComplete);
    Http.send();

    // Setting response
    Http.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            var resultJson = JSON.parse(Http.response);
            resultImageChange(resultJson);
            console.log("get request finished: "+resultJson["name"]);
        }
    }
};
*/