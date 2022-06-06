// //login js for login 
$("#submit", ).click(function(e) {
    var form = $("#needs-validation")[0];
    var isValid = form.checkValidity();
    if (!isValid) {
        e.preventDefault();
        e.stopPropagation();
    }
    form.classList.add('was-validated');
    //alert("hkldasfglagdf");
    e.preventDefault();
    // For testing only to stay on this page


    var email = $('#email').val();
    let password = $('#password1').val();
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log(password);
    $.ajax({
        url: "/api/signin/",
        type: 'POST',
        data: {
            'email': email,
            'password': password,
            'csrf': csrf
        },


        //headers: { 'Content-type': 'application/json', 'Accept': 'text/plain' },
        //dataType: 'json',
        // Fetch the stored token from localStorage and set in the header
        success: function(data) {

            //$("#modal-book .modal-content").html(data.html_form);
            console.log(data.is_valid);
            if (data.success == true) {
                var token = data.token;
                console.log(token);
                sessionStorage.setItem('MyUniqueUserToken',
                    JSON.stringify(
                        token
                    )

                );
                window.location.href = "/settings/security/";

            } else if (data.is_valid == true) {
                $("#errorlogin").html("Please verify this E-mail address.");
            } else {
                $('#errorlogin').show();
                $("#errorlogin").html(`<span class='alert alert-danger fade show text-center' role='alert' style='margin-bottom:0px;'>ERROR: Email or Password is not correct !`);
                var duration = 2000; //2 seconds
                setTimeout(function() { $('#errorlogin').hide(); }, duration);
            }

            // window.location.href = "{% url 'blogg:index' %}";
        },
        error: function(data) {
            // alert the error if any error occured
            alert(data)
            if (data.msg) {
                $("#errorlogin").html("Please verify this E-mail address.");
            } else {
                $("#errorlogin").html(`<span class='alert alert-danger'>Ok! Response: ${data}`);
            }
        }
    });

});

//end of login
(function() {
    'use strict';
    window.addEventListener('load', function() {
        var form = document.getElementById('needs-validation');
        form.addEventListener('submit', function(event) {
            if (form.checkValidity() === false) {
                event.preventDefault();
                event.stopPropagation();
            }

            form.classList.add('was-validated');
        }, false);
    }, false);
})();

// function onSignIn(googleUser) {
//     var profile = googleUser.getBasicProfile();
//     Shiny.onInputChange("g.email", profile.getEmail());
//     var id_token = googleUser.getAuthResponse().id_token;
//     Shiny.onInputChange("g.id_token", id_token);
// }

// function signOut() {
//     var auth2 = gapi.auth2.getAuthInstance();
//     auth2.signOut();
//     Shiny.onInputChange("g.email", null);
//     Shiny.onInputChange("g.id_token", null);
// }

// $(document).ready(function() {
//             // check user process is lock or not
//             $(document).on("click", "#post", function() {
//                 let url = "/create_blog/";
//                 let token = JSON.parse(sessionStorage.getItem('MyUniqueUserToken'));
//                 $.ajax({
//                     url: url,
//                     type: 'GET',
//                     data: {
//                         'engagement_id': "1",

//                     },
//                     headers: {
//                         "Authentication": token
//                     },

//                     success: (data) => {
//                         console.log(data);
//                         // var data = JSON.parse(data);
//                         // if (data.msg_type == "error") {
//                         //  alert(data.msg);
//                         //  return false;
//                         // } else {
//                         //  data_url = $(this).attr('data-url');
//                         //  window.location.href = data_url;
//                         // }
//                     }
//                 });
//             });


// <
// script src = "https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js" > < /script> <
// script >
//     $(document).ready(function() {
//         console.log("{{request.session.token}}");
//         //pretend to get a token after logging in
//         sessionStorage.setItem('MyUniqueUserToken',
//             JSON.stringify(
//                 "{{request.session.token}}"
//             )
//         );
//         $('#submit').on('click', function() {
//             // e.preventDefault();

//             $.ajax({
//                 url: "/api/signin",
//                 type: 'POST',
//                 // Fetch the stored token from localStorage and set in the header
//                 success: function(response) {
//                     alert("resp");
//                     // window.location.href = "{% url 'blogg:index' %}";
//                 },
//             });

//         });
//     });

// <
// /script>