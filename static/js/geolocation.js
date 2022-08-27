  
  
  let autocomplete;

  function initMap() {
    autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('places_search_field'),
      {
        types: ['locality', 'sublocality', 'administrative_area_level_1'],
        componentRestrictions : {country: ['ZA', 'ZM', 'ZW', 'BW', 'NA']},
        fields: ['place_id', 'name', 'types'],
      }
    );
    autocomplete.addListener('place_changed', onPlaceChange);
  }

  function onPlaceChange(){
    console.log(autocomplete.getPlace())

  }