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

// ID de la hoja de cálculo y rango de la celda que deseas obtener
const SHEET_ID = '1vs-Qp3D73AZxpkb39KtwQATMAybyzsqc9tbAqvFUP-E';
const SHEET_TITLE = 'Factores';
const SHEET_RANGE = 'Factores!A2:C53';

const FULL_URL = `https://docs.google.com/spreadsheets/d/${SHEET_ID}/gviz/tq?sheet=${SHEET_TITLE}&range=${SHEET_RANGE}`;
let factor = 1;

// Calcular Lotaje
// Agregamos un eventListener al evento input en ambos inputs para que se calcule el resultado en tiempo real
capitalRiesgoInput.addEventListener('input', calcularLotaje);
stoplossInput.addEventListener('input', calcularLotaje);
const activoSelect = document.getElementById('activo');
const activoSeleccionadoLabel = document.getElementById('activo_seleccionado');


activoSelect.addEventListener('change', () => { 
  lotajeInput.value = ""; // Reiniciamos el valor del input de lotaje al seleccionar un nuevo activo
  stoplossInput.value = "";
  takeprofitInput.value = "";
  ratioInput.value = "";
  BeneficioEsperadoInput.value = "";
  utilidadProyectadaInput.value = "";

  // if(activoSelect.value === '' ){
  //   stoploss.disabled = true; // Deshabilitar el campo
  //   takeprofit.disabled = true; 
  // }
  // else{
  //   stoploss.disabled = false; // Deshabilitar el campo
  //   takeprofit.disabled = false;
  // }
    
});

function calcularLotaje() {
  const capitalRiesgo = parseFloat(capitalRiesgoInput.value);
  const stoploss = parseFloat(stoplossInput.value);
  
   // Validamos si existen datos dentro del input
   if (stoploss === 0 || isNaN(stoploss)) {
    lotajeInput.value = "";
    takeprofitInput.value = "";
    return;
  }
  const activoSeleccionado = activoSelect.value;

  fetch(FULL_URL)
    .then(res => res.text())
    .then(rep => {
      const data = JSON.parse(rep.substring(47).slice(0, -2));
      const rows = data.table.rows; // Acceder a la propiedad 'rows' dentro de 'table'
      

      if (data && data.table && rows) {
        // Recorrer los datos de la columna "INSTRUMENTO" en el JSON y realizar la comparación
        for (let i = 0; i < rows.length; i++) {
          const instrumento = rows[i].c[0].v;
          if (instrumento === activoSeleccionado) {
            factor = rows[i].c[2].v;
            if(factor < 10)
            {
              factor = 10;
            }
            break; // Si se encuentra la coincidencia, se sale del bucle
          }
        }
      }

      const lotaje = capitalRiesgo / stoploss / factor;
      lotajeInput.value = lotaje.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
    })
    .catch(error => {
      console.error('Error al obtener los datos del JSON:', error);
    });
}
// Fin Calcular Lotaje





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
  let stoploss = parseFloat(stoplossInput.value);
  let takeprofit = parseFloat(takeprofitInput.value);

  // Validamos si existen datos dentro del input
  if (stoploss == 0 || isNaN(stoploss) || takeprofit == 0 || isNaN(takeprofit)) {
    ratioInput.value = "";  
    return;
  }
  let ratio = takeprofit / stoploss;
  ratioInput.value = "1 / " + ratio.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
}
//Fin Calcular ratio reisgo/beneficio

//Calcular  Beneficio Esperado
// Agregamos un eventListener al evento input en ambos input para que se calcule el resultado en tiempo real
lotajeInput.addEventListener('input', calculateBeneficioEsperado);
takeprofitInput.addEventListener('input', calculateBeneficioEsperado);
stoplossInput.addEventListener('input', calculateBeneficioEsperado);
BeneficioEsperadoInput.addEventListener('input', calculateBeneficioEsperado);

