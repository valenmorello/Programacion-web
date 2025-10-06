let saldoActual = 0;
function registrarse (){
    window.location.assign('registro.html')
}

let password = document.getElementById('contraseña');
let confirmarDiv = document.getElementById('confirm-container');

password.addEventListener('input', function() {
    if (password.value.length > 0) {
        confirmarDiv.style.display = 'block';
    } else {
        confirmarDiv.style.display = 'none';
    }
});

function registro (){
    let user = document.getElementById('usuario').value
    let nombre = document.getElementById('nombre').value
    let apellido = document.getElementById('apellido').value
    let code = document.getElementById('codigoFamiliar').value
    let confirmación = document.getElementById('confirmar');

    let num = false
    let esp = false
    let nums = '0123456789'
    let esps = '/?.><,;:][}{=_-+*&^%$#@!~'

    for (let i = 0; i < password.value.length; i++){
        for (let j = 0; j < nums.length; j++){
            console.log(password.value[i], nums[j])
            if (password.value[i] == nums[j]){
                num = true
                console.log(num)
            } 
        }
        for (let k = 0; k < nums.length; k++){
            console.log(password.value[i], esps[k])
            if (password.value[i] == esps[k]){
                esp = true
                console.log(esp)
            } 
        }
    }

    if (code.length != 6){
        alert('Ingrese codigo de 6 digitos')
    } else if (num == false || esp == false){
        alert('Incluya al menos un número y un caracter especial.')
    } else if (num == true && esp == true && password.value == confirmación.value && code.length == 6){
        alert(`Bienvenido, ${user}`)
        window.location.assign('inicio.html')
        localStorage.setItem('user', user)
    } else {
        alert('Contraseñas no coincidentes.')
    }
    
    
}

function loguearse (){
    let user = document.getElementById('usuario').value
    let password = document.getElementById('contraseña').value

}

function actividad (){
    window.location.assign('actividad.html')
}

function cuenta (){
    window.location.assign('cuenta.html')
}

function editar (){
    let newUser = document.getElementById('usuarioNuevo').value
    let newPassword = document.getElementById('contraseñaNueva').value
}

function transferencia (){
    window.location.assign('transferir.html')
}

function validarTransferencia() {
  let userDestino = document.getElementById('usuarioDestino').value.trim();
  let monto = parseFloat(document.getElementById('monto').value);
  let motivo = document.getElementById('motivo').value.trim();

  if (userDestino.length < 5 || monto < 1 || motivo.length < 1) {
    alert('Complete los datos!');
  } else {
    transferirDinero(userDestino, monto, motivo);
  }
}

function transferirDinero (userDestino, monto, motivo){
    alert(`Transferencia exitosa!`)
}

function ingresar() {
  let montoIngreso = parseFloat(document.getElementById("montoIngresar").value);
  let saldoTexto = document.getElementById("saldoActual").textContent;
  let saldoActual = parseFloat(saldoTexto.replace("$", "").trim());
  let nuevoSaldo = saldoActual + montoIngreso;
  document.getElementById("saldoActual").textContent = `$ ${nuevoSaldo.toFixed(2)}`;
}

function inicio (){
    window.location.assign('inicio.html')
}

function solicitud (){
    window.location.assign('solicitar.html')
}

function solicitarDinero (){
    let montoSolicitar = document.getElementById('montoSolicitar').value
}

function quitar (){
    window.location.assign('quitar.html')
}

function cerrarSesion (){
    window.location.assign('index.html')
    localStorage.removeItem('user')
}

function validarModificaciones (){
    let nombreNew = document.getElementById('nombreNuevo').value.trim();
    let apNew = parseFloat(document.getElementById('apellidoNuevo').value);
    let passNew = document.getElementById('contraseñaNueva').value.trim();

    if (nombreNew.length < 1 || apNew.length < 1 || passNew.length < 1) {
        alert('Complete los datos!');
    } else {
        modificarUser(nombreNew, apNew, passNew);
    }
}

function modificarUser (nombreNew, apNew, passNew){
    alert(`Modificacion exitosa!`)
}


function hijo(){
    window.location.assign('padre2.html')
}
function aingresar(){
    window.location.assign("ingresar.html")
}

function cargarNombre (){
    let nombrePag = document.getElementById('cuenta')
    nombrePag.innerHTML = `Hola, ${localStorage.getItem('user')}!`
}