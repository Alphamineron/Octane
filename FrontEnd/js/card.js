
function addEventListenerToCards() {
    var card      = document.querySelectorAll(".card-wrapper");
    var cardMenu  = document.querySelectorAll(".card--menu-wrapper");
    var toggleAll = document.querySelector(".toggle-all");

    if (cardMenu) {
      cardMenu.forEach(function(el){
        var cardMenuDropdown = el.querySelector(".card--menu-dropdown-wrapper");

        el.addEventListener("click", function (e) {
          e.stopPropagation();
          e.preventDefault();

          if (cardMenuDropdown.classList.contains("card--menu-dropdown-wrapper-entered")) {
            cardMenuDropdown.classList.remove("card--menu-dropdown-wrapper-entered");
          } else {
            cardMenuDropdown.classList.add("card--menu-dropdown-wrapper-entered");
          }
        });
      });
    }

    if (card) {
      card.forEach(function(el){
        var cardCF = el.querySelector(".card--custom-field-wrapper");
         el.addEventListener("click", function () {
            if (el.classList.contains("card--is-expanded")) {
              el.classList.remove("card--is-expanded");
              cardCF.classList.add("card--animate-out");
              cardCF.classList.remove("card--animate-in");
            } else {
              el.classList.add("card--is-expanded");
              cardCF.classList.add("card--animate-in");
              cardCF.classList.remove("card--animate-out");
            }
         });
      });
    }

    // var toggleState = false;
    //
    // toggleAll.addEventListener("click", function(e) {
    //   toggleState = !toggleState;
    //
    //   if (toggleState) {
    //     toggleAll.innerHTML = "Collapse All"
    //     card.forEach(function(el) {
    //       el.classList.add("card--is-expanded");
    //     });
    //   } else {
    //     toggleAll.innerHTML = "Expand All"
    //     card.forEach(function(el) {
    //       el.classList.remove("card--is-expanded");
    //     });
    //   }
    // })

}
