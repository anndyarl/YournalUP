//abre modal de confirmación antes de borrar cuenta

  $(document).ready(function() {
    $('#deleteBtn').on('click', function(event) {
      event.preventDefault();
      const deleteUrl = $(this).attr('href');
      $('#confirmDeleteLink').attr('href', deleteUrl);
      $('#confirmDeleteModal').modal('show');
    });
  });

  $(document).ready(function(){
    $('#confirmDeleteModal').click(function(e) {
      if (e.target == this) {
        $('#confirmDeleteModal').modal('hide');
      }
    });
  });


  document.addEventListener("DOMContentLoaded", function() {
    const editableCells = document.querySelectorAll(".editable-cell");
  
    editableCells.forEach(cell => {
      cell.addEventListener("input", function() {
        const row = this.parentNode;
        const formData = new FormData();
        // formData.append("selected_option", this.querySelector("select").value);  // Agregar el valor seleccionado del <select>
        // formData.append("field_value", this.innerText);
        
        formData.append("field_name", this.getAttribute("name"));
        formData.append("field_value", this.innerText);
        console.log(formData);
        // Obtener el valor de id_cuenta
        const id_cuenta = this.dataset.idCuenta;
        console.log("id_cuenta:", id_cuenta);
  
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;  // Obtener el token CSRF 
       
        fetch(`editar_cuentas/${id_cuenta}/`, {
          method: "POST",
          headers: {
            'X-CSRFToken': csrfToken // Incluir el token CSRF como encabezado
          },
          body: formData
        })
        .then(response => {
          if (response.ok) {
            row.classList.add("success");           
            setTimeout(() => {
              row.classList.remove("success");
            }, 1000);
          } else {
            row.classList.add("error");
            setTimeout(() => {
              row.classList.remove("error");
            }, 1000);
          }
        })
        .catch(error => {
          console.error("Error:", error);
          row.classList.add("error");
          setTimeout(() => {
            row.classList.remove("error");
          }, 1000);
        });
      });
    });
  });
  

