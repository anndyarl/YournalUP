const form = document.getElementById('myForm');
const comision = document.getElementById('comision');
const swap = document.getElementById('swap');
let timeoutId;


const enviarFormulario = () => {
  form.submit();
};

comision.addEventListener('blur', enviarFormulario);
swap.addEventListener('blur', enviarFormulario);
beneficio_total.disabled = true; 
porcentaje_beneficio_total.disabled = true; 

  const comisionInput = document.getElementById('comision');
  comisionInput.addEventListener('input', () => {
    let value = comisionInput.value.trim();
  
    // Verificamos si el primer carácter es un número
    if (/^\d/.test(value)) {
      // Añadimos el signo menos al principio del valor
      value = '-' + value;
    }    
  
    comisionInput.value = value;
  });


  const swapInput = document.getElementById('swap');
  swapInput.addEventListener('input', () => {
    let value = swapInput.value.trim();
  
    // Verificamos si el primer carácter es un número
    if (/^\d/.test(value)) {
      // Añadimos el signo menos al principio del valor
      value = '-' + value;
    }
  
    swapInput.value = value;
  });
  
  document.addEventListener('DOMContentLoaded', function() {
    var toggleButton = document.getElementById('open-modal-button-commission');
    var modalContainerCommission = document.querySelector('.modal-container-commission');
    var isExpanded = false;
  
    toggleButton.addEventListener('click', function() {
      if (!isExpanded) {
        toggleButton.classList.add('expand');
        toggleButton.innerHTML = '<i class="fas fa-fw fa-angle-double-right"></i>';
        isExpanded = true;
        modalContainerCommission.classList.toggle('show');
      } else {
        toggleButton.classList.remove('expand');
        toggleButton.innerHTML = '<i class="fas fa-fw fa-angle-double-left"></i>';
        isExpanded = false;
        modalContainerCommission.classList.toggle('show');
      
      }
    });
  });
  
  const checkboxes = document.getElementsByClassName('fila-checkbox');

  // Itera sobre cada checkbox
  for (let i = 0; i < checkboxes.length; i++) {
    const checkbox = checkboxes[i];
    const checkboxId = checkbox.getAttribute('id');
  
    // Establece el estado inicial del checkbox basado en el valor guardado en localStorage
    const isChecked = localStorage.getItem(checkboxId) === 'true';
    checkbox.checked = isChecked;
  
    // Agrega un event listener para guardar el estado del checkbox en localStorage cuando cambie
    checkbox.addEventListener('change', function () {
      const checkboxLabel = this.parentNode;
      checkboxLabel.classList.toggle('checked');
  
      // Guarda el estado del checkbox en localStorage
      localStorage.setItem(checkboxId, this.checked.toString());
    });
  }
// Obtener todas las instancias del menú desplegable
const dropdowns = document.querySelectorAll('.dropdown');

// Agregar evento de clic a cada menú desplegable
dropdowns.forEach(function(dropdown) {
  const dropdownIcon = dropdown.querySelector('.dropdown-button');
  const dropdownMenu = dropdown.querySelector('.dropdown-menu');

  // Función para abrir el menú desplegable
  function openDropdown() {
    closeDropdowns();
    dropdownMenu.classList.add('show');
    // document.body.style.overflow = 'hidden'; // Bloquear el scroll del body
    // const tablaScroll = dropdown.closest('.tabla-scroll'); // Obtener la referencia a la tabla
    // if (tablaScroll) {
    //   tablaScroll.style.overflow = 'hidden'; // Bloquear el scroll de la tabla
    // }
  }

  // Función para cerrar el menú desplegable
  function closeDropdown() {
    dropdownMenu.classList.remove('show');
    // document.body.style.overflow = ''; // Habilitar el scroll del body
    // const tablaScroll = dropdown.closest('.tabla-scroll'); // Obtener la referencia a la tabla
    // if (tablaScroll) {
    //   tablaScroll.style.overflow = ''; // Habilitar el scroll de la tabla
    // }
  }

  // Abrir el menú desplegable al hacer clic o tocar en el icono
  dropdownIcon.addEventListener('click', function(event) {
    event.stopPropagation();
    openDropdown();
  });

  // Cerrar el menú desplegable al hacer clic fuera de él
  document.addEventListener('click', function() {
    closeDropdown();
  });

  // Cerrar el menú desplegable al tocar fuera de él en dispositivos táctiles
  document.addEventListener('touchstart', function(event) {
    if (!dropdown.contains(event.target)) {
      closeDropdown();
    }
  });
});

// Cerrar todos los menús desplegables
function closeDropdowns() {
  dropdowns.forEach(function(dropdown) {
    const dropdownMenu = dropdown.querySelector('.dropdown-menu');
    dropdownMenu.classList.remove('show');
  });
  document.body.style.overflow = ''; // Habilitar el scroll del body al cerrar todos los menús
  const tablaScrolls = document.querySelectorAll('.tabla-scroll');
  tablaScrolls.forEach(function(tablaScroll) {
    tablaScroll.style.overflow = ''; // Habilitar el scroll de todas las tablas al cerrar todos los menús
  });
}
