console.log("home.html");

$(document).ready(function(){
	var statusSection = $("section#id-status-section");
	var statusForm = statusSection.find("form");
	console.log(statusSection);
	console.log(statusForm);

	statusForm.submit(function(e){
		var houseCodeInput = statusForm.find('input[type="text"]');
		this.setAttribute("action", "/api/status/" + houseCodeInput.val());
	    });
    });

