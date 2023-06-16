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
