$(document).ready(function () {
    "use strict";
    var instsForm = $("#instruments-form");

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
            }
        });
        return false;
    });
});

function displayDFs (results) {
	"use strict";
	var outputTable = $("#output-table");
	$(outputTable).empty() // Remove all child elements
						   // in case this is not the first run
	var headerRow = $("<thead><tr><th>Dates</th>"
			          + "<th>Discount Factors</th></tr></thead>");
	$(headerRow).appendTo(outputTable);

	var numRows = results.dates.length;
	for (var i=0; i<numRows; i++) {
		var date = results.dates[i];
		var df = results.dfs[i].toString().substring(0, 12);
		outputTable.append("<tr><td class=\"date\">" + date +          "</td>"
						 +     "<td class=\"discount-factor\">" + df + "</td>"
						 + "</tr>");
	};
}
