
  let autocomplete;

  function initAutocomplete() {
    autocomplete = new google.maps.places.Autocomplete(
      document.getElementById('places_search_field'),
      {
        types: ['geocode', 'regions', 'cities'],
        componentRestrictions : ['ZA', 'ZM', 'ZW', 'BW', 'NA'],
        fields: ['place_id', 'name', 'types'],
      }
    )
    autocomplete.addListener('place_changed', onPlaceChange)
  }

  function onPlaceChange(){
    console.log("place changed")
  }