// Variable para los botones
//  const agregarBtn = document.getElementById("agregar-btn");
// const cerrarBtn = document.getElementById("cerrar-btn");
// const popup = document.getElementById("popup");
// const gridItems = document.querySelectorAll(".grid-item");
// Variable para el calculo de lotaje
let riesgoPorOperacionInput = document.getElementById('riesgo_operacion');
let stoplossInput = document.getElementById('stoploss');
let lotajeInput = document.getElementById('lotaje');
// Variable para el calculo el riesgo
let cuentaInput = document.getElementById('cuenta');
let nOperacionesInput = document.getElementById('n_operaciones');
let capitalRiesgoInput = document.getElementById('capital_riesgo');

let ratioInput = document.getElementById('ratio');
let takeprofitInput = document.getElementById('takeprofit');
let BeneficioEsperadoInput = document.getElementById('beneficio_esperado');
let utilidadProyectadaInput = document.getElementById('utilidad_proyectada');
let BeneficioRealInput = document.getElementById('beneficio_real');
let porcentajeBeneficioRealInput = document.getElementById('porcentaje_beneficio_real');


//Aun no se que hace
// gridItems.forEach(function (item) {
//   item.addEventListener("click", function () {
//     if (!item.classList.contains("editable")) {
//       item.classList.add("selected");
//     }
//   });

//   item.addEventListener("dblclick", function () {
//     item.classList.add("editable");
//   });
// });
//Fin Aun no se que hace


//Calcular Lotaje
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
capitalRiesgoInput.addEventListener('input', calculateResult);
stoplossInput.addEventListener('input', calculateResult);
const activoSelect = document.getElementById('activo');
const activoSeleccionadoLabel = document.getElementById('activo_seleccionado');

activoSelect.addEventListener('change', () => {
  const activoSeleccionado = activoSelect.value;
  activoSeleccionadoLabel.textContent = activoSeleccionado;
});


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
  stoplossInput.value = stoplossInput.value.replace(/[^\d.-]/g, '');
  takeprofitInput.value = takeprofitInput.value.replace(/[^\d.-]/g, '');
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


//Calcular porcentaje Utilidad Beneficio real
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
cuentaInput.addEventListener('input', calculateUtilidadBeneficioReal);
BeneficioRealInput.addEventListener('input', calculateUtilidadBeneficioReal);
// porcentajeBeneficioRealInput.addEventListener('input', calculateUtilidadBeneficioReal);

function calculateUtilidadBeneficioReal() {
  BeneficioRealInput.value = BeneficioRealInput.value.replace(/[^\d.-]/g, '');
  // porcentajeBeneficioRealInput.value = porcentajeBeneficioRealInput.value.replace(/[^\d.-]/g, '');
  let BeneficioReal = parseFloat(BeneficioRealInput.value);
  let cuenta = parseFloat(cuentaInput.value);
  // Validamos si existen datos dentro del input

  let porcentaje_beneficio_real = BeneficioReal * 100 / cuenta;
  porcentajeBeneficioRealInput.value = porcentaje_beneficio_real.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
  
}
//Fin Calcular Porcentaje Utilidad Beneficio real


function expandImage(img) {
  var expandedImage = document.createElement('div');
  expandedImage.classList.add('expanded-image');
  var imgElement = document.createElement('img');
  imgElement.src = img.src;
  expandedImage.appendChild(imgElement);
  document.body.appendChild(expandedImage);
  setTimeout(function () {
    expandedImage.style.opacity = 1;
  }, 0);
  expandedImage.onclick = function () {
    expandedImage.style.opacity = 0;
    setTimeout(function () {
      expandedImage.parentNode.removeChild(expandedImage);
    }, 300);
  };
}


$(document).ready(function () {
  $("#open-modal-button").click(function () { 
    event.preventDefault();   
    $("#nuevocontainer").addClass("show");
    $("#nuevocontainer").addClass("modal-open");
    $("#nuevocontainer").css("display", "block");
  
  });

  $(".close").click(function () {
    $("#nuevocontainer").removeClass("show");
    $("#nuevocontainer").removeClass("modal-open");
    $("#nuevocontainer").css("display", "none");
  });

  $("#expand-modal-button").click(function () {
    $(".modal-dialog").toggleClass("expanded");
  });
});

$("#nuevocontainer").click(function(event) {
  if (event.target.id === "nuevocontainer") {
    $("#nuevocontainer").hide();
  }
});

 // Configuración del calendario
 $( function() {
  $( "#fecha" ).datepicker({
    dateFormat: "yy-mm-dd",
    changeMonth: true,
    changeYear: true,
    yearRange: "-100:+0",
    showButtonPanel: true
  });
});



// Despliega nuevo formulario de ingreso, haciendo scroll hasta el final del modal
modalBodyAdd.style.display = "none";

$(document).ready(function () {
  const toggleButton = $("#toggleButton");
  const modalBodyAdd = $("#modalBodyAdd");

  toggleButton.click(function () {
    modalBodyAdd.slideToggle(50, function() {
      toggleButton.html(modalBodyAdd.hasClass("show") ? '<i class="fas fa-plus"></i>' : '<i class="fas fa-minus"></i>');
      modalBodyAdd.toggleClass("show");
      $('#nuevocontainer').animate({
        scrollTop: $('#nuevocontainer')[0].scrollHeight
      }, 500);
    });
  });

// Agrega la clase 'edited' al elemento padre del input, imagen o textarea que se haya editado
$('input, textarea').on('input', function () {
  const imageContainer = $(this).closest('.image-container');
  imageContainer.addClass('edited');
  imageContainer.find('.update-button').show();
});

// Mostrar solo el botón de actualización correspondiente al hacer clic en el elemento correspondiente
$('.update-button').click(function () {
  const imageContainer = $(this).closest('.image-container');
  imageContainer.removeClass('edited');
  $(this).hide();
});

  // Agregar desplazamiento hacia el final del modal al presionar el botón "guardar"
  $('.add-button').click(function() {
    $('#nuevocontainer').animate({
      scrollTop: $('#nuevocontainer')[0].scrollHeight
    }, 500);
  });
});




// Obtener el botón "Volver arriba"
var mybutton = document.getElementById("back-to-top-button");

// Cuando el usuario hace scroll hacia abajo desde la parte superior de la página, mostrar el botón
window.onscroll = function() {
  event.preventDefault(); 
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// Cuando el usuario hace clic en el botón, volver arriba de manera suave
mybutton.addEventListener("click", function() {
  event.preventDefault(); 
  // Obtenemos el elemento con clase "modal-content"
  var modalContent = document.querySelector(".modal-body");
  
  // Obtenemos la posición del elemento
  var modalContentPosition = modalContent.getBoundingClientRect().top;
  
  // Animamos el scroll hacia la posición del elemento
  window.scrollBy({
    top: modalContentPosition,
    left: 0,
    behavior: 'smooth'
  });
});
