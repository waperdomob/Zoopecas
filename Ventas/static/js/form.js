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
                    max: 1000000000,
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

    var option = $(
        '<div class="wrapper container">' +
        '<div class="row">' +
        '<div class="col-lg-1">' +
        '<img src="' + repo.image + '" class="img-fluid img-thumbnail d-block mx-auto rounded">' +
        '</div>' +
        '<div class="col-lg-11 text-left shadow-sm">' +
        //'<br>' +
        '<p style="margin-bottom: 0;">' +
        '<b>Nombre:</b> ' + repo.name + '<br>' +
        '<b>Categoría:</b> ' + repo.cat.name + '<br>' +
        '<b>PVP:</b> <span class="badge badge-warning">$' + repo.pvp + '</span>' +
        '</p>' +
        '</div>' +
        '</div>' +
        '</div>');

    return option;
}
$(function () {
    $('.select2').select2({
        theme: "bootstrap4",
        language: 'es'
    });

    $("input[name='descuento']").on('change', function () {
        vents.calculate_invoice();
    })
        .val(0.0);

    // search products
     $('input[name="search"]').autocomplete({
        source: function (request, response) {
            $.ajax({
                url: window.location.pathname,
                type: 'POST',
                data: {
                    'action': 'search_products',
                    'term': request.term
                },
                dataType: 'json',
            }).done(function (data) {
                response(data);
            }).fail(function (jqXHR, textStatus, errorThrown) {
                //alert(textStatus + ': ' + errorThrown);
            }).always(function (data) {

            });
        },
        delay: 500,
        minLength: 1,
        select: function (event, ui) {
            event.preventDefault();
            console.clear();
            ui.item.cant = 1;
            ui.item.subtotal = 0.00;
            vents.add(ui.item);
            $(this).val('');
        }
    }); 
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
    vents.list(); 

});

