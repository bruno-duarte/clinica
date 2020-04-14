
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
	var hoje = data.getFullYear()+'-'+(data.getMonth()+1)+'-'+data.getDate();

	if (Date.parse(data_consulta) >= Date.parse(hoje)) { 
		status = true;   
    } else {
    	document.getElementById("erro").innerHTML = "Por favor, corrija a data!";
    	status = false;  
    }
	    
	return status;  
} 
