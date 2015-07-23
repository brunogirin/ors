var timer_id;

function startTimer(interval){
    console.log("startTimer: interval: " + interval);
    return setInterval(getCache, interval);
}

function getCache(){
    console.log("getCache");
    $("#id-cache").slideUp(function(){
	var ajaxSettings = {
	    async: true,
	    complete: function(response){
		console.log("ajax ok");
		console.log(response);
		if(response.responseJSON.content != ""){
		    $("#id-cache").html(JSON.stringify(response.responseJSON.content));
		    $("#id-cache").slideDown();
		} else {
		    $("#id-cache").html("empty");
		    $("#id-cache").slideDown();
		}
	    }
	}
	$.ajax("/rev2-emulator/get-statuses", ajaxSettings);
    });
}

$(document).ready(function(){
    console.log("document.ready()");
    var responseSection = $("#id-response-section");
    var responseCode = responseSection.find("code");

    getCache();
    timer_id = startTimer(4000);

    $("#id-relative-humidity-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-relative-humidity-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "relative-humidity": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/relative-humidity", ajaxSettings);
    });

    $("#id-temperature-opentrv-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-temperature-opentrv-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "temperature-opentrv": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/temperature-opentrv", ajaxSettings);
    });

    $("#id-temperature-ds18b20-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-temperature-ds18b20-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "temperature-ds18b20": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/temperature-ds18b20", ajaxSettings);
    });

    $("#id-window-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-window-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "window": val},
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	    method: "post",
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/window", ajaxSettings);
    });

    $("#id-switch-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-switch-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "switch": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/switch", ajaxSettings);
    });

    $("#id-last-updated-all-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-last-updated-all-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "last-updated-all": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/last-updated-all", ajaxSettings);
    });


    $("#id-last-updated-temperature-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-last-updated-temperature-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "last-updated-temperature": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/last-updated-temperature", ajaxSettings);
    });

    $("#id-synchronising-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-synchronising-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "synchronising": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/synchronising", ajaxSettings);
    });

    $("#id-ambient-light-form").submit(function(e){
	e.preventDefault();
	var val = $("#id-ambient-light-input").val();
	var ajaxSettings = {
	    async: true,
	    data: {"house-code": $("#id-house-code-input").val(), "ambient-light": val},
	    method: "post",
	    complete: function(response){
		responseCode.html(JSON.stringify(response.responseJSON));
		responseCode.css("visibility", "visible");
		responseCode.slideDown();
	    },
	};
	responseCode.css("visibility", "hidden");
	responseCode.hide();
	responseCode.empty();
	$.ajax("/rev2-emulator/ambient-light", ajaxSettings);
    });

    // Get Cached Contents
    $("#id-get-cached-contents-interval-form").submit(function(e){
	e.preventDefault();
	var interval = $("#id-get-cached-contents-interval-input").val() * 1000;
	console.log("start-counter clicked: interval: " + interval);
	clearInterval(timer_id);
	if(interval != 0){
	    timer_id = startTimer(interval);
	}
    });
    

});
