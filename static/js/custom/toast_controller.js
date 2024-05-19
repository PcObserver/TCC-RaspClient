$('.toast').map(function (index, element) {
    if (element.classList.contains('hide')) { return; }
    let toast = new bootstrap.Toast(element);
    toast.show();
    setTimeout(function () { element.remove(); }, 15 * 1000);
});
document.addEventListener('DOMContentLoaded', function () {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function (toastEl) {
        return new bootstrap.Toast(toastEl)
    })
    toastList.forEach(toast => toast.show());
});

// HTMX requests
htmx.onLoad(function (content) {
    [content].map(el => {
        if (el.classList.contains('toast')) {
            let toast = new bootstrap.Toast(el);
            toast.show();
            setTimeout(function () {
                el.remove();
            }, 15 * 1000);
        }
    });
});