function boxWidth() {
  let x = screen.width
  let w = (x - 160)/8  + "px"
  let restaurants = document.querySelectorAll(".restaurant")
  for (restaurant of restaurants) {
    restaurant.style.width = w
    restaurant.style.height = w
  }
}
boxWidth()
// redirect to favorites page
favoritesBtn = document.querySelector("#favorites")
favoritesBtn.addEventListener('click', ()=> {
  window.location.href = "/favorites";
})
console.log("IN JAVASCRIPT MAIN")
