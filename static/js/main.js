// start of the sidenav js
function openNav(sidenav) {
    document.getElementById(sidenav).style.animation = "expand 0.3s forwards";
    document.getElementById("closeBtn").style.display = "block";
    document.getElementById("closeBtn").style.animation = "show 0.3s";
    // page-overlay
    document.getElementById("page-overlay").style.display = "block";
    document.getElementById("page-overlay").style.animation = "show 0.3s";
  }
  
  function closeNav(sidevanv) {
    let ele = document.getElementById(sidevanv);
    
    if(ele.style.animation.includes('expand') == true){
      document.getElementById(sidevanv).style.animation = "collapse 0.3s forwards";
    }else{
      document.getElementById('mySidenav-submenu').style.animation = "collapse 0.3s forwards";
    }
    
    document.getElementById("closeBtn").style.animation = "hide 0.3s";
    // page-overlay
    document.getElementById("page-overlay").style.animation = "hide 0.3s";
  
    setTimeout(() => {
      document.getElementById("closeBtn").style.display = "none";
      document.getElementById("page-overlay").style.display = "none";
  }, 300);
  }
  // end of the sidenav js


  // password show/hide toggle eye.
function hide_show_pwd(elem){
  const togglePassword = $(elem); //document.querySelector("#togglePassword");
  const password = document.querySelector("#password");

  
    console.log("i am clicked")
    // toggle the type attribute
    const type = password.getAttribute("type") === "password" ? "text" : "password";
    password.setAttribute("type", type);
    // toggle the eye icon
    togglePassword.toggleClass('fa-eye');
    togglePassword.toggleClass('fa-eye-slash');
  
}

function checkSel(elem){
  let doctype = $(elem).val();
  if(doctype==6){
    $('#othertype').show();
  }else{
    $('#othertype').hide();
  }
}


async function get_signed_AWS_url() {
  let file = $('.clientdoc-fileinput').prop('files')[0];
  var fdata = new FormData();
  
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  fdata.append('csrfmiddlewaretoken', csrftoken);
  fdata.append('clientpk', $('#client_id').attr('data-clientid'));
  fdata.append('documents_name', file.name);
  fdata.append('doctype', $('.client-doctype').val());
  fdata.append('otherdoc_type', $('.client-otherdoctype').val());

  $('.form-overlay').css('display', 'block');
  $('.loader-icon').css('display', 'block');
 
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/dhclients/upload-client-doc/");
  xhr.files = file;
  xhr.onreadystatechange = function(){
    if(xhr.readyState === 4){
      if(xhr.status === 200){
        var response = JSON.parse(xhr.responseText);  
          console.log(response[0]); 
          upload_client_doc_toAWS(response[0], file);         
      }
      else{
        alert("Could not get signed URL.");
      }
    }
  };
  xhr.send(fdata);
}

function setDoc_visibility(elem){
  let doc_id = $(elem).data('docid');

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/dhclients/change-visibility/");
  
  var postData = new FormData();
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  postData.append('csrfmiddlewaretoken', csrftoken);
  postData.append("doc_pk", doc_id);
         
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200 || xhr.status === 204) {
        var response = JSON.parse(xhr.responseText);   
        console.log(response);  
      } else {
        alert("Could not upload file.");
      }
    }
  };
  xhr.send(postData);
}


// uploads driver document to amazon.
function upload_client_doc_toAWS(resp, file) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", resp.data.url);
  
  var postData = new FormData();
  for (key in resp.data.fields) {  
    postData.append(key, resp.data.fields[key]);
  }
  
  postData.append("file", file)
         
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200 || xhr.status === 204) {
        $('.form-overlay').css('display', 'none');
        $('.loader-icon').css('display', 'none');
        $('.success-msg').css('display', 'block');
      } else {
        alert("Could not upload file.");
        $('.loader-icon').css('display', 'none');
      }
    }
  };
  xhr.send(postData);
}


$(document).ready(function() {
  $('.clientdocs-form').submit(function() {
      $(this).find(':button[type=submit]').prop('disabled', true);

      // For this example, don't actually submit the form
      event.preventDefault();
  });

  $('#jobclosing_date, .startdate, .enddate').datepicker({  
    showAnim: 'drop',
    numberOfMonth: 1,
  });
});

