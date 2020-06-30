 function campoVazio() {
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
    var botao = document.getElementById('botao-signup');
    if (campoVazio()) botao.disabled = true;
    else botao.disabled = false;
}

$('#myModal').modal({
    backdrop: 'static',
    keyboard: false
});
