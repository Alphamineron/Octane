if (document.readyState == "loading")
	document.addEventListener("DOMContentLoaded", cardRenderReady);
else cardRenderReady();
// =================================================================
// 			Above Code Ensures that the JS isn't executed
// 			In case the HTML hasn't been loaded as we are
// 			Using async
// =================================================================

let chips = [];

function cardRenderReady() {
	const endpoint = "../../data/chips.json";
	// const endpoint = "res/people.json";   // (Path Relative to html files sourcing this script)
	fetch(endpoint)
	    .then(response => response.json())
	    .then(function(data) {
	        chips.push(...data);
	        cardRenderMain();
	    })
	    .catch(err => console.log(err));

}

function cardRenderMain() {
    renderData(chips)
    addEventListenerToCards()
}

function renderData(data) {
    var mainContainer = document.getElementById("myData");

	if(data.length > 50) var n_cards = 50;
	else var n_cards = data.length;

    for (var i = 0; i < n_cards; i++) {
        var div = document.createElement("div");
        div.innerHTML = `
    <div class="card-wrapper" id="${data[i].ID}">

    	<div class="card--date">${data[i].folders}</div>
    	<div class="card--details">

    		<div class="card--details-left">

    			<div class="card--title" contenteditable="true"><a href="${data[i].url}">${data[i].name}</a></div>
    			<div class="card--attribute-wrapper show-on-mobile">
    				<div class="card--attribute card--attribute-1">
                        <span>Starred</span>
                        <span>${data[i].starred}</span>
    				</div>

    				<span class="divider">•</span>

    				<div class="card--attribute card--attribute-2">
    					<span class="c-n700 heavy">AUD</span>
    					<span>99.00</span>
    				</div>
    			</div>

    		</div>
    		<div class="card--details-right">

    			<div class="card--attribute-wrapper hide-on-mobile">

    				<div class="card--attribute card--attribute-1">
    					<span>Starred</span>
    					<span>${data[i].starred}</span>
    				</div>
                    <img class="card--attribute card--attribute-image" src="res/image_placeholder.png"/>

    			</div>
    			<div class="card--icon card--menu-wrapper">

    				<button class="card--menu-button">
    					<i class="fa fa-ellipsis-v"></i>
    				</button>
    				<div class="card--menu-dropdown-wrapper" role="menu">
    					<ul class="card-menu">
    						<li class="card-menu--item" role="menuitem">
    							<a class="link link--edit" href="#">Menu1</a>
    						</li>
    						<li class="card-menu--item" role="menuitem">
    							<a class="link link--delete" href="#">Menu2</a>
    						</li>
    					</ul>
    				</div>

    			</div>
    			<div class="card--icon card--chevron hide-on-mobile">
    				<i class="fa fa-chevron-down"></i>
    			</div>

    		</div>

    	</div>
    	<span class="card--brick brick-primary">AWS Certification</span>
    	<div class="card--custom-field-wrapper" id="custom-field">

    		<div class="custom-field--row">

    			<div class="custom-field--label">Description</div>
    			<div class="custom-field--value">${data[i].description}</div>

    		</div>
            <div class="custom-field--row">

                <div class="custom-field--label">Kind</div>
                <div class="custom-field--value">${data[i].kind}</div>

            </div>
            <div class="custom-field--row">

                <div class="custom-field--label">UseCases</div>
                <div class="custom-field--value">${data[i].useCases}</div>

            </div>
            <div class="custom-field--row">

                <div class="custom-field--label">Topics</div>
                <div class="custom-field--value">${data[i].topics}</div>

            </div>
            <div class="custom-field--row">

                <div class="custom-field--label">Tags</div>
                <div class="custom-field--value">${data[i].tags}</div>

            </div>
    		<div class="custom-field--row">

                <div class="custom-field--label">Source</div>
                <div class="custom-field--value">${data[i].source}</div>

    		</div>
            <div class="custom-field--row">

                <div class="custom-field--label">URL</div>
                <div class="custom-field--value"><a href="${data[i].url}">${data[i].url}</a></div>

            </div>

    	</div>

    </div>
    `;
        // div.innerHTML = `
        //     <span>${data[i].source}</span>
        //     <a href="${data[i].url}">${data[i].name}</a>
        // `;
        // div.innerHTML = `
        //     ${data[i].firstName} ${data[i].lastName}
        // `
        mainContainer.appendChild(div);
  }
}








































































// fetch('people.json')
//   .then(function (response) {
//     return response.json();
//   })
//   .then(function (data) {
//     appendData(data);
//   })
//   .catch(function (err) {
//     console.log(err);
//   });
//
// function appendData(data) {
//   var mainContainer = document.getElementById("myData");
//   for (var i = 0; i < data.length; i++) {
//     var div = document.createElement("div");
//     div.innerHTML = `Name: ${data[i].firstName} ${data[i].lastName}`;
//     mainContainer.appendChild(div);
//   }
// }
