let saldoActual = 0;
function registrarse (){
    window.location.assign('registro.html')
}

function registro (){
    let user = document.getElementById('usuario').value
    let nombre = document.getElementById('nombre').value
    let apellido = document.getElementById('apellido').value
    let password = document.getElementById('contraseña').value
    let code = document.getElementById('codigoFamiliar').value
    usuarioGuardado={user,nombre,apellido,password,code}
    alert(`Bienvenido, ${user}`)
    window.location.assign('inicio.html')
    localStorage.setItem('user', user)
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

function transferirDinero (){
    let userDestino = document.getElementById('usuarioDestino').value
    let montoTransferir = document.getElementById('monto').value
    let userEmisor=document.getElementById("usuarioEmisor").value
    

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