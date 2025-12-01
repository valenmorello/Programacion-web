let saldoActual = 0;

let contraseña = document.forms['registro']['contraseña']
let confirmar = document.forms['registro']['confirmar'];
let confirmarDiv = document.getElementById('confirm-container');
let eyeBtn = document.getElementById("eyeBtn");
let select = document.forms['registro']['select']
let codigo = document.forms['registro']['codigoFamiliar']

contraseña.addEventListener('input', function() {
    if (contraseña.value.length > 0) {
        confirmarDiv.style.display = 'block';
    } else {
        confirmarDiv.style.display = 'none';
    }
});

select.addEventListener('change', function() {
    const valor = select.value
    if (valor == 'hijo') {
        codigo.style.display = 'block';
    } else {
        codigo.style.display = 'none';
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
    document.getElementById('errorUser').innerHTML = '';
    document.getElementById('errorNom').innerHTML = '';
    document.getElementById('errorApe').innerHTML = '';
    document.getElementById('errorCode').innerHTML = '';
    document.getElementById('errorPass').innerHTML = '';
    document.getElementById('errorConf').innerHTML = '';

    let user = document.forms['registro']['usuario'].value
    let nombre = document.forms['registro']['nombre'].value
    let apellido = document.forms['registro']['apellido'].value
    let code = document.getElementById('codigoFamiliar').value
    let rol = document.forms['registro']['select'].value
    let imagen = document.forms['registro']['imagen'];


    let valido = true

    if (/[\d!@#$%^&*()_+\-=\[\]{};:"'\\|,.<>\/?~`]/.test(nombre)){
        document.getElementById('errorNom').innerHTML = 'Ingrese solo letras'
        valido = false
    }
    if (/[\d!@#$%^&*()_+\-=\[\]{};:"'\\|,.<>\/?~`]/.test(apellido)){
        document.getElementById('errorApe').innerHTML = 'Ingrese solo letras'
        valido = false
    }
    if (rol == 'hijo') {
        if (!/^\d{6}$/.test(code)) {
            document.getElementById('errorCode').innerHTML = 'Código de 6 dígitos (solo números)';
            valido = false;
        }
    }
    if (!/\d/.test(contraseña.value) || !/[!@#$%^&*()_+\-=\[\]{};:"'\\|,.<>\/?~`]/.test(contraseña.value) || !/.{6,}/.test(contraseña.value)){
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
        localStorage.setItem('user', user)            
        localStorage.setItem('code', code)
        localStorage.setItem('padre', false)
        return true
    }
    else if (document.forms['registro']['select'].value == "padre"){        
        localStorage.setItem('user', user)
        localStorage.setItem('code', code)            
        localStorage.setItem('padre', true)
        return true

    }
}

function validarAdmision(admitido){
    document.getElementById('errorAdmision').innerHTML = '';

    if (admitido == 1){
        window.location.replace('/inicio')
    } else {
        document.getElementById('errorAdmision').innerHTML = 'Su usuario todavia no ha sido admitido.'
       
    }
}

 
function loguearse (event){
    if (event) event.preventDefault()

    let user = document.forms['login']['usuario']
    let password = document.forms['login']['contraseña']
    /*document.getElementById('errorUser').innerHTML = '';
    document.getElementById('errorPass').innerHTML = '';
    document.getElementById('login').innerHTML = ''*/
    user.style.border =  "2px solid #000852"
    password.style.border =  "2px solid #000852"

    let valido = true

    console.log(user, password)
    if (!/.{1.}/.test(user.value) || !/.{1.}/.test(password.value)){
        document.getElementById('login').innerHTML = 'Complete los campos'
        valido = false
        if (user.value.length < 1){
            user.style.border =  "2px solid #ff0000ff";            
        }
        if (password.value.length < 1){
            password.style.border =  "2px solid #ff0000ff";            
        }
    }

}

function inicio (){
    if (localStorage.getItem('padre') === 'true'){
        window.location.assign('iniciopadre.html')
    } else {
        window.location.assign('inicio.html')
    }
    
}


function validarTransferencia(event) {
  if (event) event.preventDefault();
  let userDestino = document.forms['transferir']['usuarioDestino'].value;
  let monto = parseFloat(document.forms['transferir']['monto'].value)
  let motivo = document.forms['transferir']['motivo'].value
  document.getElementById('transferir').innerHTML = ''

  if (userDestino.length < 1 || monto < 1 || motivo.length < 1) {
    document.getElementById('transferir').innerHTML = 'Complete los datos.'
  } else {
    document.getElementById('transferir').innerHTML = 'Transferencia exitosa!'
  }
}

function ingresar(event) {
  if (event) event.preventDefault();
  let montoIngreso = parseFloat(document.forms['ingreso']['montoIngresar'].value)
  //let saldoActual = parseInt(document.getElementById('saldoActual').value)
  //let nuevoSaldo = saldoActual + montoIngreso;
  let saldoActual = 0
  document.getElementById('ingresar').innerHTML = ''
  if (montoIngreso >= 1){
    document.getElementById('ingresar').innerHTML = 'Se ha ingresado el dinero!'
    saldoActual += montoIngreso
    document.getElementById('saldoActual').innerHTML = "$ " + saldoActual;
   
  } else {
    document.getElementById('ingresar').innerHTML = 'Complete el monto!'
  }
}


/*
function solicitarDinero (event){
    document.getElementById('solicitar').innerHTML = ''
    if (event) event.preventDefault();
    let montoSolicitar = document.forms['solicitar']['montoSolicitar'].value
    if (montoSolicitar >= 1){
        document.getElementById('solicitar').innerHTML = 'Se ha solicitado el dinero!'
    }else{
        document.getElementById('solicitar').innerHTML = 'Complete los datos!'
    }
}

function aceptarSolicitudGrupo (){    
    document.getElementById('solicitudGrupo').innerHTML = ''
    document.getElementById('solicitudGrupo').innerHTML = 'Se ha aceptado la solicitud! ✅'
    document.getElementById('botonAceptar').style.display = 'none';
    document.getElementById('botonRechazar').style.display = 'none';
}

function rechazarSolicitudGrupo (){    
    document.getElementById('solicitudGrupo').innerHTML = ''
    document.getElementById('solicitudGrupo').innerHTML = 'Se ha rechazado la solicitud! ❌'
    document.getElementById('botonAceptar').style.display = 'none';
    document.getElementById('botonRechazar').style.display = 'none';
}
*/
function aceptarTransferencia (){    
    document.getElementById('solicitudTransferencia').innerHTML = ''
    document.getElementById('solicitudTransferencia').innerHTML = 'Se ha transferido el dinero! ✅'
    document.getElementById('aceptarTransferencia').style.display = 'none';
    document.getElementById('rechazarTransferencia').style.display = 'none';
}

function rechazarTransferencia (){    
    document.getElementById('solicitudTransferencia').innerHTML = ''
    document.getElementById('solicitudTransferencia').innerHTML = 'Se ha rechazado la transferencia! ❌'
    document.getElementById('aceptarTransferencia').style.display = 'none';
    document.getElementById('rechazarTransferencia').style.display = 'none';
}
/*
function quitar (){
    window.location.assign('quitar.html')
}

function quitarDinero (event){
    document.getElementById('quitar').innerHTML = ''
    if (event) event.preventDefault();
    let quitar = document.forms['quitar']['montoQuitar'].value
    if (quitar >= 1){
        document.getElementById('quitar').innerHTML = 'Dinero quitado!'
        return true
    } else {
        document.getElementById('quitar').innerHTML = 'Complete el campo!'
        return false
    }
}*/

function cerrarSesion (){
    window.location.replace('index.html')
    localStorage.removeItem('user')
    localStorage.removeItem('code')
}

/*
function validarModificaciones (event){
    if (event) event.preventDefault();
    let nombreNew = document.forms['datos']['nombreNuevo'].value;
    let apNew = document.forms['datos']['apellidoNuevo'].value;
    document.getElementById('cambioDatos').innerHTML = ''

    modificarUser(nombreNew, apNew);
}

function modificarUser (nombreNew, apNew){
    
    if (nombreNew == "" && apNew != ""){
        document.getElementById('cambioDatos').innerHTML = 'Usted ha modificado su apellido!'
        return true
    }
    else if (apNew == "" && nombreNew != ""){
        document.getElementById('cambioDatos').innerHTML = 'Usted ha modificado su nombre!'
        return true
    }
    else if (apNew != "" && nombreNew != ""){
        document.getElementById('cambioDatos').innerHTML = 'Usted ha modificado su nombre y apellido!'
        return true
    } else {
        return false
    }
}
*/

function hijo(){
    window.location.assign('padre2.html')
}
function aIngresar(){
    window.location.assign("ingresar.html")
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