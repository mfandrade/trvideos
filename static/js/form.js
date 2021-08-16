$(function() {

    // masking time inputs correctly
    $('#begin, #end').mask('60:60', {
        translation: {
            '6': { pattern: /[0-5]/, optional: false }
        }
    });

    // usability on submit
    $('form').submit(function(e) {
        $('#btnSubmit').hide();
        $('#btnLoading').show();
    });
    $('#btnSubmit').show();
    $('#btnLoading').hide();
  
});
