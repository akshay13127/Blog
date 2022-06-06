$(document).ready(function() {

    $("#imgform", ).click(function(e) {
        e.preventDefault();
        // alert(e);
        let token = JSON.parse(sessionStorage.getItem('MyUniqueUserToken'));
        var id = $('#idd').val();
        var form = "/pro_pic/" + id;

        var fd = new FormData();
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        // alert(fd);
        var photos = $('#Img').get(0).files[0];
        fd.append('csrf', csrf);
        fd.append('photo', photos);
        console.log(photos);
        $.ajax({
            type: 'POST',
            url: form,
            data: fd,
            headers: { 'Authorization': token },
            processData: false,
            contentType: false,
            success: function(data) {
                $('#msgs').show();
                $("#msgs").html(`<span class='alert alert-success fade show text-center' role='alert' style='margin-bottom:0px;'>SUCCESS: You're Register Successfully...`);
                var duration = 5000; //2 seconds
                setTimeout(function() { $('#msgs').hide(); }, duration);
                console.log("Image Update");
                window.location.reload(true);
            },
        });
    });

    $("#postform", ).click(function(e) {
        e.preventDefault();

        //alert("save ho rha h");
        var fd = new FormData();
        let token = JSON.parse(sessionStorage.getItem('MyUniqueUserToken'));
        let title = $('#title').val();
        let content = $('#Content').val();
        let csrf = $("input[name=csrfmiddlewaretoken]").val();
        let uname = $("#uname").val();
        let slug = $("#slug").val();
        let photos = $('#photos').get(0).files[0];
        console.log(photos);
        fd.append('title', title);
        fd.append('Content', content);
        fd.append('csrf', csrf);
        fd.append('uname', uname);
        fd.append('slug', slug);
        fd.append('photos', photos);
        console.log(fd)
        if (title == "") {
            alert("Please enter title");
        } else if (content == "") {
            alert("Please enter content");
        } else if (uname == "") {
            $('#msgs1').show();
            $("#msgs1").html(`<span class='alert alert-danger fade show text-center' role='alert' style='margin-bottom:0px;'>ERROR: You're Not Authorised. Login First...`);
            var duration = 5000; //2 seconds
            setTimeout(function() { $('#msgs').hide(); }, duration);
            console.log("form submgafdgfasgafgit");
        } else {
            mydata = { title: title, content: content, uname: uname, csrf: csrf, photos: fd }

            let url = "/edit/";
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
                        $('#msgs1').show();
                        $("#msgs1").html(`<span class='alert alert-success fade show text-center' role='alert' style='margin-bottom:0px;'>SUCCESS: You're Blog Post Successfully...`);
                        var duration = 5000; //2 seconds
                        setTimeout(function() { $('#msgs1').hide(); }, duration);
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