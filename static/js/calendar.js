function reset_events(){
    document.getElementById('events').innerHTML = ""
}

// ajax call the get the dates and times of a training event.
function getTimes(elem){
    let trainingday = $(elem)
    let date_str = trainingday.attr('id') 

    var fdata = new FormData();
    const csrftoken = $("[name=csrfmiddlewaretoken]").val();
    fdata.append('csrfmiddlewaretoken', csrftoken);
    fdata.append('date', date_str);
  
    
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/training_courses/get-times/");
    
    xhr.onreadystatechange = function(){
      if(xhr.readyState === 4){
        if(xhr.status === 200){
          var response = JSON.parse(xhr.responseText);      
          for(var k=0; k<response.length; k++){  
            upload_files_toAWS_loads(response[k], files);          
          }  
        }
        else{
          alert("Could not get times");
        }
      }
    };
    xhr.send(fdata);
}