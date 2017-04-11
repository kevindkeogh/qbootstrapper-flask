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
                console.log(result); // TODO: parse to show table of DFs
            }
        });
        return false;
    });
});
