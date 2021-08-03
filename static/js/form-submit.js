var loading = $('div#loading');
$(function() {
  $('form').submit(function(e) {
    e.preventDefault();
    loading.show();
    $.ajax({
      url: '/process', // # TODO: endereço destino
      data: $(this).serialize(),
      method: 'post',
      dataType: 'JSON'
    }).done(function(res) {
      loading.hide();
      alert(res.status);
    });
  });
});
