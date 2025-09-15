function registrarse (){
    let user = document.getElementById('usuario').value
    let password = document.getElementById('contraseña').value
    let code = document.getElementById('codigoFamiliar').value
    
    alert(`Bienvenido, ${user}`)
    window.location.assign('registro.html')
}

function loguearse (){
    let user = document.getElementById('usuario').value
    let password = document.getElementById('contraseña').value
    
    alert(`Bienvenido, ${user}`)
    window.location.assign('inicio.html')
}

function actividad (){
    window.location.assign('actividad.html')
}

function cuenta (){
    let newUser = document.getElementById('usuarioNuevo').value
    let newPassword = document.getElementById('contraseñaNueva').value

    window.location.assign('cuenta.html')
}

function transferencia (){
    let userDestino = document.getElementById('usuarioDestino').value
    let monto = document.getElementById('monto').value

    window.location.assign('transferir.html')
}

function inicio (){
    window.location.assign('inicio.html')
}

function solicitar (){
    let montoSolicitar = document.getElementById('montoSolicitar').value

    window.location.assign('solicitar.html')
}

function quitar (){
    window.location.assign('quitar.html')
}

function cerrarSesion (){
    window.location.assign('index.html')
}

function hijo(){
    window.location.assign('padre2.html')
}