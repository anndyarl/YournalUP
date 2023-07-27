// const form = document.getElementById('commission-form');
// const comision = document.getElementById('comision');
// const swap = document.getElementById('swap');
// let timeoutId;


// const enviarFormulario = () => {
//   form.submit();
// };

// comision.addEventListener('blur', enviarFormulario);
// swap.addEventListener('blur', enviarFormulario);
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
  const dropdowns = document.querySelectorAll('.dropdown');

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
  
 
  document.addEventListener('DOMContentLoaded', function() {  
  var modalContainer = document.querySelector('.modal-container-commission');
  var closeButton = modalContainer.querySelector('.close');
  
  closeButton.addEventListener('click', function() {
    modalContainer.classList.remove('show');
  });
});

// Agrega la clase 'edited' al elemento padre del input, imagen o textarea que se haya editado
$('input, select').on('input', function() {
  const Container = $(this).closest('.modal-container-commission, .container-commission-desktop');
  Container.addClass('edited');
  Container.find('.add-order-button-commission').removeClass('disabled-button').show();
});

// Mostrar solo el botón de actualización correspondiente al hacer clic en el elemento correspondiente
$('.add-order-button-commission').click(function() {
  const Container = $(this).closest('.modal-container-commission, .container-commission-desktop');
  Container.removeClass('edited');
  $(this).addClass('disabled-button');
});

// document.addEventListener('DOMContentLoaded', function() {
//   var toggleButton = document.getElementById('open-modal-button');
//   var modalContainer = document.getElementById('modal-confirm');
//   var closeButton = modalContainer.querySelector('.close'); 

//   toggleButton.addEventListener('click', function() {
//     modalContainer.classList.toggle('show');
//   });

//   closeButton.addEventListener('click', function() {
//     modalContainer.classList.remove('show');
//   });

// });
 document.addEventListener('DOMContentLoaded', function() {
var tablaScroll = document.querySelector('.tabla-scroll');

tablaScroll.addEventListener('mouseenter', function() {
  tablaScroll.classList.remove('hide-scrollbar');
});

tablaScroll.addEventListener('mouseleave', function() {
  tablaScroll.classList.add('hide-scrollbar');
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