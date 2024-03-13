/* Magic Mirror Config 
 *
 * Magic Mirror CaravanPi
 * (c) Spitzlberger josef
 *
 */

var config = {
port: 8080,
address: "0.0.0.0",		// 0.0.0.0 = webserver is available within the network
				// ipWhitelist:
				//		first three entrys = from localhost
				//		specific IP addresses
				//		"::ffff:192.168.178.1/120" for all addresses 192.168.178.1 to 192.168.178.255
				//		192.168.178.x Wohnung
				//		192.168.168.x Caravan WLAN
ipWhitelist: [
		"127.0.0.1", 
		"::ffff:127.0.0.1", 
		"::1",
		"::ffff:192.168.178.1/120","192.168.178.1/24",
		"::ffff:192.168.168.1/120","192.168.168.1/24"
], 
language: "de",
timeFormat: 24,
units: "metric",

useHttps: false, 		// Support HTTPS or not, default "false" will use HTTP
httpsPrivateKey: "", 	// HTTPS private key path, only require when useHttps is true
httpsCertificate: "", 	// HTTPS Certificate path, only require when useHttps is true
	
modules: [

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
	module: "MMM-SimpleLogo",
	position: "top_center",
	config: {
		fileUrl: "modules/MMM-SimpleLogo/public/CaravanPi-Logo-weiss.png",
		width: "220px", 
		position: "center",
		text: "",
	}
},

/* **********************************************************
 *  nützliche Wettermodule
 * **********************************************************
 */
{
	module: "MMM-MarineWeather",
	position: "top_right",
	config: {
		latitude: 43.224591562827726, // Latitude 
		longitude: 3.247385126241382, // Longitude
		appid: "28de0ae6-f507-11eb-9edf-0242ac130002-28de0b5e-f507-11eb-9edf-xxxxxxxxxxxx" // StormGlass API key (docs.stormglass.io)
	}
},

{
	module: "MMM-Sunrise-Sunset",
	position: "top_right",
	config: {
		latitude: 43.224591562827726, // Latitude 
		longitude: 3.247385126241382, // Longitude
		apiKey: "b39e8a12da9a4355b1c3eaeexxxxxxxx",
		layout: "inline",
	}
},

{
	module: "weather",
	position: "top_right",
	header: "Wetteraussichten",
	config: {
		type: "forecast",
		roundTemp: true,
		colored: true,
		showPrecipitationAmount: true,
		fade: false,
		locationID: "6454040",  //ID from https://openweathermap.org/find
		apiKey: "777b12391a0929fddd40310xxxxxxxxx",
		maxNumberOfDays: 7,
	}
},

/* **********************************************************
 *  CaravanPi Module
 * **********************************************************
 */

// bevorzugt nicht mehr die MMM-CaravanPi-xxx einbinden, sondern Grafana Grafen 

/* -------------
{
	 module: 'MMM-GrafanaEmbedded',
		 position: 'top_right',   // This can be any of the regions.
		 config: {
				// http://192.168.178.139:3000/d/mef4p9ZVz/caravanpi-temperaturen?orgId=1&viewPanel=1
				id: "mef4p9ZVz", 
				host: "192.168.178.139", 
				port: 3000,
				dashboardName: "caravanpi-temperaturen",
				orgId: 1,
				panelId: 1,
				width: "450",
				height: "200",
				refreshRate: "5m",
				from: "now-36h",
				to: "now",
			}
},
--------------- */



/* -------------
{
	module: "MMM-CaravanPiClimate",
	position: "top_left",
	header: 'Klimawerte',
	config: {
		updateInterval: 60000,
		style: "boxlines",
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
--------------- */

/* -------------
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
--------------- */

/* -------------
{
	module: "MMM-CaravanPiGasWeight",
	position: "top_left",
	header: 'Füllstand Gasflasche',
	config: {
		updateInterval: 60000,
		style: "boxlines",
		weightPrecision: 0,
		sensors: [
				{
					name: "Alu 6kg Flasche 1",
					file: "gasScale1",
				},
				{
					name: "Alu 8kg Flasche 2",
					file: "gasScale2",
				},
			]
	}
},

--------------- */

/* -------------
{
	module: "MMM-CaravanPiPosition",
	position: "top_left",
	header: 'Lage Caravan',
	config: {
		updateInterval: 500,
		sensors: [
			{
				name: "Lagesensor",
				file: "position",
			},
		]
	}
},
--------------- */



/* **********************************************************
 *  weitere Module - Vorschläge
 * **********************************************************
 */
	
/* -------------
{
	module: 'MMM-DWD-WarnWeather',
	position: 'top_right',
	header: 'Wetterwarnungen xxxx',
	config: {
		displayInnerHeader: false,
		displayRegionName: false,
		region: 'xxxx',
		changeColor: true,
		minutes: false,
		interval: 10 * 60 * 1000, // every 10 minutes
		loadingText: 'Warnungen werden geladen...',
		noWarningText: 'Keine Warnungen',
		severityThreshold: 2,
	}
},
--------------- */

/* -------------
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
--------------- */

/* -------------
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
--------------- */


/* **********************************************************
 *  Remote Control Modul
 * **********************************************************
 */
	
{
	module: 'MMM-Remote-Control',
	// uncomment the following line to show the URL of the remote control on the mirror
	position: 'bottom_right'
},

] /* modules */

};

/*************** DO NOT EDIT THE LINE BELOW ***************/
if (typeof module !== "undefined") {module.exports = config;}
