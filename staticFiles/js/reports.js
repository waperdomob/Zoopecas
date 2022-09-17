var date_range= null;
var metodo_pago = null;
var categoria = null;
var selectedOption = null;
var selectedOption2 = null;
var opcion1 = null;
var opcion2 = null;
var date_now = new moment().format('YYYY-MM-DD');
function generarReporte() {
    var select1 = document.getElementById('id_Metodo_pago');
    var select2 = document.getElementById('id_categoria');

    select1.addEventListener('change',
    function(){
        selectedOption = this.options[select1.selectedIndex];
        opcion1 = selectedOption.value
        });
    select2.addEventListener('change',
    function(){
        selectedOption2 = this.options[select2.selectedIndex];
        opcion2 = selectedOption2.value
        });
    var parameters = {
        'action' : 'search_report',
        'start_date': date_now,
        'end_date': date_now,
        'metodo_pago':metodo_pago,
        'categoria':categoria,

    }
    if (date_range !== null) {
        parameters['start_date'] = date_range.startDate.format('YYYY-MM-DD');
        parameters['end_date'] = date_range.endDate.format('YYYY-MM-DD');
        parameters['metodo_pago'] = opcion1;
        parameters['categoria'] = opcion2;
    }   


    tblSale = $('#data').DataTable({
        responsive: true,
        scrollX: true,
        autoWidth: false,
        destroy: true,
        deferRender: true,
        ajax: {
            url: window.location.pathname,
            type: 'POST',
            data: parameters,
            dataSrc: "",
            headers: {'X-CSRFToken': csrftoken},
        },
        order : false,
        paging: false,
        ordering: false,
        info: false,
        searching: false,
        dom: 'Bfrtip',
        buttons: [
            {
                extend: 'excelHtml5',
                text: 'Descargar Excel <i class="fas fa-file-excel"></i>',
                titleAttr: 'Excel',
                className: 'btn btn-success btn-flat btn-xs'
            },
            {
                extend: 'pdfHtml5',
                text: 'Descargar Pdf <i class="fas fa-file-pdf"></i>',
                titleAttr: 'PDF',
                className: 'btn btn-danger btn-flat btn-xs',
                download: 'open',
                orientation: 'landscape',
                pageSize: 'LEGAL',
                customize: function (doc) {
                    doc.styles = {
                        header: {
                            fontSize: 18,
                            bold: true,
                            alignment: 'center'
                        },
                        subheader: {
                            fontSize: 13,
                            bold: true
                        },
                        quote: {
                            italics: true
                        },
                        small: {
                            fontSize: 8
                        },
                        tableHeader: {
                            bold: true,
                            fontSize: 11,
                            color: 'white',
                            fillColor: '#2d4154',
                            alignment: 'center'
                        }
                    };
                    doc.content[1].margin = [0, 35, 0, 0];
                    doc.content[1].layout = {};
                    doc['footer'] = (function (page, pages) {
                        return {
                            columns: [
                                {
                                    alignment: 'left',
                                    text: ['Fecha de creación: ', {text: date_now}]
                                },
                                {
                                    alignment: 'right',
                                    text: ['página ', {text: page.toString()}, ' de ', {text: pages.toString()}]
                                }
                            ],
                            margin: 20
                        }
                    });

                }
            },
        ],

        columnDefs: [
            {
                targets: [-1,-2, -3],
                class: 'text-center',
                orderable: false,
                render: function (data, type, row) {
                    return '$' + parseFloat(data).toFixed(2);
                }
            },
        ],
        initComplete: function (settings, json) {

        }
    });
}

$(function () {
    $('input[name="date_range"]').daterangepicker(options = {
        locale: {
            format : 'YYYY-MM-DD',
            applyLabel: '<i class="fas fa-chart-pie"></i>Applicar',
            cancelLabel: '<i class="fas fa-times"></i>Cancelelar',
        }
    }).on('apply.daterangepicker', function(ev, picker) {
        date_range = picker;
        generarReporte();
    }).on('cancel.daterangepicker', function(ev, picker) {
        $(this).data('daterangepicker').setStartDate(date_now);
        $(this).data('daterangepicker').setEndDate(date_now);
        date_range =picker;
        generarReporte();

    });
    generarReporte();
   
});

