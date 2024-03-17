function PagePrevious() {
	window.history.back();
}

//Solo numeros
function Solo_Numero(e){
	var keynum = window.event ? window.event.keyCode : e.which;
	if ((keynum == 8) || (keynum == 46))
	return true;
	return /\d/.test(String.fromCharCode(keynum));
}
  
//Solo texto
function Solo_Texto(e) {
	var code;
	if (!e) var e = window.event;
	if (e.keyCode) code = e.keyCode;
	else if (e.which) code = e.which;
	var character = String.fromCharCode(code);
	var AllowRegex  = /^[\ba-zA-Z\s]$/;
	if (AllowRegex.test(character)) return true;     
	return false; 
}
  //Solo numeros sin puntos 
function Solo_Numero_ci(e){
	var keynum = window.event ? window.event.keyCode : e.which;
	if ((keynum == 8))
	return true;
	return /\d/.test(String.fromCharCode(keynum));
}
  
  // solo numeros y letras sin caracteres especiales
function Texto_Numeros(e) {
	var code;
	if (!e) var e = window.event;
	if (e.keyCode) code = e.keyCode;
	else if (e.which) code = e.which;
	var character = String.fromCharCode(code);
	var AllowRegex  = /^[A-Za-z0-9\s\.,-]+$/g;
	if (AllowRegex.test(character)) return true;     
	return false; 
}

$(function() {

	$('#listado').DataTable({
		responsive: true,
		autoWidth: false,
		destroy: true,
		deferRender: true,
		ordering: false,
		searching: true,
		paging: true,
		"language": {
			"sProcessing": "Procesando...",
			"sLengthMenu": "Mostrar _MENU_ registros",
			"sZeroRecords": "No se encontraron resultados",
			"sEmptyTable": "Ningún dato disponible en esta tabla",
			"sInfo": "Mostrando del _START_ al _END_ de un total de _TOTAL_ registros",
			"sInfoEmpty": "Mostrand del 0 al 0 de un total de 0 registros",
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
		initComplete: function(settings, json) {
	
		}
	});
	
});

/** TABLA DINAMICA PARA NO REPETIR CODIGO */
const getDataTable = async (paging_p, searching_p, ordering_p, id_table, data_params, data_columns, data_columns_def, data_url) => {

	tblCate = $(id_table).DataTable({
		responsive: true,
		autoWidth: false,
		destroy: true,
		deferRender: true,
		ordering: ordering_p,
		searching: searching_p,
		paging: paging_p,
		"aaSorting": [], 
		"language": {
			"sProcessing": "Procesando...",
			"sLengthMenu": "Mostrar _MENU_ registros",
			"sZeroRecords": "No se encontraron resultados",
			"sEmptyTable": "Ningún dato disponible en esta tabla",
			"sInfo": "Mostrando del _START_ al _END_ de un total de _TOTAL_ registros",
			"sInfoEmpty": "Mostrand del 0 al 0 de un total de 0 registros",
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
		ajax: {
			url: data_url,
			type: 'POST',
			data: data_params,
			dataSrc: ""
		},
		columns: data_columns,
		columnDefs: data_columns_def,
		initComplete: function (settings, json) {

		},

	});


}


const SendDataJsonBuyForm = async (url, parameters, callback) => {
	try {

		const response = await fetch (url, {
			method: "POST",
			body: parameters
		});
		const data = await response.json();

		notifier.show(data['response']['title'], data['response']['data'], data['response']['type_response'], '', 4000);
		if (data['response']['type_response'] === 'danger') {
			console.log(data);
			return false
		}

		callback();

	} catch (error) {
		notifier.show('Ocurrió un error!', error, 'danger', '', 4000);
		console.log(error);
	}
}

const SendDataJSONForm = async (url, form, callback) => {
	try {
		const formData = new FormData(form);

		const response = await fetch (url, {
			method: "POST",
			body: formData
		});
		const data = await response.json();

		notifier.show(data['response']['title'], data['response']['data'], data['response']['type_response'], '', 4000);
		if (data['response']['type_response'] === 'danger') {
			console.log(data);
			return false
		}

		callback();

	} catch (error) {
		notifier.show('Ocurrió un error!', error, 'danger', '', 4000);
		console.log(error);
	}
}