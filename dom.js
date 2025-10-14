let saldoActual = 0;
function registrarse (){
    window.location.assign('registro.html')
}

let contraseña = document.forms['registro']['contraseña']
let confirmar = document.forms['registro']['confirmar'];
let confirmarDiv = document.getElementById('confirm-container');
let eyeBtn = document.getElementById("eyeBtn");

contraseña.addEventListener('input', function() {
    if (contraseña.value.length > 0) {
        confirmarDiv.style.display = 'block';
    } else {
        confirmarDiv.style.display = 'none';
    }
});


eyeBtn.addEventListener("click", () => {
  if (confirmar.type === "password" && contraseña.type === 'password') {
    confirmar.type = "text";
    contraseña.type = "text";
    eyeBtn.textContent = "Ocultar contraseñas"; 
  } else {
    confirmar.type = "password";
    contraseña.type = "password"
    eyeBtn.textContent = "Visualizar contraseñas";
  }
});

function validarRegistro (event){
    if (event) event.preventDefault();
    let num = false
    let esp = false
    let carN = false
    let carA = false
    let nums = '0123456789'
    let esps = '/?.><,;:][}{=_-+*&^%$#@!~'
    let numEsps = '0123456789/?.><,;:][}{=_-+*&^%$#@!~'
    document.getElementById('errorUser').innerHTML = '';
    document.getElementById('errorNom').innerHTML = '';
    document.getElementById('errorApe').innerHTML = '';
    document.getElementById('errorCode').innerHTML = '';
    document.getElementById('errorPass').innerHTML = '';
    document.getElementById('errorConf').innerHTML = '';

    let user = document.forms['registro']['usuario'].value
    let nombre = document.forms['registro']['nombre'].value
    for (let i = 0; i < nombre.length; i++){
        for (let k = 0; k < numEsps.length; k++){
            if (nombre[i] == numEsps[k]){
                carN = true
            } 
        }
    }

    let apellido = document.forms['registro']['apellido'].value
    for (let i = 0; i < apellido.length; i++){
        for (let k = 0; k < numEsps.length; k++){
            if (apellido[i] == numEsps[k]){
                carA = true
            } 
        }
    }

    let code = document.getElementById('codigoFamiliar').value

    for (let i = 0; i < contraseña.value.length; i++){
        for (let j = 0; j < nums.length; j++){
            if (contraseña.value[i] == nums[j]){
                num = true
            } 
        }
        for (let k = 0; k < esps.length; k++){
            if (contraseña.value[i] == esps[k]){
                esp = true
            } 
        }
    }

    let valido = true

    if (user == 'existe'){
        document.getElementById('errorUser').innerHTML = 'Usuario existente'
        valido = false
    }
    if (carN == true){
        document.getElementById('errorNom').innerHTML = 'Ingrese solo letras'
        valido = false
    }
    if (carA == true){
        document.getElementById('errorApe').innerHTML = 'Ingrese solo letras'
        valido = false
    }
    if (code.length != 6){
        document.getElementById('errorCode').innerHTML = 'Codigo de 6 digitos'
        valido = false
    }
    if (num == false || esp == false || contraseña.value.length < 6){
        document.getElementById('errorPass').innerHTML = 'Incluya al menos un número y un caracter especial. Minimo 6 caracteres.'
        valido = false
    }
    if (contraseña.value != confirmar.value) {
        document.getElementById('errorConf').innerHTML = 'Contraseñas no coincidentes.'
        valido = false
    }
    if (valido != true){
        return false
    }

    if(document.forms['registro']['select'].value == "hijo"){
        alert(`Bienvenido, ${user}`)
        window.location.assign('inicio.html')
        localStorage.setItem('user', user)            
        localStorage.setItem('code', code)
        localStorage.setItem('padre', false)
        return true
    }
    else if (document.forms['registro']['select'].value == "padre"){
        alert(`Bienvenido, ${user}`)            
        window.location.assign('iniciopadre.html')
        localStorage.setItem('user', user)
        localStorage.setItem('code', code)            
        localStorage.setItem('padre', true)
        return true

    }
}


