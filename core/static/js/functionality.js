
window.onload = function() {
    var cpf = document.getElementById("cpf"),
        user = document.getElementById("username");
    cpf.addEventListener('input', function() {
        user.value = cpf.value;
    });
};
