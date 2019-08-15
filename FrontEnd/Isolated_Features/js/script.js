if (document.readyState == "loading")
	document.addEventListener("DOMContentLoaded", ready);
else ready();
// =================================================================
// 			Above Code Ensures that the JS isn't executed
// 			In case the HTML hasn't been loaded as we are
// 			Using async
// =================================================================

let chips = [];

function ready() {
	const endpoint = "../../data/chips.json";
	// const endpoint = "res/people.json";   // (Path Relative to html files sourcing this script)
	fetch(endpoint)
	    .then(response => response.json())
	    .then(function(data) {
	        chips.push(...data);
	        main();
	    })
	    .catch(err => console.log(err));

}

function main() {
    renderData(chips)
}

function renderData(data) {
  var mainContainer = document.getElementById("myData");
  for (var i = 0; i < data.length; i++) {
    var div = document.createElement("div");
    div.innerHTML = `
        <span>${data[i].source}</span>
        <a href="${data[i].url}">${data[i].name}</a>
    `;
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
