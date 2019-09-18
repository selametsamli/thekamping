$(function () {
    /* 1. OPEN THE FILE EXPLORER WINDOW */
    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        data: {
            'step': 'step2', 'csrfmiddlewaretoken': "{{ csrf_token }}"
        },
        done: function (e, data) {  /* 3. PROCESS THE RESPONSE FROM THE SERVER */
            if (data.result.is_valid) {
                $("#gallery tbody").prepend(
                    "<tr><td><a href='" + data.result.url + "'>" + data.result.name + "</a></td></tr>"
                )
            }
        }
    })
    ;

});