$(document).ready(function() {

    $('.select2-brands').select2({
        ajax: {
            url: '/api/brands',
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
        },
    });

    $('.select2-devices').select2({
        ajax: {
            url: '/api/devices',
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
        },
    });
});