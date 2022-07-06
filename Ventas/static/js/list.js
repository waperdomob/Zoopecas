function enviarid(data){
    $('#detailTable').DataTable({
        responsive: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: {
                'action': 'search_details_prod',
                'id': data.id
            },
            dataSrc: "",
            headers: {
                'X-CSRFToken': csrftoken
            },
        },
        columns: [
            {"data": "producto.producto"},
            {"data": "producto.categoria.categoria"},
            {"data": "precio"},
            {"data": "cant"},
            {"data": "subtotal"},
        ],
        columnDefs: [
            {
                targets: [-1, -3],
                class: 'text-center',
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
            {
                targets: [-2],
                class: 'text-center',
                render: function (data, type, row) {
                    return data;
                }
            },
        ],
        initComplete: function (settings, json) {
        }
    });
    $('#detailVenta_Modal').modal('show');
}