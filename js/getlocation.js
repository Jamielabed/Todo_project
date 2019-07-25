function getClientLocation(url = "https://www.googleapis.com/geolocation/v1/geolocate?key="+GOOGLE_API_KEY, data = {}) {
  fetch(url, {
    method: "POST",
    mode: "cors",
    cache: "no-cache",
    credentials: "same-origin",
    headers: {
      'Content-Type': 'application/json',
    },
    redirect: 'follow',
    referrer: 'no-referrer',
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(function (myJson){
    let latitude = myJson.location.lat
    let longitude = myJson.location.lng

    console.log(myJson)
    //sendLocationToServer(latitude,longitude)
    window.location.href = `/?lat=${latitude}&long=${longitude}`
  })
}
function sendLocationToServer(lat,long) {
  fetch('/location?lat='+lat+'&long='+long)
  .then(response => response.text())
  .then(function (myText) {
    document.querySelector('#restaurants_info').innerHTML = myText
    formatBoxes()

  })
  // .then(response => response.json())
  // .then(function (myJson){
  //   console.log(myJson)
  //
  // })
}


  //redirect to favorites page
  // favoritesBtn = document.querySelector("#favorites")
  // favoritesBtn.addEventListener('click', ()=> {
  //   window.location.href = "/favorites";
  //     window.location.href = "/AddInterest";
  //  })
  // console.log("IN JAVASCRIPT MAIN")

// console.log("IN JAVASCRIPT LOCATION")
// console.log(getClientLocation())
// let clientLocation = getClientLocation()
// console.log(typeof clientLocation)
// console.log(clientLocation.location)

getClientLocation()
