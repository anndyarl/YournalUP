
// Variable para el calculo de lotaje
let riesgoPorOperacionInput = document.getElementById('riesgo_operacion');
// Variable para el calculo el riesgo
let cuentaInput = document.getElementById('cuenta');
let nOperacionesInput = document.getElementById('n_operaciones');
let capitalRiesgoInput = document.getElementById('capital_riesgo');
// let operacionesRestantesInput = document.getElementById('operaciones_restantes');
// let capitalActualInput = document.getElementById('capital_actual');
let nivelRiesgoInput = document.getElementById('nivel_riesgo');
let nloginInput = document.getElementById('n_login');


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
      // capitalActualInput.value = "";
      operacionesRestantesInput.value = "";
      riesgoPorOperacionInput.value = "";
      return;
    }
    // capitalActualInput.value = cuenta.toFixed(2);
    // operacionesRestantesInput.value = nOperaciones;
    let capitalRiesgo = cuenta / nOperaciones ;
    capitalRiesgoInput.value = capitalRiesgo.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
    //sacar porcentaje de riesgo
    let porcentajeRiesgo = capitalRiesgo * 100 / cuenta;
    riesgoPorOperacionInput.value = porcentajeRiesgo.toFixed(1);
    
  }
  //Fin Calcular Riesgo

  document.addEventListener('DOMContentLoaded', function() {
    var selectBroker = document.getElementById('broker');
    var otroBrokerField = document.getElementById('otroBrokerField');
  
    selectBroker.addEventListener('change', function() {
      if (selectBroker.value === 'Otro') {
        otroBrokerField.style.display = 'block';
      } else {
        otroBrokerField.style.display = 'none';
      }
    });
  
    // Mostrar u ocultar el campo "otro_broker" al cargar la página
    if (selectBroker.value === 'otro') {
      otroBrokerField.style.display = 'block';
    } else {
      otroBrokerField.style.display = 'none';
    }
  });
  