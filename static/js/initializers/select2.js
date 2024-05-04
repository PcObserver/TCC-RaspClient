$(document).ready(function() {
    $('.select2-brands').select2({
        ajax: {
            url: '/api/brands',
            dataType: 'json',
            delay: 250,
            data: function(params) {
                return {
                    search: params.term,
                    page: params.page
                };
            },
            processResults: function(data, params) {
                return {
                    results: data.data,
                    pagination: {
                        more: data.meta.current_page < data.meta.last_page
                    }
                };
            },
            cache: true
        },
    });
});