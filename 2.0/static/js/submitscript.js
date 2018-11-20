$(function() {
    $('submit').click(function() {
        var user = $('#txtname').val();
        var pass = $('#radioCycle').val();
        var key = $('#keyword').val();
        $.ajax({
            url: '/register',
            data: $('form').serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
});