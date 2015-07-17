console.log("rev2_emulator: home.js");

var test;
var pageVisited = new Date();		

function displayStatuses(){
    $("code").slideUp(function(){
	    var ajaxSettings = {
		async: true,
		complete: function(response){
		    console.log("ajax ok");
		    $("code").html(JSON.stringify(response.responseJSON));
		    $("code").slideDown();
		}
	    }
	    $.ajax("/rev2-emulator/get-statuses", ajaxSettings);
	});
}

function startTimer(interval){
    console.log("startTimer: interval: " + interval);
    return setInterval(displayStatuses, interval);
}

// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

var csrftoken = getCookie('csrftoken');
console.log(csrftoken);

$.ajaxSetup({
	beforeSend: function(xhr, settings) {
	    if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
		// Send the token to same-origin, relative URLs only.
		// Send the token only if the method warrants CSRF protection
		// Using the CSRFToken value acquired earlier
		xhr.setRequestHeader("X-CSRFToken", csrftoken);
	    }
	}
    });

$(document).ready(function(){

	console.log("document ready!");

	var house_code_input = $("#id-house-code-input");
	var temperature_opentrv_input = $("#id-room-temp-input");
	var temperature_opentrv_send_button = $("#id-room-temp-send-button");
	var ds18b20_input = $("#id-ds18b20-temp-input");
	var ds18b20_send_button = $("#id-ds18b20-temp-send-button");
	var button_input = $("#id-button-input");
	var button_send_button = $("#id-button-send-button");
	var led_input = $("#id-led-input");
	var led_send_button = $("#id-led-send-button");
	var synchronising_input = $("#id-synchronising-input");
	var synchronising_send_button = $("#id-synchronising-send-button");
	var relative_humidity_input = $("#id-relative-humidity-input");
	var relative_humidity_send_button = $("#id-relative-humidity-send-button");
	var window_input = $("#id-window-input");
	var window_send_button = $("#id-window-send-button");
	var last_updated_input = $("#id-last-updated-input");
	var last_updated_send_button = $("#id-last-updated-send-button");
	var last_updated_temperatures_input = $("#id-last-updated-temperatures-input");
	var last_updated_temperatures_send_button = $("#id-last-updated-temperatures-send-button");
	var get_cached_contents_interval_input = $("#id-get-cached-contents-interval-input");
	var get_cached_contents_interval_send_button = $("#id-get-cached-contents-interval-send-button");
	var cache_output = $("code");

	displayStatuses();
	test = startTimer(4000);

	// show cache now
	$("#id-show-cache-now").click(function(event){
		get_cached_contents_interval_input.val("0");
		get_cached_contents_interval_send_button.click();
	    });

	// last_updated_temperatures
	last_updated_temperatures_send_button.on("click", function(event){
		var value = last_updated_temperatures_input.val();
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "last-updated-temperatures": value},
		    method: "post",
		};
		$.ajax("/rev2-emulator/last-updated-temperatures", ajaxSettings);
	    });

	// last_updated
	last_updated_send_button.on("click", function(event){
		var value = last_updated_input.val();
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "last-updated": value},
		    method: "post",
		};
		$.ajax("/rev2-emulator/last-updated", ajaxSettings);
	    });

	// window
	window_send_button.on("click", function(event){
		var value = window_input.prop("checked") ? "open" : "closed";
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "window": value},
		    method: "post",
		};
		$.ajax("/rev2-emulator/window", ajaxSettings);
	    });

	// relative_humidity
	relative_humidity_send_button.on("click", function(event){
		var value = relative_humidity_input.val();
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "relative-humidity": value},
		    method: "post",
		};
		$.ajax("/rev2-emulator/relative-humidity", ajaxSettings);
	    });

	// synchronising
	synchronising_send_button.on("click", function(event){
		var value = synchronising_input.prop("checked") ? "on" : "off";
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "synchronising": value},
		    method: "post",
		};
		$.ajax("/rev2-emulator/synchronising", ajaxSettings);
	    });

	// led
	led_send_button.on("click", function(event){
		var value = led_input.val();
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "led": value},
		    method: "post",
		};
		$.ajax("/rev2-emulator/led", ajaxSettings);
	    });

	// button
	button_send_button.on("click", function(event){
		var state = button_input.prop("checked") ? "on" : "off";
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "button": state},
		    method: "post",
		};
		$.ajax("/rev2-emulator/button", ajaxSettings);
	    });

	// DS18B20 Temp
	ds18b20_send_button.on("click", function(event){
		var temp = ds18b20_input.val();
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "ds18b20-temp": temp},
		    method: "post",
		};
		$.ajax("/rev2-emulator/ds18b20-temperature", ajaxSettings);
	    });

	// Room Temp
	temperature_opentrv_send_button.on("click", function(event){
		var temp = temperature_opentrv_input.val();
		var ajaxSettings = {
		    async: true,
		    data: {"house-code": house_code_input.val(), "room-temp": temp},
		    method: "post",
		};
		$.ajax("/rev2-emulator/temperature-opentrv", ajaxSettings);
	    });

	// Get Cached Contents
	get_cached_contents_interval_send_button.on("click", function(event){
		event.preventDefault();
		var interval = $("#id-get-cached-contents-interval-input").val() * 1000;
		console.log("start-counter clicked: interval: " + interval);
		clearInterval(test);
		if(interval != 0){
		    test = startTimer(interval);
		}
	    });

	
    });


