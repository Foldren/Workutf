/*!
 * jQuery ClassyQR library
 * www.class.pm
 *
 * Written by Marius Stanciu - Sergiu <marius@class.pm>
 * Licensed under the MIT license www.class.pm/LICENSE-MIT
 * Version 1.2.0
 *
 */
 (function(c){c.fn.extend({ClassyQR:function(e){var a=c.extend({baseUrl:"http://chart.apis.google.com/chart?cht=qr&chs=",size:230,create:!1,number:null,email:null,subject:null,latitude:null,longitude:null,address:null,name:null,url:null,alt:"QR code",note:null,encoding:"UTF-8",type:"text",text:"Welcome to ClassPM"},e);return this.each(function(){var d=c(this),b=a.baseUrl+a.size+"x"+a.size+"&choe="+a.encoding+"&chl=";switch(a.type){case "contact":b=b+"MECARD:N:"+a.name+";TEL:"+a.number+";URL:"+a.url+ ";EMAIL:"+a.email+";ADR:"+a.address+";NOTE:"+a.note+";";break;case "wifi":b=b+"WIFI:S:"+a.ssid+";T:"+a.auth+";P:"+a.password+";";break;case "location":b=b+"geo:"+a.latitude+","+a.longitude;break;case "call":b=b+"tel:"+a.number;break;case "email":b=b+"mailto:"+a.email+":"+a.subject+":"+a.text;break;case "sms":b=b+"smsto:"+a.number+":"+a.text;break;case "url":b+=a.url;break;default:b+=a.text}a.create?d.append('<img src="'+b+'" alt="'+a.alt+'" />'):d.attr("src",b)})}})})(jQuery);