//$.getScript('{{ url_for('static', filename = 'myScript.js') }}', function() {
//    alert('Load was performed.');
//});

$(document).ready(function () {
    $("#show").toggle();
    flag = true;
    $("#resizable").resizable();


    $("#btnSubmit").click(function (event) {

        //stop submit the form, we will post it manually.
        event.preventDefault();

        var data = $('#fileUploadForm').serialize();

        // console.log(data);

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
                /*var keys = Object.keys(obj);
                for(var i=0;i<keys.length;i++){
                    var key = keys[i];
                    console.log(key, obj[key]);
                    tr = $("<tr></tr>");
                    tr.append("<td>" + key + "</td>");
                    tr.append("<td>" + obj[key] + "</td>");
                    $("#result").append(tr);
                }*/

                //create Tabulator on DOM element with id "example-table"
                $("#example-table").tabulator({
                    height:150, // set height of table, this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
                    layout:"fitColumns", //fit columns to width of table (optional)

                    columns:[ //Define Table Columns
                        {title:"Summary", field:"doc_text", align:"center", headerSort:false},
                        //{title:"Similaridade", field:"average_score", headerFilter:"input", headerFilterPlaceholder:"valor mínimo (max= 10)", headerFilterFunc:">=", align:"center", width:150, sorter:"number", formatter:"progress",formatterParams:{min:0, max:1, color:'#000099'}},
                        {title:"Similarity", field:"average_score", align:"center", width:150, sorter:"number", formatter:"progress",formatterParams:{min:0, max:100, color:'#000099'}},

                        {title:"%", field:"average_score", align:"center", sorter:"number", width:80, sorterParams:{dir:"desc"}},
                    ],
                    initialSort:[
                        {column:"average_score", dir:"desc"}, //sort by this first
                        //{column:"doc_text", dir:"desc"}, //then sort by this second
                    ],
                    rowClick:function(e, row){ //trigger this when the row is clicked
                        if(flag){
                            $("#show").toggle();
                            flag = false
                        };


                        var alltext = row.getData().doc_text;
                        // alert("Row " + row.getData().average_score + " Clicked!!!!");
                        $("#full-text").text(function(){
                            return alltext
                        });

                    }
                });
                //define data
                var tablescores = [];
                for(var x in obj){ // json to array
                  tablescores.push(obj[x]);
                }

                //load sample data into the table
                $("#example-table").tabulator("setData", tablescores);
                // $("#example-table").tabulator("setFilter", "average_score", ">", 0.5);

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