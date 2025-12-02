

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



function validarRegistro(event) {
    document.getElementById('errorUser').innerHTML = '';
    document.getElementById('errorNom').innerHTML = '';
    document.getElementById('errorApe').innerHTML = '';
    document.getElementById('errorCode').innerHTML = '';
    document.getElementById('errorPass').innerHTML = '';
    document.getElementById('errorConf').innerHTML = '';

    let form = document.forms['registro']; 

    let user = form['usuario'].value;
    let nombre = form['nombre'].value;
    let apellido = form['apellido'].value;
    let code = document.getElementById('codigoFamiliar').value;
    let rol = form['select'].value;
    let contraseña = form['contrasenia'];  
    let confirmar = form['confirmar'];      

    let valido = true; 

    if (/[\d!@#$%^&*()_+\-=\[\]{};:"'\\|,.<>\/?~`]/.test(nombre)) {
        document.getElementById('errorNom').innerHTML = 'Ingrese solo letras';
        valido = false;
    }

    if (/[\d!@#$%^&*()_+\-=\[\]{};:"'\\|,.<>\/?~`]/.test(apellido)) {
        document.getElementById('errorApe').innerHTML = 'Ingrese solo letras';
        valido = false;
    }

    if (rol === 'hijo') {
        if (!/^\d{6}$/.test(code)) {
            document.getElementById('errorCode').innerHTML = 'Código de 6 dígitos (solo números)';
            valido = false;
        }
    }

    if (
        !/\d/.test(contraseña.value) || 
        !/[!@#$%^&*()_+\-=\[\]{};:"'\\|,.<>\/?~`]/.test(contraseña.value) ||
        contraseña.value.length < 6
    ) {
        document.getElementById('errorPass').innerHTML =
        'Incluya al menos un número, un caracter especial. Mínimo 6 caracteres.';
        valido = false;
    }

    if (contraseña.value !== confirmar.value) {
        document.getElementById('errorConf').innerHTML = 'Contraseñas no coinciden.';
        valido = false;
    }

    if (!valido) {                
        event.preventDefault();   
        return false;              
    }

    return true;                   
}


 
function Validarcamposlogin(event) {

    let form = document.forms['login'];   
    let user = form['usuario'];           
    let password = form['contraseña'];    

    document.getElementById('error_login_js').innerHTML = '';

    user.style.border = "2px solid #000852";
    password.style.border = "2px solid #000852";

    let valido = true;

    if (user.value.trim().length === 0 || password.value.trim().length === 0) {
        document.getElementById('error_login_js').innerHTML = 'Complete los campos';
        valido = false;

        if (user.value.trim().length === 0) {
            user.style.border = "2px solid #ff0000ff"; 
        }
        if (password.value.trim().length === 0) {
            password.style.border = "2px solid #ff0000ff"; 
        }
    }
    
    if (!valido) {            
        event.preventDefault();  
        return false;            
    }

    return true;                
}


function ValidarCamposTransferencia(event) {

    let form = document.forms['transferir'];          
    let userDestino = form['usuarioDestino'].value.trim();  
    let monto = parseFloat(form['monto'].value);            
    let motivo = form['motivo'].value.trim();               

    document.getElementById('error_transferir_js').innerHTML = '';

    let valido = true;   

    if (userDestino.length < 1 || isNaN(monto) || monto < 1 || motivo.length < 1) {
        document.getElementById('error_transferir_js').innerHTML = 'Complete los datos.';
        valido = false;   
    }

    if (!valido) {                   
        event.preventDefault();      
        return false;               
    }

    return true;                  
}


function ValidarCamposIngresar(event) {
    let form = document.forms['ingreso'];

    let montoStr = form['montoIngresar'].value.trim();
    let montoIngreso = parseFloat(montoStr);

    document.getElementById('error_ingresar_js').innerHTML = '';

    let valido = true;

    if (isNaN(montoIngreso) || montoIngreso < 1 || montoStr.length < 1) {
        document.getElementById('error_ingresar_js').innerHTML = 'Complete el monto';
        valido = false;   
    }

    if (!valido) {                   
        event.preventDefault();      
        return false;               
    }

    return true;    
}



function ValidarCamposSoicitar(event){
    let form = document.forms['solicitar'];

    let montoStr = form['montoSolicitar'].value.trim();
    let montoSolicitar = parseFloat(montoStr);

    document.getElementById('error_solicitar_js').innerHTML = ''
    let valido = true;

    if (isNaN(montoSolicitar) || montoSolicitar < 1 || montoStr.length < 1){
        document.getElementById('error_solicitar_js').innerHTML = 'Complete los datos';
        valido = false
    }
    if (!valido) {                   
        event.preventDefault();      
        return false;               
    }
    return true; 
}

function ValidarCamposQuitar(event){
    let form = document.forms['quitar'];

    let montoStr = form['montoQuitar'].value.trim();
    let montoQuitar = parseFloat(montoStr);

    document.getElementById('error_quitar_js').innerHTML = ''
    let valido = true;

    if (isNaN(montoQuitar) || montoQuitar < 1 || montoStr.length < 1){
        document.getElementById('error_quitar_js').innerHTML = 'Complete los datos';
        valido = false
    }
    if (!valido) {                   
        event.preventDefault();      
        return false;               
    }
    return true; 
}