function selfile(){
  console.log("btn clicked")
  $('#profpic_file').click();
}

function mouse_in(){
  $('#profpic_overlay').css('display', 'flex');
}
function mouse_out(){
  $('#profpic_overlay').css('display', 'none');
}

$('.imgcontainer').hover(mouse_in, mouse_out);

// handles the process of uploading a driver's profile pic
async function upload_img(elem) {
  let profile_image = $(elem)[0].files[0]
  var fdata = new FormData();
  const csrftoken = $("[name=csrfmiddlewaretoken]").val();
  fdata.append('csrfmiddlewaretoken', csrftoken);
  fdata.append('clientpk', $('#clientId').val());
  fdata.append('img_name', profile_image.name);

  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/dhclients/upload-image/");
  xhr.files = profile_image;
  xhr.onreadystatechange = function(){
    if(xhr.readyState === 4){
      if(xhr.status === 200){
        var response = JSON.parse(xhr.responseText);
          convert_img(response[0], profile_image);              
      }
      else{
        alert("Could not get signed URL.");
      }
    }
  };
  xhr.send(fdata);
}

function processContainer(){
  let containerDivs = $('*[data-loaded="false"]');
  $(containerDivs[0]).children("i").eq(0).hide();
  $(containerDivs[0]).children("progress").eq(0).show();
  containerDivs[0].setAttribute('data-loaded', 'true');
  return containerDivs[0];
}


// converts user uploaded profile pic to webp format to take advantage of webp's small file size and fast loading time.
function convert_img(response, image){
  let container = processContainer();
// Load the data into an image
new Promise(function (resolve, reject) {
  let rawImage = new Image();

  rawImage.addEventListener("load", function () {
    resolve(rawImage);
  });

  rawImage.src = URL.createObjectURL(image);
}).then(function (rawImage) {
  // Convert image to webp ObjectURL via a canvas blob
  return new Promise(function (resolve, reject) {
    let canvas = document.createElement('canvas');
    let ctx = canvas.getContext("2d");

    canvas.width = rawImage.width;
    canvas.height = rawImage.height;
    // if(response.aws_fname.substr(31, 12))
    console.log(response.aws_fname.substr(30, 12));
    ctx.drawImage(rawImage, 0, 0);

    canvas.toBlob(function (blob) {
      resolve(URL.createObjectURL(blob));
    }, "image/webp");
  });
}).then(function (imageURL) {
  // Load image for display on the page
  return new Promise(function (resolve, reject) {
    let scaledImg = new Image();

    scaledImg.addEventListener("load", function () {
      resolve({imageURL, scaledImg});
    });

    scaledImg.setAttribute("src", imageURL);
  });
}).then(function (data) {
  // Inject into the DOM
  fetch(data.imageURL)
    .then(function (response) {
       return response.blob();
    })
    .then(function (blob) {
      var file = new File([blob], `${image.name}`, {type: "image/webp"});
      upload_image_to_aws(response, file, container);
    });   
  
});
}

// uploads the image to aws s3 and returns an aws url to the image
function upload_image_to_aws(resp, img, container) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", resp.data.url);
  
  var postData = new FormData();
  for (key in resp.data.fields) {  
    postData.append(key, resp.data.fields[key]);
  }
  
  postData.append("file", img)
         
  xhr.onreadystatechange = function () {
    if (xhr.readyState === 4) {
      if (xhr.status === 200 || xhr.status === 204) {
        alert("Image uploaded successfully.")
        $(container).css({
          "background-image": "url(" + resp.url + ")",
          "background-size": "contain",
          "background-repeat": "no-repeat",
          "background-position": "center",
        });
        
        $(container).children("progress").eq(0).hide();
        $(container).children(".close_ad_btn").eq(0).show();
        $(container).children("input").val(resp.aws_fname);
        location.reload();
      } else {
        alert("Could not upload file.");
      }
    }
  };
  xhr.send(postData);
}


