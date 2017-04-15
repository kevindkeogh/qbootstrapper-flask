function displayDFs(results) {
	"use strict";
	var i;
	var date;
	var df;
	var outputTable = $("#output-table");
	$(outputTable).empty(); // Remove all child elements
	// in case this is not the first run
	var headerRow = $("<thead><tr><th>Dates</th>" +
			"<th>Discount Factors</th></tr></thead>");
	$(headerRow).appendTo(outputTable);

	var numRows = results.dates.length;
	for (i=0; i<numRows; i++) {
		date = results.dates[i];
		df = results.dfs[i].toString().substring(0, 12);
		outputTable.append("<tr><td class=\"date\">" + date + "</td>" +
				"<td class=\"discount-factor\">" + df + "</td></tr>");
	}
}

function displayBootstrapError(text) {
	"use strict";
	var outputTable = $("#output-table");
	$(outputTable).empty();
	outputTable.append("<p class=\"ajax-error\">" + text + "</p>");
}

$(document).ready(function () {
	"use strict";
	var instsForm = $("#instruments-form");
	var csrfToken = $("#csrf-token")[0].value;

	$.ajaxSetup({
		beforeSend: function(xhr, settings) {
						if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
							xhr.setRequestHeader("X-CSRFToken", csrfToken);
						}
					}
	});


	$(instsForm).submit(function (e) {
		e.preventDefault();
		var instsData = $(instsForm).serializeArray();
		$.ajax({
			type: "POST",
			url: "/curve",
			data: JSON.stringify(instsData),
			contentType: "application/json;charst=UTF-8",
			success: function (result) {
				displayDFs(result);
			},
			error: function (errObj) {
					   var errMessage = JSON.parse(errObj.responseText);
					   displayBootstrapError(errMessage.message);
				   }
		});
		return false;
	});
});

