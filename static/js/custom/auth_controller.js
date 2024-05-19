htmx.on('store-token', function (event) {
    sessionStorage.setItem('access_token', event.detail.access_token);
    sessionStorage.setItem('refresh_token', event.detail.refresh_token);
});

htmx.on('remove-token', function (event) {
    sessionStorage.removeItem('access_token');
    sessionStorage.removeItem('refresh_token');
    console.log('Token removed');
})