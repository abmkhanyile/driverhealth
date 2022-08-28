  
  
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

    let place_id = autocomplete.getPlace().place_id

    // var axios = require('axios');

    var config = {
      method: 'get',
      url: `https://maps.googleapis.com/maps/api/place/details/json?place_id=${place_id}&key=AIzaSyBA4UiuR4j_5veSQb6hjx-k4izHptNOqdE`,
      headers: {
        Accept: 'application.json',
        'Content-Type': 'application/json'
      }
    };

    axios(config)
    .then(function (response) {
      console.log(JSON.stringify(response.data));
    })
    .catch(function (error) {
      console.log(error);
    });

    // fetch(`https://maps.googleapis.com/maps/api/place/details/json?place_id=${place_id}&key=AIzaSyBA4UiuR4j_5veSQb6hjx-k4izHptNOqdE`)
    // .then(response => {
    //   //handle response            
    //   console.log(response);
    // })
    // .then(data => {
    //   //handle data
    //   console.log(data);
    // })
    // .catch(error => {
    //   //handle error
    // });

  }