let form_user = document.getElementById('form_user');

$( async function () {
    // await getData();

	// ALMACEN SEND FORM
	form_user.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_user);
        await SendDataJsonForm(type_actions['user'][action.value], parameters, async () => {  
            // await getData();
            $('#smallmodal').modal('hide');   
            $("#form_user")[0].reset(); 
        });
    });

    // REGISTER ALMACEN
    $('#btn_nuevo_usuario').on('click', function () {
        $('#form_user')[0].reset();
        $('input[name="action"]').val('nuevo_usuario');
        $('#smallmodal').modal('show');
    });

    // ALMACEN EDIT
    $('#listado_almacen tbody').on('click', 'a[rel="edit"]', function () {
        $('#form_user')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action"]').val('edit_almacen');
        $('input[name="id"]').val(data.id);
        $('input[name="nombre"]').val(data.nombre);

        $('#smallmodal').modal('show');
    });
    
});