function calculateBeneficioEsperado() {
  let lotaje = parseFloat(lotajeInput.value);
  let takeprofit = parseFloat(takeprofitInput.value);
  let stoploss = parseFloat(stoplossInput.value);

  // Validamos si existen datos dentro del input
  if (stoploss == 0 || isNaN(stoploss) || takeprofit == 0 || isNaN(takeprofit)) {
    BeneficioEsperadoInput.value = "";    
    return;
  }
  let beneficio = lotaje *  factor * takeprofit;
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
if(BeneficioRealInput && porcentajeBeneficioRealInput){
cuentaInput.addEventListener('input', calculateUtilidadBeneficioReal);
BeneficioRealInput.addEventListener('input', calculateUtilidadBeneficioReal);
// porcentajeBeneficioRealInput.addEventListener('input', calculateUtilidadBeneficioReal);

function calculateUtilidadBeneficioReal() {
  BeneficioRealInput.value = BeneficioRealInput.value.replace(/[^\d.-]/g, '');
  // porcentajeBeneficioRealInput.value = porcentajeBeneficioRealInput.value.replace(/[^\d.-]/g, '');
  let BeneficioReal = parseFloat(BeneficioRealInput.value);
  let cuenta = parseFloat(cuentaInput.value);
  // Validamos si existen datos dentro del input

  if (BeneficioReal == 0 || isNaN(BeneficioReal)) {
    porcentajeBeneficioRealInput.value = "";
    return;
  }

  let porcentaje_beneficio_real = BeneficioReal * 100 / cuenta;
  porcentajeBeneficioRealInput.value = porcentaje_beneficio_real.toFixed(2); // Redondeamos el resultado a dos decimales y lo mostramos en el tercer input
  
}
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
// modalBodyAdd.style.display = "none";

$(document).ready(function () {
  const toggleButton = $("#toggleButton");
  const modalBodyAdd = $("#modalBodyAdd");

  toggleButton.click(function () {
    modalBodyAdd.slideToggle(50, function() {
      toggleButton.html(modalBodyAdd.hasClass("show") ? '<i class="fas fa-plus"></i>' : '<i class="fas fa-minus"></i>');
      modalBodyAdd.toggleClass("show");
      $('.modal-container').animate({
        scrollTop: $('.modal-container')[0].scrollHeight
      }, 500);
    });
  });

// Agrega la clase 'edited' al elemento padre del input, imagen o textarea que se haya editado
$('input, textarea').on('input', function () {
  const imageContainer = $(this).closest('.image-container');
  imageContainer.addClass('edited');
  imageContainer.find('.update-button').show(); 
});

$('input[type="file"]').on('change', function () {
  const fileInput = $(this);
  const imageContainer = fileInput.closest('.image-container');
  imageContainer.addClass('edited');
  imageContainer.find('.add-button').removeClass('disabled-button').show();
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


document.addEventListener('DOMContentLoaded', function() {
  var toggleButton = document.getElementById('open-modal-button');
  var modalContainer = document.querySelector('.modal-container');
  var closeButton = modalContainer.querySelector('.close');
  var expandModalButton = document.getElementById('expand-modal-button');
  var gridContainerMaster = document.querySelector('.grid-container-master');
  var gridContainer = document.querySelector('.grid-container');

  toggleButton.addEventListener('click', function() {
    modalContainer.classList.toggle('show');
  });

  closeButton.addEventListener('click', function() {
    modalContainer.classList.remove('show');
  });

  expandModalButton.addEventListener('click', function() {
    if (gridContainerMaster.style.gridTemplateColumns != '1fr') { 
      
      gridContainerMaster.classList.add('expand');   
      gridContainerMaster.style.gridTemplateColumns = '1fr';
      gridContainer.style.display = 'none';     
    }
    else{
      gridContainerMaster.style.gridTemplateColumns = 'repeat(2, 1fr)';     
      gridContainerMaster.classList.remove('expand');  
      gridContainer.style.display = 'grid';
    }
  });  

});


const textarea1 = document.getElementById('descripcion');
textarea1.addEventListener('input', function() {
  this.style.height = 'auto';
  this.style.height = this.scrollHeight + 'px';
});




// Obtener todos los elementos de texto de descripción
const textAreas = document.querySelectorAll('[id^="descripcion_"]');

// Iterar sobre cada elemento de texto de descripción
textAreas.forEach((textarea) => {
  // Establecer la altura inicial en función del contenido existente
  textarea.style.height = textarea.scrollHeight + 'px';

  textarea.addEventListener('input', function () {
    this.style.height = 'auto';
    this.style.height = this.scrollHeight + 'px';

    // Almacenar el contenido del textarea en el almacenamiento local
    localStorage.setItem('textareaContent', this.value);
  });
});

const dropdowns = document.querySelectorAll('.dropdown-delete');

dropdowns.forEach(function(dropdown) {
  const dropdownIcon = dropdown.querySelector('.dropdown-button');
  const dropdownMenu = dropdown.querySelector('.dropdown-menu');

  function openDropdown() {
    closeDropdowns();
    dropdownMenu.classList.add('show');
  }

  function closeDropdown() {
    dropdownMenu.classList.remove('show');
  }

  dropdownIcon.addEventListener('click', function(event) {
    event.stopPropagation();
    openDropdown();
  });

  document.addEventListener('click', function() {
    closeDropdown();
  });

  document.addEventListener('touchstart', function(event) {
    if (!dropdown.contains(event.target)) {
      closeDropdown();
    }
  });
});

function closeDropdowns() {
  dropdowns.forEach(function(dropdown) {
    const dropdownMenu = dropdown.querySelector('.dropdown-menu');
    dropdownMenu.classList.remove('show');
  });
}

// // Realiza una solicitud HTTP a la API para obtener los tipos de cambio
// fetch("https://api.exchangeratesapi.io/latest?base=USD")
//   .then(response => response.json())
//   .then(data => {
//     // Obtén el tipo de cambio de AUD/CAD
//     var audCadExchangeRate = data.rates.CAD;

//     // Calcula el valor de AUD/CAD para un lote de 1
//     var audCadValue = 1 / audCadExchangeRate;

//     console.log(audCadValue);  // Salida: Valor de AUD/CAD para 1 lote
//   })
//   .catch(error => {
//     console.log("Error al obtener los datos de tipo de cambio:", error);
//   });

// fetch("https://www.alphavantage.co/query?function=FX_DAILY&from_symbol=AUD&to_symbol=CAD&apikey=TU_API_KEY")
//   .then(response => response.json())
//   .then(data => {
//     // Obtén el precio de cierre del último día disponible
//     var lastDayData = data["Time Series FX (Daily)"];
//     var dates = Object.keys(lastDayData);
//     var lastDate = dates[0];
//     var closePrice = parseFloat(lastDayData[lastDate]["4. close"]);

//     // Calcula el valor de AUD/CAD para un lote de 1
//     var audCadValue = 1 / closePrice;

//     console.log(audCadValue);  // Salida: Valor de AUD/CAD para 1 lote
//   })
//   .catch(error => {
//     console.log("Error al obtener los datos de Alpha Vantage:", error);
//   });


  $(document).ready(function() {
    // Abrir el modal al hacer clic en el botón de ayuda
    $("#open-modal-button-delete").click(function() {
      $('#modal-confirm').modal('show');
    });
  
    // Cerrar el modal al hacer clic en el botón de cierre
    $(".btn-secondary").click(function() {
      $('#modal-confirm').modal('hide');
    });
  });
  
  document.addEventListener('DOMContentLoaded', function() {
   var modalContainer = document.querySelector('.grid-container-2.modal-container.container');

  
  modalContainer.addEventListener('mouseenter', function() {
    modalContainer.classList.remove('hide-scrollbar');
  });
  
  modalContainer.addEventListener('mouseleave', function() {
    modalContainer.classList.add('hide-scrollbar');
  });
});

  
  //Alert Notifications
  function cerrarMensaje(btn) {
    var alertDiv = btn.parentNode;
    alertDiv.style.display = 'none';
  }  
  var alertDiv = document.querySelector('.alert.alert-info');
  if (alertDiv) {
    alertDiv.style.transition = 'opacity 10s'; // Duración de la transición: 5 segundos
    alertDiv.style.opacity = '1'; // Establecer la opacidad inicial en 1 para mostrar el mensaje
    setTimeout(function() {
      alertDiv.style.opacity = '0';
      setTimeout(function() {
        alertDiv.style.display = 'none';
      }, 10000); // 5000 milisegundos = 5 segundos (tiempo de espera después de la transición)
    }, 3000); // 3000 milisegundos = 3 segundos (tiempo de espera antes de iniciar la transición)
  }