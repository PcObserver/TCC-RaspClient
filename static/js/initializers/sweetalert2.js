document.addEventListener("htmx:confirm", function(e) {
    should_publish = $('#is_public').is(':checked')
    e.preventDefault()
    Swal.fire({
        title: "Atenção!",
        text: `${e.detail.question} ${should_publish ? 'Essa ação tambem tera efeito no repositorio remoto!' : ''}`,
        showDenyButton: true,
        confirmButtonText: `Sim`,
        denyButtonText: `Não`,
        focusDeny: true,
    }).then(function(result) {
        if(result.isConfirmed) e.detail.issueRequest(true) // use true to skip window.confirm
    })
})