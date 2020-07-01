 function temCampoVazio() {
    var form = document.getElementById('signup-form');
    for (let i = 0; i < form.length; i++) {
        if (form[i].value == "") { 
            if (i == 1 || i >= 10) continue
            if (form[i].value == "") {
                return true;
            } 
        }
    }
    return false;
}

function habilitaBotao() {
    var botao = document.getElementById('signup-btn');
    if (temCampoVazio()) botao.disabled = true;
    else botao.disabled = false;
}

$('#signup-modal').modal({
    backdrop: 'static',
    keyboard: false
});

$('#appointment-form').on('submit', function(e) {
    $('#appointment-modal').modal('show');
    e.preventDefault();
});
