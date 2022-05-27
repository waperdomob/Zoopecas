var tblProducts;
var vents={
    items : {
        cliente: '',
        fecha_compra : '',
        metodoPago:'',
        subtotal : 0.00,
        descuento : 0.00,
        total : 0.00,
        productos : []
    },
    get_ids: function () {
        var ids = [];
        $.each(this.items.productos, function (key, value) {
            ids.push(value.id);
        });
        return ids;
    },
    calculate_invoice: function () {
        var subtotal = 0.00;
        var descuento = $('input[name="descuento"]').val();
        $.each(this.items.productos, function (pos, dict) {
            dict.pos = pos; 
            dict.subtotal = dict.cant * parseFloat(dict.precio_venta);
            subtotal += dict.subtotal;
        });
        this.items.subtotal = subtotal;
        this.items.descuento = descuento; 
        this.items.total = this.items.subtotal - this.items.descuento;

        $('input[name="subtotal"]').val(this.items.subtotal.toFixed(2));
        $('input[name="total"]').val(this.items.total.toFixed(2));
    },
    add: function (item) {
        this.items.productos.push(item);
        this.list();
    },
    list: function () {
        this.calculate_invoice();
        tblProducts = $('#tblProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            data: this.items.productos,
            columns: [
                {"data": "id"},
                {"data": "producto"},
                {"data": "categoria.categoria"},
                {"data": "precio_venta"},
                {"data": "cant"},
                {"data": "subtotal"},
            ],
            columnDefs: [
                {
                    targets: [0],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash-alt"></i></a>';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<input type="text" name="cant" class="form-control form-control-sm input-sm" autocomplete="off" value="' + row.cant + '">';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
            ],
            rowCallback(row, data, displayNum, displayIndex, dataIndex) {

                $(row).find('input[name="cant"]').TouchSpin({
                    min: 1,
                    max: data.cantidad_total,
                    step: 1
                });

            },
            initComplete: function (settings, json) {

            } 
        });
    },
}
function formatRepo(repo) {
    if (repo.loading) {
        return repo.text;
    }
    if (!Number.isInteger(repo.id)) {
        return repo.text;
    }
    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.imagen + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.producto + '<br>' +
        '<b>Descripción:</b> ' + repo.descripcion + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.precio_venta + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}
$(function () {

    $("input[name='descuento']").on('change', function () {
        vents.calculate_invoice();
    })
        .val(0.0);
    
    // event remove all
    $('#btnRemoveAll').on('click', function () {
        if(vents.items.productos.length == 0) return false;

        alert_action('Notificación', '¿Estas seguro de eliminar todos los items?', function name(params) {
            vents.items.productos = [];
            vents.list(); 
        });
        
    });

    // event cant
    $('#tblProducts tbody')
        .on("click", 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            alert_action('Notificación', '¿Estas seguro de eliminar este producto?', function name(params) {
                vents.items.productos.splice(tr.row,1);
            vents.list();
            });            
        })
        .on('change', 'input[name="cant"]', function () {
        console.clear();
        var cant = parseInt($(this).val());
        var tr = tblProducts.cell($(this).closest('td, li')).index();
        vents.items.productos[tr.row].cant = cant;
        vents.calculate_invoice();
        $('td:eq(5)', tblProducts.row(tr.row).node()).html('$' + vents.items.productos[tr.row].subtotal.toFixed(2));
    });
    $('.btnClearSearch').on('click', function () {
        $('input[name="search"]').val('').focus();
    })
    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            responsive: true,
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'ids': JSON.stringify(vents.get_ids()),
                    'term': $('select[name="search"]').val()
                },
                dataSrc: ""
            },
            columns: [
                {"data": "full_name"},
                {"data": "image"},
                {"data": "stock"},
                {"data": "pvp"},
                {"data": "id"},
            ],
            columnDefs: [
                {
                    targets: [-4],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '<img src="' + data + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<span class="badge badge-secondary">' + data + '</span>';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    orderable: false,
                    render: function (data, type, row) {
                        var buttons = '<a rel="add" class="btn btn-success btn-xs btn-flat"><i class="fas fa-plus"></i></a> ';
                        return buttons;
                    }
                },
            ],
            initComplete: function (settings, json) {

            }
        });
        $('#myModalSearchProducts').modal('show');
    });
    //event submit
    $('form').on('submit', function (e) {
        e.preventDefault();

        if (vents.items.productos.length === 0) {
            message_error('Debe al menos tener un item en su detalle de venta');
            return false;
        }
        vents.items.fecha_compra = $('input[name="fecha_compra"]').val();
        vents.items.cliente = $('select[name="cliente"]').val();
        vents.items.metodoPago = $('select[name="metodoPago"]').val();
        var parameters = new FormData();
        parameters.append('action', $('input[name="action"]').val());
        parameters.append('vents', JSON.stringify(vents.items));

        submit_with_ajax(window.location.pathname, 'Notificación', '¿Estas seguro de realizar la siguiente acción?', parameters, function () {
            location.href = '/Venta/add/';
        });
    });
     // search products
    $('select[name="search"]').select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            url: window.location.pathname,
            data: function (params) {
                var queryParameters = {
                    term: params.term,
                    action: 'search_autocomplete',
                    ids: JSON.stringify(vents.get_ids())
                }
                return queryParameters;
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
        templateResult: formatRepo,
    }).on('select2:select', function (e) {
        var data = e.params.data;
        if (!Number.isInteger(data.id)) {
            return false;
        }
        data.cant = 1;
        data.subtotal = 0.00;
        vents.add(data);
        $(this).val('').trigger('change.select2');
    });
    vents.list(); 

});

