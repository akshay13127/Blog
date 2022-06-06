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


    var fname = $('#firstname').val();
    var lname = $('#lastname').val();
    var city = $('#city').val();
    var state = $('#state').val();
    var contact = $('#contact').val();
    var email = $('#email').val();
    var password = $('#password3').val();
    let repassword = $('#repassword').val();
    let csrf = $("input[name=csrfmiddlewaretoken]").val();
    console.log(password, 'jhfljkdshafjklhsjak');
    console.log(repassword);
    if (password != repassword) {
        $('#signup_msg').show();
        $("#signup_msg").html(`<span class='alert alert-danger fade show text-center' role='alert' style='margin-bottom:0px;'>ERROR:Password didn't Match!!!!`);
        var duration = 2000; //2 seconds
        setTimeout(function() { $('#signup_msg').hide(); }, duration);
    } else {
        $.ajax({
            url: "/api/signup/",
            type: 'POST',
            data: {
                'person.fname': fname,
                'person.lname': lname,
                'person.contact': contact,
                'person.city': city,
                'person.state': state,
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
                    $('#msgs').show();
                    $("#msgs").html(`<span class='alert alert-success fade show text-center' role='alert' style='margin-bottom:0px;'>SUCCESS: You're Register Successfully...`);
                    var duration = 5000; //2 seconds
                    setTimeout(function() { $('#msgs').hide(); }, duration);
                    console.log("form submit");
                    window.location.href = "/api/signin";

                } else if (data.is_valid == true) {
                    $("#signup_msg").html("Please verify this E-mail address.");
                } else {
                    $('#signup_msg').show();
                    $("#signup_msg").html(`<span class='alert alert-danger fade show text-center' role='alert' style='margin-bottom:0px;'>ERROR: Email already exists!!!!!!!!!!!!!!`);
                    var duration = 2000; //2 seconds
                    setTimeout(function() { $('#signup_msg').hide(); }, duration);
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
    }

});










// (function() {
//     'use strict';
//     window.addEventListener('load', function() {
//         var form = document.getElementById('needs-validation');
//         form.addEventListener('submit', function(event) {
//             if (form.checkValidity() === false) {
//                 event.preventDefault();
//                 event.stopPropagation();
//             } else {

//             }
//             form.classList.add('was-validated');
//         }, false);
//     }, false);
// })();

// $(document).ready(function() {
//     $("#needs-validation").validate({
//         // Specify validation rules
//         rules: {

//             email: {
//                 required: true,
//                 email: true
//             },
//             password: {
//                 required: true,
//                 minlength: 5
//             },
//             repassword: {
//                 required: true,
//                 minlength: 5,
//                 equalTo: "#password"
//             }
//         },

//     });
// });

// $(document).on('click', '.navbar-toggler', function() {
//     $toggle = $(this);
//     $navbar = $('.navbar[color-on-scroll]');
//     scroll_distance = $navbar.attr('color-on-scroll') || 500;

//     if (materialKit.misc.navbar_menu_visible == 1) {
//         $('body').removeClass('nav-open');
//         materialKit.misc.navbar_menu_visible = 0;
//         $('#bodyClick').remove();
//         setTimeout(function() {
//             $toggle.removeClass('toggled');
//         }, 550);

//         $('body').removeClass('nav-open-absolute');
//     } else {
//         setTimeout(function() {
//             $toggle.addClass('toggled');
//         }, 580);


//         div = '<div id="bodyClick"></div>';
//         $(div).appendTo("body").click(function() {
//             $('body').removeClass('nav-open');

//             if ($('nav').hasClass('navbar-absolute')) {
//                 $('body').removeClass('nav-open-absolute');
//             }
//             materialKit.misc.navbar_menu_visible = 0;
//             $('#bodyClick').remove();
//             setTimeout(function() {
//                 $toggle.removeClass('toggled');
//             }, 550);
//         });

//         if ($('nav').hasClass('navbar-absolute')) {
//             $('html').addClass('nav-open-absolute');
//         }

//         $('body').addClass('nav-open');
//         materialKit.misc.navbar_menu_visible = 1;
//     }

//     if ($('.navbar-color-on-scroll').length != 0) {
//         $(window).on('scroll', materialKit.checkScrollForTransparentNavbar)
//     }
// });

// materialKit = {
//     misc: {
//         navbar_menu_visible: 0,
//         window_width: 0,
//         transparent: true,
//         fixedTop: false,
//         navbar_initialized: false,
//         isWindow: document.documentMode || /Edge/.test(navigator.userAgent)
//     },

//     checkScrollForTransparentNavbar: debounce(function() {
//         if ($(document).scrollTop() > scroll_distance) {
//             if (materialKit.misc.transparent) {
//                 materialKit.misc.transparent = false;
//                 $('.navbar-color-on-scroll').removeClass('navbar-transparent');
//             }
//         } else {
//             if (!materialKit.misc.transparent) {
//                 materialKit.misc.transparent = true;
//                 $('.navbar-color-on-scroll').addClass('navbar-transparent');
//             }
//         }
//     }, 17)
// };

// function debounce(func, wait, immediate) {
//     var timeout;
//     return function() {
//         var context = this,
//             args = arguments;
//         clearTimeout(timeout);
//         timeout = setTimeout(function() {
//             timeout = null;
//             if (!immediate) func.apply(context, args);
//         }, wait);
//         if (immediate && !timeout) func.apply(context, args);
//     };
// };