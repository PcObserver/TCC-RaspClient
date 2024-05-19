$("form").submit(function (e) {
    e.preventDefault();
    var is_public = $(this).find("#is_public").is(":checked");
    var accessToken = sessionStorage.getItem("access_token", "");
    if (!accessToken && is_public) {
      htmx.trigger("#auth-toggle", "click");
      return;
    }
    e.target.submit();
});