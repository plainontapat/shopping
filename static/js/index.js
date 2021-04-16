$(function () {
  $("a#myaccount").bind("click", function () {
    $.ajax({
      type: "POST",
      url: "{{url_for('myaccout')}}",
      data: { data: 0 },
    });
  });
});
