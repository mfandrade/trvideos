$(function() {
  $('#btnSubmit').show();
  $('#btnLoading').hide();

  $('form').submit(function(e) {
    $('#btnSubmit').hide();
    $('#btnLoading').show();
  });
});

