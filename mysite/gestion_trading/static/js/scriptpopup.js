// Variable para los botones
 const agregarBtn = document.getElementById("agregar-btn");
// const cerrarBtn = document.getElementById("cerrar-btn");
const popup = document.getElementById("popup");
const gridItems = document.querySelectorAll(".grid-item");
// Variable para el calculo de lotaje
let riesgoPorOperacionInput = document.getElementById('riesgoPorOperacion');
let stoplossInput = document.getElementById('stoploss');
let lotajeInput = document.getElementById('lotaje');
// Variable para el calculo el riesgo
let cuentaInput = document.getElementById('cuenta');
let nOperacionesInput = document.getElementById('nOperaciones');
let capitalRiesgoInput = document.getElementById('capitalRiesgo');

let ratioInput = document.getElementById('ratio');
let takeprofitInput = document.getElementById('takeprofit');
let BeneficioEsperadoInput = document.getElementById('beneficioEsperado');
let utilidadProyectadaInput = document.getElementById('utilidadProyectada');


//Boton "Nueva Orden" para abrir pop up
// agregarBtn.addEventListener('click', function () {
//   popup.classList.remove('hidden');
// });

//Boton "Nueva Orden" para abrir pop up
// cerrarBtn.addEventListener('click', function () {
//   popup.classList.add('hidden');
// });


//Aun no se que hace
gridItems.forEach(function (item) {
  item.addEventListener("click", function () {
    if (!item.classList.contains("editable")) {
      item.classList.add("selected");
    }
  });

  item.addEventListener("dblclick", function () {
    item.classList.add("editable");
  });
});
//Fin Aun no se que hace



//Calcular Lotaje
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
capitalRiesgoInput.addEventListener('input', calculateResult);
stoplossInput.addEventListener('input', calculateResult);

function calculateResult() {
  let capitalRiesgo = parseFloat(capitalRiesgoInput.value);
  let stoploss = parseFloat(stoplossInput.value);

  // Validamos si existen datos dentro del input
  if (stoploss == 0 || isNaN(stoploss) ) {
    lotajeInput.value = "";
    return;
  }

  const lotaje = capitalRiesgo / stoploss / 10.66;
  lotajeInput.value = lotaje.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
}
//Fin Calcular Lotaje


//Calcular Riesgo
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
cuentaInput.addEventListener('input', calculateResultRiesgo);
nOperacionesInput.addEventListener('input', calculateResultRiesgo);

function calculateResultRiesgo() {
  let cuenta = parseFloat(cuentaInput.value);
  let noperaciones = parseFloat(nOperacionesInput.value);

  // Validamos si existen datos dentro del input
  if (noperaciones === 0) {
    cuentaInput.value = 'Error';
    return;
  }
  let capitalRiesgo = cuenta / noperaciones / 10;
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
      break;
    default:
      capitalRiesgoInput.value = "Error";
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
  nOperacionesInput.value = nOperaciones.toFixed(); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
}
//Fin Calcular  operaciones maximas a utilizar 


//Calcular  ratio reisgo/beneficio
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real

stoplossInput.addEventListener('input', calculateRatio);
takeprofitInput.addEventListener('input', calculateRatio);

function calculateRatio() {
  let stoplost = parseFloat(stoplossInput.value);
  let takeprofit = parseFloat(takeprofitInput.value);

  // Validamos si existen datos dentro del input
  if (stoplost == 0 || isNaN(stoplost) || takeprofit == 0 || isNaN(takeprofit)) {
    ratioInput.value = "";
    return;
  }
  let ratio = takeprofit / stoplost;
  ratioInput.value = "1 / " + ratio.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
}
//Fin Calcular ratio reisgo/beneficio

//Calcular  Beneficio Esperado
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
lotajeInput.addEventListener('input', calculateBeneficioEsperado);
takeprofitInput.addEventListener('input', calculateBeneficioEsperado);
BeneficioEsperadoInput.addEventListener('input', calculateBeneficioEsperado);

function calculateBeneficioEsperado() {
  let lotaje = parseFloat(lotajeInput.value);
  let takeprofit = parseFloat(takeprofitInput.value);

  // Validamos si existen datos dentro del input
  if (takeprofit == 0 || isNaN(takeprofit)) {
    BeneficioEsperadoInput.value = "";
    return;
  }
  let beneficio = lotaje *  10.66 * takeprofit;
  BeneficioEsperadoInput.value = "$ " + beneficio.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
  calculateUtilidadProyectada();
}
//Fin Calcular Beneficio Esperado


//Calcular  utilidad proyectada
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real

cuentaInput.addEventListener('input', calculateUtilidadProyectada);
BeneficioEsperadoInput.addEventListener('input', calculateUtilidadProyectada);
stoplossInput.addEventListener('input', calculateUtilidadProyectada);
takeprofitInput.addEventListener('input', calculateUtilidadProyectada);

function calculateUtilidadProyectada() {
  BeneficioEsperadoInput.value = BeneficioEsperadoInput.value.replace(/[^\d.-]/g, '');
  let BeneficioEsperado = parseFloat(BeneficioEsperadoInput.value);
  let cuenta = parseFloat(cuentaInput.value);
  let stoplost = parseFloat(stoplossInput.value);
  let takeprofit = parseFloat(takeprofitInput.value);

    // Validamos si existen datos dentro del inputs
  if (stoplost == 0 || isNaN(stoplost) || takeprofit == 0 || isNaN(takeprofit)) {
    utilidadProyectadaInput.value = "";
    return;
  }

  let utilidadProyectada = BeneficioEsperado * 100 / cuenta;
  utilidadProyectadaInput.value = utilidadProyectada.toFixed(2) + " %"; // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
  BeneficioEsperadoInput.value = "$ " + BeneficioEsperado.toFixed(2);
}
//Fin Calcular utilidad proyectada

// Obtener elementos del DOM
var modal = document.getElementById("myModal");
var btn = document.getElementById("myBtn");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

span.onclick = function() {
  modal.style.display = "none";
}

//Valida campos antes de enviarlo a la bd
$('#takeprofit').on('input', function() {
    $('#takeprofit-error').text('');
});

$('#stoploss').on('input', function() {
    $('#stoploss-error').text('');
});

$('form').submit(function(event) {
    // Detiene el envío del formulario
    event.preventDefault();

    // Valida los campos del formulario
    var activo = $('#activo').val();
    var orden = $('#orden').val();
    var stoploss = $('#stoploss').val();
    var takeprofit = $('#takeprofit').val();

    // Validación del campo "activo"
    if (activo.trim() === '') {
        alert('Por favor ingrese un activo válido');
        return false;
    }

    // Validación del campo "orden"
    if (orden !== 'compra' && orden !== 'venta') {
        alert('Por favor seleccione una orden válida');
        return false;
    }

    // Validación del campo "stoploss"
    if (isNaN(stoploss) || stoploss <= 0) {
        $('#stoploss-error').text('ingrese valor');
        return false;
    }

    // Validación del campo "takeprofit"
    if (isNaN(takeprofit) || takeprofit <= 0) {
        $('#takeprofit-error').text('Ingrese valor');
        return false;
    }

    // Si todos los campos son válidos, envía el formulario
    $('form').off('submit').submit();
})






