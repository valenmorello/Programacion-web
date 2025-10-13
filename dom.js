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

let eyeBtn = document.getElementById("eyeBtn");
let input = document.getElementById("confirmar");

eyeBtn.addEventListener("click", () => {
  if (input.type === "password" && password.type === 'password') {
    input.type = "text";
    password.type = "text";
    eyeBtn.textContent = "Ocultar contraseñas "; 
  } else {
    input.type = "password";
    password.type = "password"
    eyeBtn.textContent = "Visualizar contraseñas ";
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
    let carN = false
    let carA = false
    let nums = '0123456789'
    let esps = '/?.><,;:][}{=_-+*&^%$#@!~'
    let numEsps = '0123456789/?.><,;:][}{=_-+*&^%$#@!~'

    for (let i = 0; i < password.value.length; i++){
        for (let j = 0; j < nums.length; j++){
            if (password.value[i] == nums[j]){
                num = true
                console.log(num)
            } 
        }
        for (let k = 0; k < esps.length; k++){
            if (password.value[i] == esps[k]){
                esp = true
                console.log(esp)
            } 
        }
    }

    for (let i = 0; i < nombre.length; i++){
        for (let k = 0; k < numEsps.length; k++){
            if (nombre[i] == numEsps[k]){
                carN = true
            } 
        }
    }

    for (let i = 0; i < apellido.length; i++){
        for (let k = 0; k < numEsps.length; k++){
            if (apellido[i] == numEsps[k]){
                carA = true
            } 
        }
    }

    if (code.length != 6){
        alert('Ingrese codigo de 6 digitos')
    } else if (carA == true || carN == true){
        alert('Ingrese solo letras en Nombre, Apellido')
    } else if (num == false || esp == false || password.value.length <= 6){
        alert('Incluya al menos un número y un caracter especial. Minimo 6 caracteres.')
    } else if (num == true && esp == true && password.value == confirmación.value && code.length == 6){
        if(document.getElementById("usuario_select").value == "hijo"){
            alert(`Bienvenido, ${user}`)
            window.location.assign('inicio.html')
            localStorage.setItem('user', user)
        }
        else if (document.getElementById("usuario_select").value == "padre"){
            alert(`Bienvenido, ${user}`)
            window.location.assign('iniciopadre.html')
            localStorage.setItem('user', user)
            localStorage.setItem('code', code)
        }
    } else {
        alert('Contraseñas no coincidentes.')
    }
    
    
}

function loguearse (){
    let u = "minombre"
    let p = "contraseña123"

    let user = document.getElementById('usuario')
    let password = document.getElementById('contraseña')


    if (user.value == u && password.value == p){
        alert(`Bienvenido, ${user.value}`)
        window.location.assign('inicio.html')
        localStorage.setItem('user', user.value)
        }

    else if (user.value.length < 1 || password.value.length < 1){
            alert(`Completar campos`)
            if (user.value.length < 1){
                user.style.border =  "2px solid #ff0000ff";
            }
            if (password.value.length < 1){
                password.style.border =  "2px solid #ff0000ff";
            }
        }

    else if (user.value != u){
            alert(`No se encontro usuario`)

            user.value = ""
            password.value = ""

            user.style.border =  "2px solid #ff0000ff";
            password.style.border =  "2px solid #000852";
        }    

    else if (user.value == u && password.value != p){
            alert(`Contraseña Incorrecta`)

            password.value = ""

            user.style.border =  "2px solid #000852";
            password.style.border =  "2px solid #ff0000ff";
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
    window.location.assign('inicio.html')
}

function solicitud (){
    window.location.assign('solicitar.html')
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
  let montoIngreso = Number(document.getElementById("montoIngresar").value);
  let saldoTexto = document.getElementById("saldoActual").textContent;
  let nuevoSaldo = saldoActual + montoIngreso;
  document.getElementById("saldoActual").textContent = "$ " + nuevoSaldo;
}



function solicitarDinero (){
    let montoSolicitar = document.getElementById('montoSolicitar').value
    if (montoSolicitar != 0){
        alert("se ha solicitado el dinero")
    }else{
        alert("ingrese los datos")
    }
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