  
  
  let autocomplete;

  function initMap() {
    autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('places_search_field'),
      {
          types: ['administrative_area_level_1', 'administrative_area_level_2', 'locality', 'sublocality'],
          componentRestrictions : {country: ['ZA', 'ZM', 'ZW', 'BW', 'NA']},
          fields: ['place_id', 'name', 'types'],
      }
    );
    autocomplete.addListener('place_changed', onPlaceChange);
  }

  function onPlaceChange(){
    document.getElementById('placeid').value = autocomplete.getPlace().place_id
  }


//  function onPlaceChange(elem) {  
//     document.getElementById('placeid').value = autocomplete.getPlace().place_id

//     let place_id = autocomplete.getPlace().place_id

    // var xhr = new XMLHttpRequest();
    // xhr.open("GET", `https://maps.googleapis.com/maps/api/place/details/json?place_id=${place_id}&key=AIzaSyBA4UiuR4j_5veSQb6hjx-k4izHptNOqdE`);
    // // xhr.setRequestHeader('Accept','application/json');
    // // xhr.setRequestHeader('Content-type','application/json');
    // xhr.setRequestHeader('Access-Control-Allow-Origin:','*');
    // xhr.onreadystatechange = function(){
    //   if(xhr.readyState === 4){
    //     if(xhr.status === 200){
    //       var response = JSON.parse(xhr.responseText);
    //       console.log(response);              
    //     }
    //     else{
    //       alert("not response from google.");
    //     }
    //   }
    // };
    // xhr.send();
  // }