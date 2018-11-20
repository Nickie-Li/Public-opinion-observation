$(function() {
    $('submit').click(function() {
        var result = $('#freqOption').val();
        $.ajax({
            url: '/Awordcloud',
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