// start of the sidenav js
function openNav() {
    document.getElementById("mySidenav").style.animation = "expand 0.3s forwards";
    document.getElementById("closeBtn").style.display = "block";
    document.getElementById("closeBtn").style.animation = "show 0.3s";
    // page-overlay
    document.getElementById("page-overlay").style.display = "block";
    document.getElementById("page-overlay").style.animation = "show 0.3s";
  }
  
  function closeNav() {
    document.getElementById("mySidenav").style.animation = "collapse 0.3s forwards";
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
});