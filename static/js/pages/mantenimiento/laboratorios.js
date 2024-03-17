let form_lab = document.getElementById('form_lab');

$( async function () {

	// LOGIN SEND FORM
	form_lab.addEventListener('submit', async (e) => {
        e.preventDefault();
        $('input[name="action"]').val('nuevo_lab');
        await SendDataJSONForm('/registro-de-laboratorio/', form_lab, async () => {  
            getDataTable();
        });
    });
    
});