// Variable para el calculo de lotaje
let riesgoPorOperacionInput = document.getElementById('riesgo_operacion');
// Variable para el calculo el riesgo
let cuentaInput = document.getElementById('cuenta');
let nOperacionesInput = document.getElementById('n_operaciones');
let capitalRiesgoInput = document.getElementById('capital_riesgo');
let operacionesRestantesInput = document.getElementById('operaciones_restantes');
let capitalActualInput = document.getElementById('capital_actual');
let nivelRiesgoInput = document.getElementById('nivel_riesgo');
let nloginInput = document.getElementById('n_login');

// Calcular Riesgo

// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
cuentaInput.addEventListener('input', calculateResultRiesgo);
nOperacionesInput.addEventListener('input', calculateResultRiesgo);
riesgoPorOperacionInput.addEventListener('input', calculateResultRiesgo);
nloginInput.addEventListener('input', calculateResultRiesgo);

//Calcular Riesgo
function calculateResultRiesgo() {
  cuentaInput.value = cuentaInput.value.replace(/[^\d.-]/g, '');
  nloginInput.value = nloginInput.value.replace(/[^\d.-]/g, '');
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
  //sacar porcentaje de riesgo 
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


//Calcular número de operaciones recomendadas 
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
cuentaInput.addEventListener('input', calculateNoperaciones);
riesgoPorOperacionInput.addEventListener('input', calculateNoperaciones);
capitalRiesgoInput.addEventListener('input', calculateNoperaciones);

function calculateNoperaciones() {
  let cuenta = parseFloat(cuentaInput.value);
  let capitalRiesgo = parseFloat(capitalRiesgoInput.value);

  let nOperaciones = cuenta / 10 / capitalRiesgo;

    // Validamos si existen datos dentro del input
    if (nOperaciones == 0 || isNaN(nOperaciones)) {
      nOperacionesInput.value = "";        
      return;
    }
  nOperacionesInput.value = nOperaciones.toFixed(); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
 
}
//Fin Calcular  operaciones maximas a utilizar 


$(document).ready(function() {
  // Abrir el modal al hacer clic en el botón de ayuda
  $("#open-modal-help").click(function() {
    $('#modalayuda').modal('show');
  });

  // Cerrar el modal al hacer clic en el botón de cierre
  $("#modalayuda .close").click(function() {
    $('#modalayuda').modal('hide');
  });
});


document.addEventListener('DOMContentLoaded', function() {
  var selectBroker = document.getElementById('broker');
  var otroBrokerField = document.getElementById('otroBrokerField');

  // Restaurar el estado del campo "otro_broker" desde localStorage
  var otroBrokerSelected = localStorage.getItem('otroBrokerSelected') === 'true';
  if (otroBrokerSelected) {
    selectBroker.value = 'Otro';
    otroBrokerField.style.display = 'block';
  }

  selectBroker.addEventListener('change', function() {
    if (selectBroker.value === 'Otro') {
      otroBrokerField.style.display = 'block';
      // Guardar el estado del campo "otro_broker" en localStorage
      localStorage.setItem('otroBrokerSelected', 'true');
    } else {
      otroBrokerField.style.display = 'none';
      // Eliminar el estado del campo "otro_broker" en localStorage
      localStorage.removeItem('otroBrokerSelected');
    }
  });
});



