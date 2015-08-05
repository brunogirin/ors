console.log("home.html");

$(document).ready(function(){

    var debugSection = $("section#id-debug-section");
    var debugForm = debugSection.find("form");
    debugForm.submit(function(e){
	var houseCodeInput = debugForm.find('#id-house-code-input');
	this.setAttribute('action', '/api/debug/' + houseCodeInput.val());
    });

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

    // Experimenting with passing json in the request for the post house codes api call
    // var postHouseCodesSection = $("section#id-post-house-codes-section");
    // var postHouseCodesForm = postHouseCodesSection.find("form");
    // postHouseCodesForm.submit(function(e){
    // 	e.preventDefault();
    // 	var houseCodesStr = postHouseCodesForm.find("#id-house-codes-input").val();
    // 	console.log("houseCodesStr: " + houseCodesStr);
    // 	var houseCodes = houseCodesStr.split(',');
    // 	console.log("houseCodes: " + houseCodes);
    // 	console.log(houseCodes.length);
    // 	document.body = houseCodes;
    // });
    
});

