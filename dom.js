function registrarse (){
    window.location.assign('registro.html')
}

function registro (){
    let user = document.getElementById('usuario').value
    let nombre = document.getElementById('nombre').value
    let apellido = document.getElementById('apellido').value
    let code = document.getElementById('codigoFamiliar').value
    let password = document.getElementById('contraseña').value
    
    alert(`Bienvenido, ${user}`)
    window.location.assign('inicio.html')
    localStorage.setItem('user', user)
}

function loguearse (){
    let user = document.getElementById('usuario').value
    let password = document.getElementById('contraseña').value

    alert(`Bienvenido, ${user}`)
    window.location.assign('inicio.html')
    localStorage.setItem('user', user)
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

    if (nombreNew.length < 5 || apNew.length < 1 || passNew.length < 1) {
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

function cargarNombre (){
    let nombrePag = document.getElementById('cuenta')
    nombrePag.innerHTML = `Hola, ${localStorage.getItem('user')}!`
}