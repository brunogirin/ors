console.log("home.html");

$(document).ready(function(){
	var statusSection = $("section#id-status-section");
	var statusForm = statusSection.find("form");

	statusForm.submit(function(e){
		var houseCodeInput = statusForm.find('input[type="text"]');
		this.setAttribute("action", "/api/status/" + houseCodeInput.val());
	    });

	var ledSection = $("section#id-led-section");
	var ledForm = ledSection.find("form");
	ledForm.submit(function(e){
		var houseCodeInput = ledForm.find("input#id-house-code-input");
		this.setAttribute("action", "/api/led/" + houseCodeInput.val());
	    });

	var valveSection = $("section#id-valve-section");
	var valveForm = valveSection.find("form");
	valveForm.submit(function(e){
		var houseCodeInput = valveForm.find("input#id-house-code-input");
		this.setAttribute("action", "/api/valve/" + houseCodeInput.val());
	    });

	
    });

