$(document).ready(function(){

    $('#add-class').submit(function(e) {
    
        console.log('click');
        e.preventDefault()
        const form = $('#classForm');
        console.log(form.serialize());
        $.ajax({
            url: form.attr('action'),
            type: form.attr('method'),
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
              },
            data: {
                name : $('#name').val(),
                url: $('#url').val(),
                lecture_date: $('#lectureDate').val(),
                description: $('#description').val(),
            },
            success : function(response) {
                console.log("hello"),
                $('#subject').append(response),
                alert("Created a new class!")
            }
        })
    
      });

})




//   $('#add-class').on("submit", function(e) {
//     var formData = $(this).serialize(); 
//     $.ajax({
//         type: "POST",
//         url: "/create_subject",
//         data: formData,
//         success: function () {
//             console.log('working')
//     }
//     });

//     e.preventDefault();
//     })