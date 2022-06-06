// window.onload = function() {
//     var duration = 2000; //2 seconds
//     setTimeout(function() { $('#my').hide(); }, duration);
// };

// $(function() {
//     $("#search").autocomplete({
//         source: "{% url 'blogg:autosuggest' %}",

//     });
// });


// sessionStorage.setItem('MyUniqueUserToken',
//     JSON.stringify(
//         '{{request.session.token}}'
//     )
// );
// // let token = JSON.parse(sessionStorage.getItem('MyUniqueUserToken'));
// console.log("haa bhai ho gya" + token);

// $(document).on("click", "#wrtblog1", function() {

//     $.ajax({
//         url: '/create',
//         type: 'GET',
//         // dataType: 'json',
//         success: function(result) {
//             console.log(result);
//             // console.log(url)
//             // window.location.href = "{% url 'blogg:create' %}";
//         }
//     });
// });


// $(document).ready(function() {
//     $(document).ajaxComplete(function(e, xhr, settings) {
//         if (xhr.status == 278) {
//             window.location.href = xhr.getResponseHeader("{% url 'blogg:create' %}");
//         }
//     });
// }); 


document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('wrtblog1').addEventListener('click', sendReq);
});

let sendReq = (ev) => {
    let url = "{% url 'blogg:create' %}";

    let req = new Request(url, {
        method: 'GET',
        mode: 'cors',
    });

    fetch(req)
        .then(resp => "dajhfklja")
        .then(data => {
            console.error("111111111111111");
            window.location.href = "{% url 'blogg:create' %}";

        })
        .catch(err => {
            console.error("2222222222222222");
            console.error(err.message);
        })
}









// $("#Btn").on('click', function() {
//     let temp = $('#akshay').val();
//     alert(temp);
//     $.ajax({
//         type: "GET",
//         url: "http://127.0.0.1:8000/list/",
//         headers: {
//             'Authorization': 'Bearer localStorage.getItem("token")'
//         },
//         success: function(data) {
//             console.log("ertg3we4t234th");
//         }
//     });
// });