function loguearse (event){
    if (event) event.preventDefault()
    let u = "minombre"
    let p = "contraseña123"

    let user = document.forms['login']['usuario']
    let password = document.forms['login']['contraseña']
    document.getElementById('errorUser').innerHTML = '';
    document.getElementById('errorPass').innerHTML = '';
    user.style.border =  "2px solid #000852"
    password.style.border =  "2px solid #000852"

    let valido = true

    console.log(user, password)
    if (user.value.length < 1 || password.value.length < 1){
        alert(`Completar campos`)
        valido = false
        if (user.value.length < 1){
            user.style.border =  "2px solid #ff0000ff";            
        }
        if (password.value.length < 1){
            password.style.border =  "2px solid #ff0000ff";            
        }
    }

    if (user.value != u){
        document.getElementById('errorUser').innerHTML = 'Usuario no existente'
        valido = false
        user.value = ""
        password.value = ""
        user.style.border =  "2px solid #ff0000ff";
        password.style.border =  "2px solid #000852";
    } 
    else if (user.value == u && password.value != p){
        document.getElementById('errorPass').innerHTML = 'Contraseña incorrecta.'
        valido = false
        password.value = ""
        user.style.border =  "2px solid #000852";
        password.style.border =  "2px solid #ff0000ff";     
    }

    if (valido != true){
        return false
    }

    if (user.value == u && password.value == p){
        alert(`Bienvenido, ${user.value}`)
        window.location.assign('inicio.html')
        localStorage.setItem('user', user.value)
        return true
    }

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

function inicio (){
    if (localStorage.getItem('padre') === 'true'){
        window.location.assign('iniciopadre.html')
    } else {
        window.location.assign('inicio.html')
    }
    
}

function solicitud (){
    window.location.assign('solicitar.html')
}

function validarTransferencia() {
  let userDestino = document.forms['transferir']['usuarioDestino'].value;
  let monto = parseFloat(document.forms['transferir']['monto'].value)
  let motivo = document.forms['transferir']['motivo'].value

  if (userDestino.length < 1 || monto < 1 || motivo.length < 1) {
    alert('Complete los datos!');
    return false
  } else {
    transferirDinero(userDestino, monto, motivo);
    return true
  }
}

function transferirDinero (userDestino, monto, motivo){
    alert(`Transferencia exitosa!`)
}

function ingresar(event) {
  if (event) event.preventDefault();
  let montoIngreso = parseFloat(document.forms['ingresar']['montoIngresar'].value)
  let saldoActual = document.getElementById('saldoActual')
  //let nuevoSaldo = saldoActual + montoIngreso;
  document.getElementById('saldoActual').innerHTML = "$ " + montoIngreso;

  if (montoIngreso > 0){
    alert('Se ha ingresado el dinero!')
    return true
  } else {
    alert('Complete el monto!')
    return false
  }
}



function solicitarDinero (event){
    if (event) event.preventDefault();
    let montoSolicitar = document.forms['solicitar']['montoSolicitar'].value
    if (montoSolicitar != 0){
        alert("Se ha solicitado el dinero!")
    }else{
        alert("Ingrese los datos")
    }
}

function quitar (){
    window.location.assign('quitar.html')
}

function quitarDinero (event){
    if (event) event.preventDefault();
    let quitar = document.forms['quitar']['montoQuitar'].value
    if (quitar > 0){
        alert('Dinero quitado!')
        return true
    } else {
        alert('Complete el campo!')
        return false
    }
}

function cerrarSesion (){
    window.location.assign('index.html')
    localStorage.removeItem('user')
}

function validarModificaciones (event){
    if (event) event.preventDefault();
    let nombreNew = document.forms['datos']['nombreNuevo'].value;
    let apNew = document.forms['datos']['apellidoNuevo'].value;

    modificarUser(nombreNew, apNew);
}

function modificarUser (nombreNew, apNew){
    
    if (nombreNew == "" && apNew != ""){
        alert(`Usted ha modificado su Apellido`)
        return true
    }
    else if (apNew == "" && nombreNew != ""){
        alert(`Usted ha modificado su Nombre`)
        return true
    }
    else if (apNew != "" && nombreNew != ""){
        alert(`Usted ha modificado su Nombre y Apellido`)
        return true
    } else {
        return false
    }
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

function cargarCodigo (){
    let codePag = document.getElementById('code')
    codePag.innerHTML = `#${localStorage.getItem('code')}`
}

function cargarDatos (){
    let codePag = document.getElementById('datosCode')
    let nombrePag = document.getElementById('datosUser')
    codePag.innerHTML = `#${localStorage.getItem('code')}`
    nombrePag.innerHTML = `Hola, ${localStorage.getItem('user')}!`

}