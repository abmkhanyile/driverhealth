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

function getComments(elem){
  let rbtn = $(elem)  
  for(let i=0; i < document.querySelectorAll('.comment').length; i++){
    document.querySelectorAll('.comment')[i].style.display = "none"
  }
  $("#"+rbtn.val()+"").css('display', 'block')
}

let tform = document.querySelectorAll(".time-cont")
let times_form = document.querySelector("#timesform")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")
let formNum = tform.length-1

function addtime_form(elem, i){  
  let newForm = tform[0].cloneNode(true)
  newForm.style.display = "flex"
  let formRegex = RegExp(`form-(\\d+)-`,'g')
  formNum++
  
  newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    
  let trtimes_container = elem.closest('.tr-times')
  let timestags = elem.children('.timeobjs') 
  
  $(newForm).find('[for="'+`id_form-${formNum}-time`+'"]')[0].innerHTML = timestags[i].dataset.time

  newForm.querySelector(`#id_form-${formNum}-timepk`).value = timestags[i].dataset.timepk
   
  trtimes_container.prepend(newForm)
  totalForms.setAttribute('value', `${formNum+1}`)
}


$('.times-qty').each(function(index){
  let times_qtys = parseInt($(this).attr("data-timeslen"))
  if(times_qtys > 0){
    for(let i=0; i<times_qtys; i++){
      addtime_form($(this), i)
    }
  }
})

function display_tot(){
  document.getElementById("booking-summary").style.display = "block"
  let cboxes = document.querySelectorAll('.timecb')
  let hrs = 0
  for(let i=0; i<cboxes.length; i++){
    if(cboxes[i].checked){
      hrs++
    }
  }
  document.getElementById('hrs-num').innerHTML = hrs
  let cprice = parseFloat(document.getElementById('course-price').getAttribute('data-courseprice'))
  let tot = cprice * hrs
  document.getElementById('coursecost').innerHTML = tot
  
}
