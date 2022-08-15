function selectday(elem){
    let day = $(elem)
    let date = day.attr("data-day")
    if(day.attr("data-dayselected") == "0"){
        day.css("background-color", "green")
        day.attr("data-dayselected", "1")
        document.getElementById('selectedates').innerHTML += '<div class="seldate-container" id="'+date+'"><div class="seldate">'+date+'</div><div class="times-container"><div class="input-group mb-3" style="width: 15%;"><input type="time" class="form-control trainingtime" aria-describedby="basic-addon2"><div class="input-group-append"> <button class="btn btn-outline-secondary" type="button"  onclick="addtime(this)">Add</button></div></div></div></div>'
        
    }else if(day.attr("data-dayselected") == "1"){
        day.css("background-color", "white")
        day.attr("data-dayselected", "0")
        document.getElementById(date).remove()
    }
    
}

let frm = document.getElementById("trainingform")

frm.onsubmit = function(e){
    e.preventDefault();
    $('.seldate-container').each( function(index, val){
        
        let dates_arr = []
        dates_arr.push($(this).attr('id'))
        
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


// function compile_dates(elem, e){
//     // compilation goes here
//     let curr_ele = $(elem)
//     e.preventDefault();

//     // return true
//     $('.seldate-container').each( function(index){
        
//         let dates_arr = []
//         dates_arr.push($(this).attr('id'))
        
//         let times = $(this).querySelectorAll('.timelabel')
//         console.log(times)
//         // times.each(function(i, val){
//         //     console.log("hello")
//         // })
//         // if($(this).attr("data-dayselected") == "1"){
//         //     dates_arr.push($(this).attr('data-day'))
//         // }
//         // $('#dates_input').val(dates_arr)
//     });
    
// }

function addtime(elem){
    let day = $(elem)
    let time = day.closest('.times-container').find('.trainingtime').val()
    if(time != ""){
        day.closest('.times-container')[0].innerHTML += '<div class="timelabel" data-time="'+time+'">"'+time+'"<span class="close" onclick=removetime(this)>&times;</span><div/>'
    }

}

function removetime(elem){
    let time = $(elem)
    time.closest('.timelabel')[0].remove()
}


