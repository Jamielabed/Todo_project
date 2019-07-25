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
    sendLocationToServer(latitude,longitude)

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

function formatBoxes() {
  function boxWidth() {
    let x = screen.width
    let w = (x - 160)/6
    let wpx = (x - 160)/6  + "px"
    let total_width = 0
    let restaurants = document.querySelectorAll(".restaurant")
    for (restaurant of restaurants) {
      console.log(restaurant.innerHTML)
      restaurant.style.width = wpx
      restaurant.style.height = wpx
      total_width += (w+20)
    }
    console.log("TOTAL WIDTH: " + total_width)
    console.log("SCREEN WIDTH: " + screen.width)
  }
  boxWidth()

  redirect to favorites page
  favoritesBtn = document.querySelector("#favorites")
  favoritesBtn.addEventListener('click', ()=> {
    window.location.href = "/favorites";
      window.location.href = "/AddInterest";
   })
  console.log("IN JAVASCRIPT MAIN")
}
// console.log("IN JAVASCRIPT LOCATION")
// console.log(getClientLocation())
// let clientLocation = getClientLocation()
// console.log(typeof clientLocation)
// console.log(clientLocation.location)
getClientLocation()
