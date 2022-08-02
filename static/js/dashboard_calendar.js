function selectday(elem){
    let day = $(elem)
    if(day.attr("data-dayselected") == "0"){
        day.css("background-color", "green")
        day.attr("data-dayselected", "1")
    }else{
        day.css("background-color", "white")
        day.attr("data-dayselected", "0")
    }
    
}

function compile_dates(){
    // compilation goes here
    let dates_arr = []
    $('.calendar-day').each( function(index){
        if($(this).attr("data-dayselected") == "1"){
            dates_arr.push($(this).attr('data-day'))
        }
        $('#dates_input').val(dates_arr)
        
       
    });
    return true
}


