// Select the form
var titleForm = d3.select("#title-search");

// Select the title input field
var titleText = d3.select("#input-title")

// Update form action when input title text changes

titleText.on("change", function(){
	console.log(titleText.node().value)
    
	titleForm.attr("action", function(){
    	return "/title/" + titleText.node().value;
    })

});

