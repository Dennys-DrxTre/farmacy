let form_user = document.getElementById('form_user');
let form_filter = document.getElementById('id_select_filter');
let form_reset = document.getElementById('form_reset_password');

let title_usuarios = {
    'AD': 'Listado de Administradores',
    'AL': 'Listado de Almacenistas',
    'AT': 'Listado de Atención al cliente',
    'JC': 'Listado de Jefes de comunidades',
    'PA': 'Listado de Pacientes',
}

let getData = async (filter_id='PA') => {
    // PROVIDERS LIST
    await getDataTable(
        // paging
        true,
        // searching
        true,
        // ordering
        true,
        '#listado_usuarios',
        {
            'action': 'search_usuarios',
            'filter_id': filter_id,
        },
        [
            {"data": "cedula"},
            {"data": "nombres"},
            {"data": "apellidos"},
            {"data": "genero"},
            {"data": "telefono"},
            {"data": "zona.zona_residencia"},
            {"data": "id"},
        ],
        [
            {
                targets: [-1],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    let buttons = '<a href="#" rel="edit" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Editar Usuario"><i class="fa fa-edit"></i></a>';
                    buttons += '<a href="#" rel="btn_recuperar_clave" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Restablecer contraseña"><i class="fa fa-unlock"></i></a>';
                    return buttons
                }
            },
        ],
        '/listado-de-perfiles/'
    );

}


$( async function () {
    page_title.innerHTML = title_usuarios[$('select[name="select_filter"]').val()]
    await getData($('select[name="select_filter"]').val());

	// ALMACEN SEND FORM
	form_user.addEventListener('submit', async (e) => {
        e.preventDefault();
        let parameters = new FormData(form_user);
        await SendDataJsonForm(type_actions['user'][action.value], parameters, async () => {  
            await getData($('select[name="select_filter"]').val());
            $('#smallmodal').modal('hide');   
            $("#form_user")[0].reset(); 
        });
    });

    // REGISTER USUARIO
    $('#btn_nuevo_usuario').on('click', function () {
        $('#form_user')[0].reset();
        $('input[name="action"]').val('nuevo_usuario');
        $('#smallmodal').modal('show');
    });

    // RESET PASSWORD

    $('#listado_usuarios tbody').on('click', 'a[rel="btn_recuperar_clave"]', function () {
        $('#form_reset_password')[0].reset();
        var tr = tblCate.cell($(this).closest('td, li')).index();
        var data = tblCate.row(tr.row).data();

        $('input[name="action_reset"]').val('reset_password');
        $('input[name="username_reset"]').val(data.usuario.username);

        $('#modal_reset_password').modal('show');

        // ALMACEN SEND FORM
        form_reset.addEventListener('submit', async (e) => {
            e.preventDefault();
            let parameters = new FormData(form_reset);
            if ($('input[name="password1_reset"]').val() === $('input[name="password2_reset"]').val() ) {
                await SendDataJsonForm(type_actions['user'][id_action_reset.value], parameters, async () => {  
                    await getData($('select[name="select_filter"]').val());
                    $('#modal_reset_password').modal('hide');   
                    $("#form_reset")[0].reset(); 
                });
            }else{
                notifier.show('Ocurrió un error!', 'Las contraseñas nueva no coinciden', 'danger', 4000);
            }
        });
    });


    form_filter.addEventListener('change', async (e) =>{
        e.preventDefault();
        await getData($('select[name="select_filter"]').val())
        notifier.show('Exito!', 'Filtro realizado con exito', 'success', '', 4000);
        page_title.innerHTML = title_usuarios[$('select[name="select_filter"]').val()]
    });
    
});