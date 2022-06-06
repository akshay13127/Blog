$(document).ready(function(e) {




    // This WILL work because we are listening on the 'document', 
    // for a click on an element with an ID of #test-element
    $(document).on("click", "#wrtblog1", function(e) {
        let token = JSON.parse(sessionStorage.getItem('MyUniqueUserToken'));

        $.ajax({
            url: "/list",
            type: 'GET',
            headers: { 'Authorization': token },
            success: function(response, json, value) {
                console.log(value, "----------------------------------------------------");

                window.location.href = "/list/";
                // e.preventDefault();

            },
            // on error
            error: function(response) {
                // alert the error if any error occured
                console.log(response.responseJSON.errors)
            }

        });

        return false;
    });



});

window.onload = function() {
    var duration = 2000; //2 seconds
    setTimeout(function() { $('#my').hide(); }, duration);
    console.log('agfgdsahfjhgdsfhdshfghsdafgjhsd');
};



// const URL = document.location.href;
// fetch(URL, {
//         headers: {
//             'Accept': 'application/json',
//             'X-Requested-With': 'XMLHttpRequest', //Necessary to work with request.is_ajax()
//         },
//     })
//     .then(response => {
//         return response.json() //Convert response to JSON
//     })
//     .then(data => {
//         console.log(data)
//             //Perform actions with the response data from the view
//     })



$(document).ready(function() {

    $("#logout").click(function(e) {
        // e.preventDefault();
        sessionStorage.removeItem("MyUniqueUserToken");
        // window.location.href = "/api/signin"
    });
});






$(document).ready(function() {

    $("#post", ).click(function(e) {
        e.preventDefault();

        //alert("save ho rha h");
        var fd = new FormData();
        let token = JSON.parse(sessionStorage.getItem('MyUniqueUserToken'));
        let title = $('#title').val();
        let content = $('#Content').val();
        let csrf = $("input[name=csrfmiddlewaretoken").val();
        let uname = $("#uname").val();
        let photos = $('#photos').get(0).files[0];
        console.log(photos);
        fd.append('title', title);
        fd.append('Content', content);
        fd.append('csrf', csrf);
        fd.append('uname', uname);
        fd.append('photos', photos);
        console.log(fd)
        if (title == "") {
            alert("Please enter title");
        } else if (content == "") {
            alert("Please enter content");
        } else if (uname == "") {
            $('#msgs').show();
            $("#msgs").html(`<span class='alert alert-danger fade show text-center' role='alert' style='margin-bottom:0px;'>ERROR: You're Not Authorised. Login First...`);
            var duration = 5000; //2 seconds
            setTimeout(function() { $('#msgs').hide(); }, duration);
            console.log("form submgafdgfasgafgit");
        } else {
            mydata = { title: title, content: content, uname: uname, csrf: csrf, photos: fd }

            let url = "/create/";
            $.ajax({
                url: url,
                type: 'POST',
                contentType: false,
                processData: false,
                data: fd,
                headers: { 'Authorization': token },
                success: function(data) {
                    // alert("Blog successfully Post!!!!!!!!!!!!");
                    console.log(data);
                    console.log(data.status);
                    if (data.status == 200) {
                        $('#msgs').show();
                        $("#msgs").html(`<span class='alert alert-success fade show text-center' role='alert' style='margin-bottom:0px;'>SUCCESS: You're Blog Post Successfully...`);
                        var duration = 5000; //2 seconds
                        setTimeout(function() { $('#msgs').hide(); }, duration);
                        console.log("form submit");
                        document.getElementById("formid").reset();
                        // window.location.reload(true);
                        // $('#msgs').show();
                        // $("#msgs").html(`<span class='alert alert-success fade show text-center' role='alert' style='margin-bottom:0px;'>SUCCESS: You're Blog Post Successfully...`);
                        // var duration = 2000; //2 seconds
                        // setTimeout(function() { $('#msgs').hide(); }, duration);
                    } else {
                        alert("sdfhdaslfkjhldasjhfjklshdalfhljksadfjkls");

                    }
                },
            });
        }
        success: (data) => {

                console.log(data);
                //alert(data);

            }
            // });

    });


});


// $(document).focusout(function() {
//     $("#title").focusout(function() {
//         if ($(this).val() == '') {

//             $("#title").css('border', 'solid 1px red');
//         } else {

//             // If it is not blank. 
//             $("#title").css('border', 'solid 1px green');
//             // $('#danger').remove();
//         }
//     }).trigger("focusout");
// });

// $("textarea").focusout(function() {
//     $("textarea").focusout(function() {
//         if ($(this).val() == '') {

//             $("#Content").css('border', 'solid 1px red');
//         } else {

//             // If it is not blank. 
//             $("#Content").css('border', 'solid 1px green');
//             // $('#dangercontent').remove();
//         }
//     }).trigger("focusout");
// });