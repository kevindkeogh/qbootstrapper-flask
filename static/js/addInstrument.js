$(document).ready(function () {
    "use strict";
    var maxFields = 30;
    var wrapper = $(".input-instruments");
    var addButton = $(".addInstrumentButton");

    var index = 1;

    $(addButton).click(function (e) {
        e.preventDefault();
        if (index < maxFields) { // not reached max insts
            index += 1;
            var lastRow = $("#instruments-table tr:last");
            var newRow = lastRow.clone(true);
            var rowNum = lastRow.attr("id").replace(/[^0-9.]/g, "");
            rowNum += 1;
            newRow.attr("id", "inst-" + rowNum);
            newRow.children().each(function () {
                var td = this.children[0];
                td.name = td.name.replace(/\d+/g, rowNum);
                td.id = td.id.replace(/\d+/g, rowNum);
            });
            $(wrapper).find("tbody:last").append(newRow);
        }
    });

    $(wrapper).on("click", ".removeInstrumentButton", function (e) {
        e.preventDefault();
        $(this).parent().parent().remove();
    });
});
