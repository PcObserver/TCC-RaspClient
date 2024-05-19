$(document).ready(function() {

    $('.select2-brands').select2({
        theme: 'bootstrap4',
        ajax: {
            url: '/brands',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    q: params.term,
                };
            },
            processResults: function(data) {
                return {
                    results: data.brands,
                };
            },
            cache: true,
        },
    });

    $('.select2-devices').select2({
        theme: 'bootstrap4',
        ajax: {
            url: '/devices',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    q: params.term,
                };
            },
            processResults: function(data) {
                return {
                    results: data.devices,
                };
            },
            cache: true,
        },
    });
});