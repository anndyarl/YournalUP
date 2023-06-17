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
  

  
