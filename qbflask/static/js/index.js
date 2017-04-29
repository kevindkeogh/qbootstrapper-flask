$(document).ready(function () {
    "use strict";

    var addButton = $(".add-instrument-button");
    var convButton = $(".add-convention-button");
    var conventions; // holds object (ccy) of object (product-types)
                     // of arrays of conventions
    var csrfToken = $("#csrf-token").val();
    var instsForm = $("#instruments-form");
    var wrapper = $(".input-instruments");


    function displayDFs(results) {
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
        /* Parse error text and display in output table */
        var outputTable = $("#output-table");
        $(outputTable).empty();
        outputTable.append("<p class=\"ajax-error\">" + text + "</p>");
    }


    function updateConventions(el) {
        var convSelectId = el.id.substring(0,
                el.id.length - "instrument_type".length);
        convSelectId = "#" + convSelectId + "convention";
        var convSelect = $(convSelectId);

        var ccy = $("#currency").val();
        var instType = el.value;

        if (!conventions.hasOwnProperty(ccy)) {
            // Check if currency is in conventions
            convSelect.empty();
            return false;
        }
        if (!conventions[ccy].hasOwnProperty(instType)) {
            // Check if instrument type is in conventions
            convSelect.empty();
            return false;
        }

        try {
            var opts = conventions[ccy][instType];
            convSelect.empty();
            if (opts !== undefined) {
                opts.forEach(function (opt) {
                    convSelect.append($("<option></option>")
                        .attr("value", opt)
                        .text(opt));
                });
            }
        } catch (err) {
            console.log(err);
        }
        return false;
    }


    $(addButton).click(function (e) {
        /* Copy last instruments row and append to last row of table
         */
        e.preventDefault();
        var lastRow = $("#instruments-table tr:last");
        var newRow = lastRow.clone(true);
        var rowNum = parseInt(lastRow.attr("id").replace(/[^0-9.]/g, ""));
        rowNum += 1;
        newRow.attr("id", "inst-" + rowNum);
        newRow.children().each(function () {
            var td = this.children[0];
            if (td.tagName.toLowerCase() === "span") {
                // catch the case where the input is covered by a span
                td = td.children[0];
            }
            td.name = td.name.replace(/\d+/g, rowNum);
            td.id = td.id.replace(/\d+/g, rowNum);
        });
        lastRow.after(newRow);
        updateConventions(newRow.find(".inst-type").get(0));
    });

    $(wrapper).on("click", ".remove-instrument-button", function (e) {
        /* Button to delete the row, but avoid deleting the row if its
         * the only one
         */
        e.preventDefault();
        var numRows = $(this).parent().parent().parent().children().length;
        if (numRows > 2) { // not sure why this is 2, not 1...
            $(this).parent().parent().remove();
        }
    });


    $(convButton).click(function (e) {
        /* Hijack "Add convention" button to be a link */
        e.preventDefault();
        window.location.href = "/conventions";
        return false;
    });


    $.ajaxSetup({
        /* Submit button to perform ajax request back to /curve server endpoint
        */
        beforeSend: function (xhr, settings) {
                        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                            xhr.setRequestHeader("X-CSRFToken", csrfToken);
                        }
                    }
    });

    $(instsForm).submit(function (e) {
        /* Send form back to server to bootstrap, call displayDFs on return
         */
        e.preventDefault();
        var instsData = $(instsForm).serializeArray();
        $.ajax({
            type: "POST",
            url: "/api/v1/bootstrap",
            data: JSON.stringify(instsData),
            contentType: "application/json;charset=UTF-8",
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


    $.ajax({
        /* Send request back to the /conventions/get endpoint for conventions
         */
        type: "GET",
        url: "/api/v1/conventions/get",
        contentType: "application/json;charset=UTF-8",
        success: function (result) {
            conventions = result;
        }
    //TODO: add error
    });

    $(".inst-type, #currency").on("change", function (e) {
        /* Populate the conventions when either the currency or
         * instrument type changes
         */
        if (e.target.className === "inst-type") {
            updateConventions(e.target);
        } else if (e.target.id === "currency") {
            var instTypes = $(".inst-type");
            instTypes.each(function (idx, el) {
                updateConventions(el);
            });
        }
    });
});
