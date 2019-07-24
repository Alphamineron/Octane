// import {lunr} from 'node_modules/lunr/lunr.js';   // Requires Babel

if (document.readyState == "loading")
	document.addEventListener("DOMContentLoaded", ready);
else ready();
// =================================================================
// 			Above Code Ensures that the JS isn't executed
// 			In case the HTML hasn't been loaded as we are
// 			Using async
// =================================================================

let chips = [];
let recentSearches = [];
let idx;
let fuse;

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
    // buildIndex()
    build_fuseOptions()
	// Sticking Event Listeners
	const searchInput = document.querySelector('.search-input');
	searchInput.addEventListener("keyup", (event) => {   // if enter/return is pressed
														if (event.keyCode === 13)
															handleSearch(event);
													});
	const searchIcon = document.querySelector('.search svg');
	searchIcon.addEventListener("click", handleSearch);
}

// ===============================< Search >====================================

function getSearchQuery() {
	return document.querySelector('.search-input').value;
}

function updateSearchHistory() {
	const searchInput = document.querySelector('.search-input');
	// searchInput.value = "";			// Clear the searchbar after search
	const searchHistory = document.querySelector('.search-history');
	searchHistory.value = "";	// Clear the search history

	// Loop the recentSearches and add to History
	recentSearches.forEach(function(index, value) {
								var li = document.createElement("li");
								li.setAttribute("class", "history-item");
								li.addEventListener("click", (event) => {
																			searchInput.value = recentSearches[index];
																		});
								li.innerText = value;
								searchHistory.appendChild(li);
							});
}

function renderSearchResults(resultChips) {
	var mainContainer = document.getElementsByClassName("search-results")[0];
	for (var i = 0; i < resultChips.length; i++) {
		var div = document.createElement("div");  // Create HTML element to display a data item
		div.innerHTML = `
		  <!-- <span>${resultChips[i].source}</span> -->
		  <a href="${resultChips[i].url}">${resultChips[i].name}</a>
		`;
		mainContainer.appendChild(div);  // Append each data item one after another
	}
}

function handleSearch(event) {
    // lunrSearch();
    fuseSearch();
}

// ===============================< Libraries >=================================

function build_lunrIndex() {
	idx = lunr(function () {
					this.ref('ID');
					this.field('name', { boost: 10 });
					this.field('url');

					chips.forEach(function (doc) { this.add(doc) }, this);
				});
}

function lunrSearch() {
	const searchInput = document.querySelector('.search-input');
	const query = searchInput.value;	// Fetch the Search Query

	recentSearches.push(query);		// Store the recent query
	document.getElementsByClassName("search-results")[0].innerHTML = '';  // Clear Previous Search Results


	var results = idx.search(query);	// Perform Search Operation on index
	var resultChips = [];
	results.forEach(function(result) {	 // Fetch complete info on Search Results
								chips.forEach(function(chip) {
															if (chip["ID"] == result["ref"]) {
																resultChips.push(chip);
															}
														});
							});


	renderSearchResults(resultChips);
    console.log("query:", query, results.length);
	// alert(resultChips);
}

function build_fuseOptions() {
    var options = {
                shouldSort: true,
                tokenize: true,
                // includeScore: true,
                keys: [{
                    name: 'url',
                    weight: 0.1
                }, {
                    name: 'name',
                    weight: 0.9
                }]
    };
    fuse = new Fuse(chips, options)
}

function fuseSearch() {
    const searchInput = document.querySelector('.search-input');
    const query = searchInput.value;	// Fetch the Search Query
    document.getElementsByClassName("search-results")[0].innerHTML = '';  // Clear Previous Search Results

    var result = fuse.search(query)

    renderSearchResults(result);
    console.log("query:", query, result.length);
}
