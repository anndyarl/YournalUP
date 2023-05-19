// Variable para el calculo de lotaje
let riesgoPorOperacionInput = document.getElementById('riesgo_operacion');
// Variable para el calculo el riesgo
let cuentaInput = document.getElementById('cuenta');
let nOperacionesInput = document.getElementById('n_operaciones');
let capitalRiesgoInput = document.getElementById('capital_riesgo');
let operacionesRestantesInput = document.getElementById('operaciones_restantes');
let capitalActualInput = document.getElementById('capital_actual');
let nivelRiesgoInput = document.getElementById('nivel_riesgo');

//Calcular Riesgo
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
cuentaInput.addEventListener('input', calculateResultRiesgo);
nOperacionesInput.addEventListener('input', calculateResultRiesgo);

function calculateResultRiesgo() {
  let cuenta = parseFloat(cuentaInput.value);
  let nOperaciones = parseFloat(nOperacionesInput.value);

  // Validamos si existen datos dentro del input
  if (nOperaciones == 0 || isNaN(nOperaciones) || cuenta == 0 || isNaN(cuenta)) {
    nOperacionesInput.value = "";
    capitalRiesgoInput.value = "";  
    return;
  }
  let capitalRiesgo = cuenta / nOperaciones ;
  capitalRiesgoInput.value = capitalRiesgo.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
}
//Fin Calcular Riesgo

//Seleccionar % Riesgo
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
riesgoPorOperacionInput.addEventListener('input', seleccionarRiesgo);
capitalRiesgoInput.addEventListener('input', seleccionarRiesgo);
cuentaInput.addEventListener('input', seleccionarRiesgo);

function seleccionarRiesgo() {
  let PorcentajeRiesgo = parseFloat(riesgoPorOperacionInput.value);
  let capitalEnRiesgo = parseFloat(capitalRiesgoInput.value);
  let cuentaFondeo = parseFloat(cuentaInput.value);

  // Validamos selección de riesgo
  switch (PorcentajeRiesgo) {
    case 2:
    case 1:
    case 0.5:
    case 0.4:
    case 0.3:
    case 0.2:
    case 0.1:
      capitalEnRiesgo = (PorcentajeRiesgo / 100) * cuentaFondeo;
        // Validamos si existen datos dentro del input
  if (capitalEnRiesgo == 0 || isNaN(capitalEnRiesgo)) {
    capitalRiesgoInput.value = "";   
    return;
  }
      break;
    default:   
      capitalRiesgoInput.value = "";
      return;
  }
  capitalRiesgoInput.value = capitalEnRiesgo.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input

}
//Fin Seleccionar Riesgo

//Calcular  operaciones maximas a utilizar 
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
cuentaInput.addEventListener('input', calculateOperacionesRestantes);
riesgoPorOperacionInput.addEventListener('input', calculateOperacionesRestantes);
capitalRiesgoInput.addEventListener('input', calculateOperacionesRestantes);

function calculateOperacionesRestantes() {
  let cuenta = parseFloat(cuentaInput.value);
  let capitalRiesgo = parseFloat(capitalRiesgoInput.value);

  let nOperaciones = cuenta / 10 / capitalRiesgo;

    // Validamos si existen datos dentro del input
    if (nOperaciones == 0 || isNaN(nOperaciones)) {
      operacionesRestantesInput.value = "";     
      return;
    }
  nOperacionesInput.value = nOperaciones.toFixed(); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
  operacionesRestantesInput.value = nOperaciones.toFixed(); 
}
//Fin Calcular  operaciones maximas a utilizar 

//Seleccionar capital actual 
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
cuentaInput.addEventListener('input', seleccionarCuenta);

function seleccionarCuenta() {
  let cuenta = parseFloat(cuentaInput.value); 
  let capitalActual = 0;
// Validamos selección de riesgo
switch (cuenta) {
  case 200000:
  case 100000:
  case 50000:
  case 40000:
  case 25000:
  case 10000:  
  capitalActual =  cuenta;
    break;
  default:
    capitalActualInput.value = cuenta;
    nOperacionesInput.value = "";
    return;
}

capitalActualInput.value = capitalActual.toFixed();

}
//Fin Seleccionar capital actual 

//Seleccionar Nivel de riesgo 
riesgoPorOperacionInput.addEventListener('input', seleccionarNivelDeRiesgo);

function seleccionarNivelDeRiesgo() {
  const riesgoPorOperacion = parseFloat(riesgoPorOperacionInput.value);
  let nivelRiesgo = "";

  switch (riesgoPorOperacion) {
    case 2:
      nivelRiesgo = "Muy Riesgoso";
      break;
    case 1:
      nivelRiesgo = "Riesgoso";
      break;
    case 0.5:
      nivelRiesgo = "Optimo";
      break;
    case 0.4:
      nivelRiesgo = "Moderado";
      break;
    case 0.3:
      nivelRiesgo = "Muy Mamón";
      break;
    case 0.2:
      nivelRiesgo = "Mamonisimo";
      break;
    case 0.1:
      nivelRiesgo = "Ultra Mamón";
      break;
    default:
      nivelRiesgo = "";
      break;
  }

  nivelRiesgoInput.value = nivelRiesgo;
}

