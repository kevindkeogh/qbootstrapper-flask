$(document).on("change", "#conv_instrument_type", function() {
	"use strict";
	/* Watch the instrument type select and hide/unhide the
	 * fixed/float table depending on if its a swap convention */
	var tab = $("#swap-conventions-table");
	var instType = $("#conv_instrument_type").val().toLowerCase();
	if ((instType.includes("swap")) && !(tab.is(":visible"))) {
		tab.show();
	} else {
		tab.hide();
	}
});

$(document).ready(function () {
    "use strict";
	/* Submit button to perform ajax request back to /curve server endpoint */
    var convsForm = $("#conventions-display");
    var csrfToken = $("#csrf-token")[0].value;

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }
    });

	$(convsForm).submit(function (e) {
		e.preventDefault();
		var convData = $(convsForm).serializeArray();
		$.ajax({
			type: "POST",
			url: "/conventions",
			data: JSON.stringify(convData),
			contentType: "application/json;charset=UTF-8",
			success: function (result) {
				console.log(result);
			},
			error: function (err) {
				console.log(err);
		    }
		});
		return false;
	});
});
