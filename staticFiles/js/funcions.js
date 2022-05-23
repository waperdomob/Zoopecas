
const consulta_form = document.getElementById('consulta_form')
const doc_consulta = document.getElementById('id_documento')
const propietarioBtn = document.getElementById('propietario-btn')


consulta_form.addEventListener('submit', e=>{
  
  const csrf2 = document.getElementsByName('csrfmiddlewaretoken')[0].value

  e.preventDefault()
  const consData = new FormData()
  consData.append('csrfmiddlewaretoken',csrf2)
  consData.append('documento', doc_consulta.value)
  
  $.ajax({
    type: 'GET',
    url:'/ajax_search/',
    data: {
      'documento': doc_consulta.value
    },
    success: function (cliente) {
      if (cliente['cliente']) {
        $("#result").html("<p><center><i class='fa-solid fa-check'></i>Propietario Encontrado: " + cliente['cliente'] + " </center></p>")
        $('#mascota-btn').prop('hidden', false);
        $('#propietario-btn').prop('hidden', true);
        document.getElementById("id_propietario").value = cliente['id'];
        $("id_propietario").prop('disabled', true);

      }
       else {
        $("#result").html("<p><center><i class='icon fas fa-ban'></i> Propietario No encontrado</center></p>");
        $('#mascota-btn').prop('hidden', true);
        $('#propietario-btn').prop('hidden', false);

      }
      },
    error: function(error) {
      console.log(error)
      $("#result").html("<p>ups... Algo salió mal</p>")
      },
  })
})
