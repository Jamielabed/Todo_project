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

  // redirect to favorites page
  favoritesBtn = document.querySelector("#favorites")
  favoritesBtn.addEventListener('click', ()=> {
    window.location.href = "/favorites";
  })
  console.log("IN JAVASCRIPT MAIN")
}

formatBoxes()

function includeSortBy(lat,long) {
  let sortChoice = document.querySelector('#sort_selection')
  window.location.href = `/?lat=${latitude}&long=${longitude}&sort_selection=${sortChoice}`

}
