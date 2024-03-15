let form_ingreso = document.getElementById('form_register');
let form_search = document.getElementById('search-input');

let vents = {
    items : {
        fecha: '',
        cantidad: 0,
        descripcion: '',
        tipo_ingreso: '',
        det: []
    },
    get_ids: function () {
        var ids =  [];
        $.each(this.items.det, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    add: function (item) {
        this.items.det.push(item);
        this.list()
    },
    search_productos: async function () {
        /** PRODUCT LIST **/
        await getDataTable(
            // paging
            true,
            // searching
            true,
            // ordering
            true,
            '#id_datatable_productos',
            {
                'action': 'search_productos',
                'ids': JSON.stringify(vents.get_ids()),
            },
            [
                {"data": "nombre"},
                {"data": "tipo_insumo"},
                {"data": "almacen"},
                {"data": "laboratorio"},
                {"data": "if_expire_date"},
                {"data": "total_stock"},
                {"data": "id"},
            ],
            [
        
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        let buttons = '<a href="#" rel="select_product" class="btn btn-icon btn-dark" data-bs-toggle="tooltip" data-bs-placement="top" title="Seleccionar producto"><i class="fas fa-hand-pointer"></i></a>';

                        return buttons
                    }
                },
            ],
            '/buscardor-de-productos/'
        );
    },
    list: function () {
        
        tblCate = $('#detalle').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            ordering:  false,
            searching: false,
            paging: false,
            "language": {
                "sProcessing": "Procesando...",
                "sLengthMenu": "Mostrar _MENU_ registros",
                "sZeroRecords": "No se encontraron resultados",
                "sEmptyTable": "Ningún dato disponible en esta tabla",
                "sInfo": "Mostrando _START_ al _END_ de un total de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando 0 al 0 de un total de 0 registros",
                "sInfoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sInfoPostFix": "",
                "sSearch": "Buscar:",
                "sUrl": "",
                "sInfoThousands": ",",
                "sLoadingRecords": "Cargando...",
                "oPaginate": {
                    "sFirst": "<span class='fa fa-angle-double-left'></span>",
                    "sLast": "<span class='fa fa-angle-double-right'></span>",
                    "sNext": "<span class='fa fa-angle-right'></span>",
                    "sPrevious": "<span class='fa fa-angle-left'></span>"
                },
                "oAria": {
                    "sSortAscending": ": Activar para ordenar la columna de manera ascendente",
                    "sSortDescending": ": Activar para ordenar la columna de manera descendente"
                }
            },
            data: this.items.det,
            columns: [
                {"data": "nombre"},
                {"data": "lote"},
                {"data": "cantidad"},
                {"data": "f_vencimiento"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<input type="text" value="'+ data +'"name="lote" class="form-control form-control-sm lote" required autocomplete="off">';
                    }
                },
                {
                    targets: [2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row, meta) {                        
                        return '<input type="number" value="'+ parseInt(data) +'" name="cantidad" class="form-control form-control-sm cantidad" required min="1" autocomplete="off">';
                    }
                },
                {
                    targets: [3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        return '<input type="date" value="'+ data +'"name="f_vencimiento" class="form-control form-control-sm f_vencimiento" required autocomplete="off">';
                    }
                },
                {
                    targets: [4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {

                        buttons = '<a href="#" rel="delete" class="btn btn-icon btn-danger"><i class="fa fa-trash"></i></a> ';                       
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            },
        });

    },
};

$('#id_tipo_ingreso').select2({
    theme: 'bootstrap4',
    language: 'es',
    placeholder: 'Selecionar tipo de ingreso',
    allowClear: true
});

// FORMATTING WHEN DISPLAYING THE RESULT OF THE SELECT
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }

    let option = $(
        '<div class="col text-left shadow-sm">' +
        '<p style="margin-bottom: 0;">' +
        '<b class="text-white">Nombre:</b> <b class="text-white">' + repo.text+ '</b><br>' +
        '<b class="text-white">Codigo:</b> <b class="text-white">' + repo.id + '</b><br>' +
        '<b class="text-white">Disponibilidad:</b> <b class="text-white">' + repo.others.total_stock + '</b><br>' +
        '</p>' +
        '</div>');

    return option;
}

