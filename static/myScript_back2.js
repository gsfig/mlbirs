$(document).ready(function () {

    $("#btnSubmit").click(function (event) {

        //stop submit the form, we will post it manually.
        event.preventDefault();

        var data = $('#fileUploadForm').serialize();

        console.log(data);

		// disabled the submit button
        $("#btnSubmit").prop("disabled", true);

        $.ajax({
            type: "GET",
            //enctype: 'multipart/form-data',
            url: "sendQuery",
            data: data,
            processData: false,
            contentType: false,
            cache: false,
            timeout: 600000,
            success: function (data) {

                //$("#result").text(data);
                console.log("SUCCESS : ", data);
                obj = JSON.parse(data);
                var keys = Object.keys(obj);
                for(var i=0;i<keys.length;i++){
                    var key = keys[i];
                    console.log(key, obj[key]);
                    tr = $("<tr></tr>");
                    tr.append("<td>" + key + "</td>");
                    tr.append("<td>" + obj[key] + "</td>");
                    $("#result").append(tr);
                }

                $("#btnSubmit").prop("disabled", false);



            },
            error: function (e) {

                $("#result").text(e.responseText);
                console.log("ERROR : ", e);
                $("#btnSubmit").prop("disabled", false);

            }
        });
    });
});