// $(document).ready(function(){


// 	$("#id-get-cached-contents-interval-input").click(function(e){
// 		testClear();
// 	    });

// //  	get_cached_contents_interval_send_button.on("click", function(e){
// //  		console.log("clearing interval: " + test);
// //  		testClear();
// //  	    });

//     });



// 	console.log(house_code_input);
// 	console.log(temperature_opentrv_input);
// 	console.log(temperature_opentrv_send_button);
// 	console.log(ds18b20_input);
// 	console.log(ds18b20_send_button);
// 	console.log(button_input);
// 	console.log(button_send_button);
// 	console.log(led_input);
// 	console.log(led_send_button);
// 	console.log(synchronising_input);
// 	console.log(synchronising_send_button);
// 	console.log(relative_humidity_input);
// 	console.log(relative_humidity_send_button);
// 	console.log(window_input);
// 	console.log(window_send_button);
// 	console.log(last_updated_input);
// 	console.log(last_updated_send_button);
// 	console.log(last_updated_temperatures_input);
// 	console.log(last_updated_temperatures_send_button);
// 	console.log(get_cached_contents_interval_input);
// 	console.log(get_cached_contents_interval_send_button);

	
// // 	var i = 0;
// // 	var interval = setInterval(function() {
// // 		$.ajax("/rev2-emulator/get-statuses", {
// // 			async: true,
// // 			complete: function(response){
// // 			    console.log("complete");
// // 			    console.log(response);
// // 			    console.log(response.responseJSON);
// // 			    cache_output.html(JSON.stringify(response.responseJSON.content));
// // 			},
// // 		    });
// // 	    }, 10000);

// 	var interval = 1000;
// 	function callback() {
// 	    console.log( 'callback!' );
// 	    return setTimeout( callback, interval );
// 	}

// 	timeout = callback();

// 	get_cached_contents_interval_send_button.on("click", function(e){
// 		clearTimeout(timeout);
// 	    });
	
// 	var previous_timeout = undefined;

// 	get_cached_contents_interval_send_button.click(function(e){
// 		interval = get_cached_contents_interval_input.val();
// 		if(interval == 0){
// 		    interval = 100000;
// 		}
// 		interval = interval * 1000;
// 		console.log(interval);
// 		console.log("previous_timeout: " + previous_timeout);
// 		console.log("cleanInterval: " + clearInterval(previous_timeout));
// 		previous_timeout = callback(interval);
// 		console.log("new_timeout: " + previous_timeout);
// 	    });

// 	var interval = 1000;
	
// 	function callback() {
// 	    console.log( 'callback!' );
// 	    interval -= 100; // actually this will kill your browser when goes to 0, but shows the idea
// 	    setTimeout( callback, interval );
// 	}
	
// 	setTimeout( callback, interval );
//     });