$(function () {

    vents.list()

    // auto complete search
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: "es",
        allowClear: true,
        ajax: {
            delay: 250,
            type: "POST", 
            url: '/buscar-productos/',
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: "search_productos",
                    ids: JSON.stringify(vents.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                var results = [];
              
                $.each(data, function (index, res) {
                    results.push({
                        id: res.id,
                        text: res.nombre,
                        others: res
                    });
                });
    
                return {
                    results: results
                };
            },
            cache: true

        },
        placeholder: 'Buscar producto ...', 
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.cantidad = 1;
        data.nombre = data.text;
        data.lote = "";
        data.f_vencimiento = "";
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });

    // // calculate purchase when changing the vat percentage
    // $('#percentage_iva').on('change keyup', function () {
    //     let amount = $(this).val();
    //      vents.items.percentage_iva = parseInt(amount);
    //      vents.calculate_invoice();
    // });
    // // calculate purchase when changing the quantity
    // $('#id_datatable_detail_buy tbody').on('change keyup', '.quantity', function () {
    //     let quantity = $(this).val();
    //     var tr = tblCate.cell($(this).closest('td, li')).index();
    //      vents.items.det[tr.row].quantity = parseInt(quantity);
    //      vents.calculate_invoice();
    //      $('td:eq(4)', tblCate.row(tr.row).node()).html(parseFloat(vents.items.det[tr.row].amount).toFixed(2))
    // });
    // // calculate purchase when changing the price
    // $('#id_datatable_detail_buy tbody').on('change keyup', '.price', function () {
    //     let price = $(this).val();
    //     var tr = tblCate.cell($(this).closest('td, li')).index();
    //      vents.items.det[tr.row].price = parseFloat(price);
    //      vents.calculate_invoice();
    //      $('td:eq(4)', tblCate.row(tr.row).node()).html(parseFloat(vents.items.det[tr.row].amount).toFixed(2))
    // });
    // // delete individual element
    // $('#id_datatable_detail_buy tbody').on('click', 'a[rel="delete"]', function () {
    //     var tr = tblCate.cell($(this).closest('td, li')).index();
    //     vents.items.det.splice(tr.row, 1);
    //     vents.list();
    //     notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    // });
    // /// remove all detail
    // $('a[rel="btn_delete"]').on('click', function () {
    //     if (vents.items.det.length === 0) return false;
    //     vents.items.det = [];
    //     vents.list();
    //     notifier.show('Exito!', 'Se ha eliminado correctamente', 'success', '', 4000);
    // });
    // // select2 provider
    // $('#id_provider').select2({
    //     theme: 'bootstrap4',
    //     language: 'es',
    //     placeholder: 'Selecionar proveedor',
    //     allowClear: true
    // });
    // /** OPEN MODAL PROVIDER **/
    // $('a[rel="open_modal_provider"]').on('click', function () {
    //     $('#id_provider').val(null).trigger('change');
    //     vents.search_provider()
    //     $('#modal_search_provider').modal('show');
    // });
    // // PROVIDER SELECT
    // $('#id_datatable_provider tbody').on('click', 'a[rel="select_provider"]', function () {
    //     var tr = tblCate.cell($(this).closest('td, li')).index();
    //     var data = tblCate.row(tr.row).data();
    //     $('#id_provider').val(data.id);
    //     $('#id_provider').trigger('change'); 
    //     $('#modal_search_provider').modal('hide');   
    // });
    // /** OPEN MODAL PRODUCT **/
    // $('a[rel="open_modal_product"]').on('click', function () {
    //     vents.search_products()
    //     $('#modal_search_product').modal('show');
    // });
    // // PRODUCT SELECT
    // $('#id_datatable_products tbody').on('click', 'a[rel="select_product"]', function () {
    //     var tr = tblCate.cell($(this).closest('td, li')).index();
    //     var products = tblCate.row(tr.row).data();
    //     let data = {
    //         id: products.id,
    //         text: products.name,
    //         others: products,
    //         price: products.price_buy,
    //         quantity: 1,
    //         amount: 0.00,
    //         iva: 0.00,
    //         iva_bs: 0.00,
    //         total_bs: 0.00,
    //     }
    //     vents.add(data);
    //     $('#modal_search_product').modal('hide');   
    // });
    // event submit
    // $('#form_register').on('submit', async function (e) {
    //     e.preventDefault();
        
    //     if (vents.items.det.length === 0) {
    //         notifier.show('Ocurrio un error!', 'Debe al menos tener un producto en la compra', 'danger', '', 4000);
    //         return false;
    //     }
    //     vents.items.observation = $('textarea[name="observation"]').val();
    //     vents.items.created = $('input[name="created"]').val();
    //     // console.log($('input[name="created"]').val());
    //     // return false;
    //     vents.items.provider = $('select[name="provider"]').val();
    //     vents.items.percentage_iva = parseFloat($('input[name="percentage_iva"]').val())
    //     vents.items.dollar = parseFloat($('input[name="dollar"]').val())
    //     var parameters = new FormData();
    //     parameters.append('action', 'register_buy');
    //     parameters.append('vents', JSON.stringify(vents.items));
    
    //     btn_submit.disabled = true;

    //     await SendDataJsonBuyForm(window.location.pathname, parameters, function () {
    //         window.location.replace('/listado-de-compras/');
    //     })
    // });
});