$(function() {
	// Script for the slider

	var slider = document.getElementById("days");
	var output = document.getElementById("slidervalue");
	var selection = document.getElementById("loc");
	output.innerHTML = slider.value;
	
	slider.oninput = function() {
		output.innerHTML = this.value;
	}
	
	selection.onchange = function() {
		slider.value = 1;
		output.innerHTML = 1;
	}
});