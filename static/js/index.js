$(document).ready(function () {
  $(".qtemp").on("click", function () {
    var layout = $(this).data("rep");
    $.ajax({
      url: "/workstation",
      type: "get",
      data: { layout: layout },
      success: function (response) {
        var new_html = response.html;
      },
    });
  });
});
