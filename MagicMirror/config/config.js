/* Magic Mirror Config 
 *
 * Magic Mirror Bad Schloss Lustheim 1
 * (c) Spitzlberger josef
 *
 */

var config = {
port: 8080,
address: "0.0.0.0",
// ipWhitelist: ["127.0.0.1", "::ffff:127.0.0.1", "::1","192.168.178.61","192.168.178.144","192.168.178.101","192.168.178.138","192.168.178.160"], 
ipWhitelist: [], 
language: "de",
timeFormat: 24,
units: "metric",

modules: [

{
	module: 'MMM-Remote-Control',
	// uncomment the following line to show the URL of the remote control on the mirror
	// , position: 'top_bar'
	//
	// Menü für CaravanPi
	customMenu: "CaravanPi_menu.json",
},
/*
{
	module: 'MMM-Logging',
	config: {
	}
},
*/

{
	module: 'MMM-PIR-Sensor',
	config: {
		sensorPin: 25,
		sensorState: 1,
		powerSaving: 1,
		powerSavingDelay: 60, // 60 Sekunden bis power off
		powerSavingNotification: true,
		powerSavingMessage: "Bildschirm wird ausgeschaltet",
	}
},

{
	module: "alert",
},
{
	module: "updatenotification",
	position: "top_bar",
},
{
	module: "clock",
	position: "top_left",
	showWeek: "true",
},


{
	module: "MMM-CaravanPiClimate",
	position: "top_left",
	header: 'Klimawerte',
	config: {
		updateInterval: 60000,
		style: "boxes",
		tempPrecision: 0,
		humPrecision: 0,
		pressPrecision: 0,
		sensors: [
			{
				name: "Innen",
				file: "BME280-96-118",
			},
			{
				name: "Außen",
				file: "BME280-96-119",
			},
		]
	}
},

{
	module: "MMM-CaravanPiTemperature",
	position: "top_left",
	header: 'Kühlschrank Temperaturen',
	config: {
		updateInterval: 60000,
		style: "boxes",
		tempPrecision: 0,
		sensors: [
			{
				name: "Gefrierfach",
				file: "28-01144f936caa",
			},
			{
				name: "Kühlschrank",
				file: "28-01144fea82aa",
			},
			{
				name: "Getränkefach",
				file: "28-01144febdbaa",
			},
		]
	}
},

{
	module: "MMM-CaravanPiGasWeight",
	position: "top_left",
	header: 'Füllstand Gasflasche',
	config: {
		updateInterval: 60000,
		style: "boxes",
		weightPrecision: 0,
		sensors: [
			{
				name: "Alu 6kg Flasche",
				file: "gasScale",
			},
		]
	}
},

{
	module: "MMM-CaravanPiPosition",
	position: "top_right",
	header: 'Lage Caravan',
	config: {
		updateInterval: 500,
		style: "boxes",
		sensors: [
			{
				name: "Lagesensor",
				file: "position",
			},
		]
	}
},



{
	module: "currentweather",
	position: "top_right",
	config: {
		location: "Oberschleißheim",
		locationID: "2859147",  //ID from http://www.openweathermap.org/help/city_list.txt
		appid: "92d386a20fe1111220b40687a49bddc1",
		roundTemp: "true",
		showWindDirection: "true",
		showWindDirectionAsArrow: "true",
		showFeelsLike: false,
	}
},

{
	module: "weatherforecast",
	position: "top_right",
	header: "Weather Forecast",
	config: {
		location: "Oberschleißheim",
		locationID: "2859147",  //ID from http://www.openweathermap.org/help/city_list.txt
		appid: "92d386a20fe1111220b40687a49bddc1",
		roundTemp: true,
		showRainAmount: true,
		fade: false,
	}
},


{
	module: 'MMM-DWD-WarnWeather',
	position: 'top_right',
	header: 'Wetterwarnungen Oberschleißheim',
	config: {
		displayInnerHeader: false,
		displayRegionName: false,
		region: 'Oberschleißheim',
		changeColor: true,
		minutes: false,
		interval: 10 * 60 * 1000, // every 10 minutes
		loadingText: 'Warnungen werden geladen...',
		noWarningText: 'Keine Warnungen',
		severityThreshold: 2,
	}
},



{
	module: "newsfeed",
	position: "top_right",	// This can be any of the regions. Best results in center regions.
	header: 'aktuelle Nachrichten',
	config: {
		showDescription: true,
		showPublishDate: true,
		truncDescription: true,
		lengthDescription: 300,
		updateInterval: 20000,
		ignoreOldItems: true,
		feeds: [
			{
				title: "BR24 Oberbayern",
				url: "https://nachrichtenfeeds.br.de/rdf/boards/QXAQcxl",
			},
			{
				title: "BR Nachrichten",
				url: "https://www.br.de/nachrichten/meldungen/nachrichten-bayerischer-rundfunk100~newsRss.xml",
			},
		]
	}
},


{
	module: 'MMM-SystemStats',
	position: 'bottom_bar',
	classes: 'xsmall dimmed', 
	config: {
		label: 'textAndIcon',
		updateInterval: 300000, // every 5 minutes
		align: 'left', // align labels
		singleRow: true,
	}
},


] /* modules */

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
