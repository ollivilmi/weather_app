$(function() {
	// Script for the slider

	var slider = document.getElementById("range");
	var output = document.getElementById("slidervalue");
	var selection = document.getElementById("loc");
	output.innerHTML = slider.value;
	
	slider.oninput = function() {
		output.innerHTML = this.value;
	}
});