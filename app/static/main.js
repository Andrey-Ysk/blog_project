$(function() {
  $('button#rating_vote_up').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/post_full_vote',{
      vote: 'up'
    }, function(data) {
      $('#rating-counter').text(data.rating)
      $('#post-alert').text(data.alert)
    });
    return false;
  });
});
$(function () {
  $('button#rating_vote_down').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/post_full_vote', {
      vote: 'down'
    }, function(data) {
      $('#rating-counter').text(data.rating)
      $('#post-alert').text(data.alert)
    });
    return false;
  });
})
