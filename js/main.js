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
}
formatBoxes()

let interestsBtn = document.querySelector("#interests-btn")
interestsBtn.addEventListener("click", ()=> {
  window.location.href = "/AddInterest";
})
let favoritesBtn = document.querySelector("#favorites-btn")
favoritesBtn.addEventListener("click", ()=> {
  window.location.href = "/favorites";
})
