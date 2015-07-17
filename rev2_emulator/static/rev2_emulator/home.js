console.log("rev2_emulator: home.js");

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

	console.log(house_code_input);
	console.log(temperature_opentrv_input);
	console.log(temperature_opentrv_send_button);
	console.log(ds18b20_input);
	console.log(ds18b20_send_button);
	console.log(button_input);
	console.log(button_send_button);
	console.log(led_input);
	console.log(led_send_button);
	console.log(synchronising_input);
	console.log(synchronising_send_button);
	console.log(relative_humidity_input);
	console.log(relative_humidity_send_button);
	console.log(window_input);
	console.log(window_send_button);
	console.log(last_updated_input);
	console.log(last_updated_send_button);
	console.log(last_updated_temperatures_input);
	console.log(last_updated_temperatures_send_button);
	console.log(get_cached_contents_interval_input);
	console.log(get_cached_contents_interval_send_button);

	console.log(cache_output);
	cache_output.html("cheese");

	var i = 0;
	var interval = setInterval(function() {
		$.ajax("/rev2-emulator/get-statuses", {
			async: true,
			complete: function(response){
			    console.log("complete");
			    console.log(response);
			    console.log(response.responseJSON);
			    cache_output.html(JSON.stringify(response.responseJSON.content));
			},
		    });
	    }, 3000);

    });