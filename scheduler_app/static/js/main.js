$(document).ready(function(){
    $('#classForm').submit(function(event) {
        event.preventDefault();
        console.log(event);
        $.ajax({
            url: $('#classForm').attr('action'),
            method: $('#classForm').attr('method'),
            data: $(this).serialize(),
            success : function(response) {
                $('#divSubject').append(response);
                $('#classForm').trigger('reset');
            }
        });
    });
});
