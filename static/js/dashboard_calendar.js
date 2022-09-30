let frm = document.getElementById("trainingform")

frm.onsubmit = function(e){
    e.preventDefault();
    $('.seldate-container').each( function(index, val){
        
        let dates_arr = []
        dates_arr.push($(this).attr('data-date'))
        
        let times = val.querySelectorAll('.timelabel')
        console.log(times)
        times.forEach(function(vl){
            dates_arr.push($(vl).attr("data-time"))
        })
        let input = document.createElement("input")
        input.setAttribute('type', 'hidden')
        input.setAttribute('name', 'trainingdate')
        input.setAttribute('value', dates_arr)
        frm.appendChild(input)
    });

    frm.submit()
}


let seldate_form = document.querySelectorAll(".formset-container")
let seldates_form = document.querySelector("#trainingform")
let totalForms = document.querySelector("#id_form-TOTAL_FORMS")
let formNum = seldate_form.length-1

function selectday(elem){
    let day = $(elem)
    let date = day.attr("data-day")
    if(day.attr("data-dayselected") == "0"){
        day.css("background-color", "green")
        day.attr("data-dayselected", "1")
        let newForm = seldate_form[0].cloneNode(true)
        let formRegex = RegExp(`form-(\\d+)-`,'g')
        formNum++
        newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
        newForm.style.display = "grid"
        newForm.querySelector(`#id_form-${formNum}-seldate`).value = date
        newForm.setAttribute('id', `${date}sd`)
        
        seldates_form.prepend(newForm)
        totalForms.setAttribute('value', `${formNum+1}`)
        
    }else if(day.attr("data-dayselected") == "1"){
        day.css("background-color", "white")
        day.attr("data-dayselected", "0")
        document.getElementById(''+date+'sd').remove()
        document.querySelector("#id_form-TOTAL_FORMS").value = formNum--
    } 
}

function addtime(elem){
    
    let day = $(elem)
    let container = day.closest('.formset-container')
    let datestr = container.attr('id').slice(0, -2)

    let time_input = $(container).find(".trtime")
    let times_container = $(container).find(".times-container")
    
    let newForm = seldate_form[0].cloneNode(true)
    let formRegex = RegExp(`form-(\\d+)-`,'g')
    formNum++
    newForm.innerHTML = newForm.innerHTML.replace(formRegex, `form-${formNum}-`)
    
    newForm.querySelector(`#id_form-${formNum}-seldate`).value = datestr
    newForm.classList.add(`${datestr}sd`)
    
    seldates_form.prepend(newForm)
    totalForms.setAttribute('value', `${formNum+1}`)
    
    newForm.querySelector(`#id_form-${formNum}-seltime`).value = time_input.val()
    let time = time_input.val()
  
    if(time != ""){
        times_container.append('<div class="timelabel" data-datestr="'+datestr+'" data-time="'+time+'">"'+time+'"<span class="close" onclick=removetime(this)>&times;</span><div/>')
    }

}

function removetime(elem){
    let time = $(elem)
    let timelbl = time.closest('.timelabel')[0]
    let datestr = $(timelbl).attr("data-datestr")
    let dateinput = $("."+datestr+"sd")[0]
    dateinput.remove()
    timelbl.remove()
    // time.closest('.timelabel')[0].remove()

}

function distime(elem){
    console.log($(elem).val())
}
