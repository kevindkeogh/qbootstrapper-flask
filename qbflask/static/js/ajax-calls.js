$(document).ready(function () {
    "use strict";
    var instsForm = $("#instruments-form");
    var submitForm = $("#instruments-submit");

    $(instsForm).submit(function (e) {
        e.preventDefault();
		var instsData = $(instsForm).serializeArray();
		$.ajax({
			type: "POST",
			url: "/curve",
			data: JSON.stringify(instsData),
			contentType: "application/json;charst=UTF-8",
			success: function(result) {
				console.log(result);
			}});
		return false;
    });
});
