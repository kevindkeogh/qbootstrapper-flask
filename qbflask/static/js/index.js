$(document).ready(function () {
	"use strict";
	/* Copy last instruments row and append to last row of table */
	var wrapper = $(".input-instruments");
	var addButton = $(".add-instrument-button");

	$(addButton).click(function (e) {
		e.preventDefault();
		var lastRow = $("#instruments-table tr:last");
		var newRow = lastRow.clone(true);
		var rowNum = parseInt(lastRow.attr("id").replace(/[^0-9.]/g, ""));
		rowNum += 1;
		newRow.attr("id", "inst-" + rowNum);
		newRow.children().each(function () {
			var td = this.children[0];
			if (td.tagName.toLowerCase() === "span") {
				td = td.children[0];
			}
			td.name = td.name.replace(/\d+/g, rowNum);
			td.id = td.id.replace(/\d+/g, rowNum);
		});
		lastRow.after(newRow);
	});

	$(wrapper).on("click", ".remove-instrument-button", function (e) {
	/* TODO: Prevent deleting first row */
		e.preventDefault();
		$(this).parent().parent().remove();
	});
});


$(document).ready(function () {
	"use strict";
	/* Hijack "Add convention" button to be a link */
	var convButton = $(".add-convention-button");

	$(convButton).click(function (e) {
		e.preventDefault();
		window.location.href = "/conventions";
		return false;
	});
});


$(document).ready(function () {
    "use strict";
	/* Submit button to perform ajax request back to /curve server endpoint */
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


function displayDFs(results) {
    "use strict";
	/* Parse results of discount factor results JSON and show in table */
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
	/* Parse error text and display in output table */
    var outputTable = $("#output-table");
    $(outputTable).empty();
    outputTable.append("<p class=\"ajax-error\">" + text + "</p>");
}