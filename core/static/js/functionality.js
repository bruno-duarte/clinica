window.onload = function() {
    var cpf = document.getElementById("cpf"),
        user = document.getElementById("username");
    cpf.addEventListener('input', function() {
        user.value = cpf.value;
    });
};

function validaData() {  
	var status = false;  
	var data_consulta = document.getElementById("data").value;
	var data = new Date();
	var hoje = data.getFullYear() + '-' + (data.getMonth()+1) + '-' + data.getDate();

	if (Date.parse(data_consulta) > Date.parse(hoje)) {
		status = true;   
    } else if (Date.parse(data_consulta) == Date.parse(hoje)) {
        if (data.getHours() <= 7) {
            status = true;
        } else {
            document.getElementById("erro").innerHTML = "Data inválida ou horário de agendamento excedido para hoje.";
            status = false;
        }
    } else {
    	document.getElementById("erro").innerHTML = "Data inválida ou horário de agendamento excedido para hoje.";
    	status = false;  
    }
	    
	return status;  
} 

function preCarregamento() {
    perfil = document.getElementById('user-image');
    imagem = document.getElementById('imagem'); 
    perfil.src = (window.URL ? URL : webkitURL).createObjectURL(imagem.files[0]);
}

function mudaEstadoC() {
    entrada = document.getElementById('estado');
    entrada.value = 'Cancelada';
}

function mudaEstadoA() {
    entrada = document.getElementById('estado');
    entrada.value = 'Agendada';
}

function incrementaData() {
    var data_str = document.getElementById('data-consulta').value;
    var data = new Date(data_str);

    data.setDate(data.getDate() + 2);
    var str = data.getFullYear() + '-' + (data.getMonth() + 1) + '-' + data.getDate();
    document.getElementById('data-consulta').value = str;
}

function decrementaData() {
    var data_str = document.getElementById('data-consulta').value;
    var data = new Date(data_str);
    var botao_decremento = document.getElementById('esquerda');
    var hoje = new Date();
    var hoje = hoje.getFullYear() + '-' + (hoje.getMonth() + 1) + '-' + hoje.getDate();

    data.setDate(data.getDate());
    var str = data.getFullYear() + '-' + (data.getMonth() + 1) + '-' + data.getDate();

    if (Date.parse(str) > Date.parse(hoje)) {
        document.getElementById('data-consulta').value = str;
    } else {
        botao_decremento.disabled;
    } 
}

$('.patient-avatar').on('load', function() {
    
});

function inicia() {
    var colors = [
        '#53ff54',
        '#76bae9',
        '#ff7ee6',
        '#0067fe',
        '#fb8229',
        '#20c0f3'
    ]

    var imagem = document.getElementById('imagem');
    var botao_incremento = document.getElementById('direita');
    var botao_decremento = document.getElementById('esquerda');
    
    var avatars = document.getElementsByClassName('patient-avatar');

    for (let i = 0; i < avatars.length; i++) {
        var index = Math.floor(Math.random() * 6);
        var backgroundColor = colors[index];
        avatars[i].style.backgroundColor = backgroundColor;
    }

    botao_incremento.addEventListener('click', incrementaData);
    botao_decremento.addEventListener('click', decrementaData);
    
    imagem.addEventListener('change', preCarregamento);
}

window.addEventListener('load', inicia);
