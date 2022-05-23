from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse, reverse_lazy

from django.views.generic import CreateView,ListView, UpdateView,DeleteView
from Inventario.models import Productos, Categorias, Proveedores
from Inventario.forms import ProductosForm, CategoriasForm, ProveedoresForm

# Create your views here.
class crearProductos(CreateView):
    model = Productos    
    form_class= ProductosForm
    template_name = 'productos/productoModal.html'
    paginate_by = 2
    success_url = reverse_lazy('inventario')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):        
        context = {}
        context['title'] = 'INVENTARIO DE PRODUCTOS'
        context['productos'] = self.get_queryset()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):        
        return render(request,self.template_name,self.get_context_data())

class listaProductos(ListView):
    model = Productos    
    form_class= ProductosForm
    template_name = 'productos/productos.html'
    

    def get_queryset(self):
        return self.model.objects.get_queryset().order_by('id')

    def get_context_data(self,*args, **kwargs):        
        context = {}
        context['title'] = 'INVENTARIO DE PRODUCTOS'
        context['productos'] = self.get_queryset()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):              
        return render(request,self.template_name,self.get_context_data())

class ProductoUpdate(UpdateView):
    model = Productos
    form_class = ProductosForm
    template_name = 'productos/producto_editModal.html'
    success_url = reverse_lazy('inventario')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Editar Producto'
        context['productos'] = Productos.objects.all()        
        return context

class deleteProducto(DeleteView):
    model = Productos
    template_name = 'productos/producto_eliminarModal.html'

    def post(self, request,pk, *args, **kwargs):        
        object = Productos.objects.get(id=pk)
        object.delete()
        return redirect('inventario')
    
@login_required
def create_categoria(request):
    categorias = Categorias.objects.all()
    if request.method=="POST":
        categoria = CategoriasForm(request.POST)
        if categoria.is_valid():
            nombre = categoria.cleaned_data['categoria']
            consulta = Categorias.objects.filter(categoria=nombre)
            if consulta:
                categorias = Categorias.objects.all()
                formulario = CategoriasForm()
                context = {'categorias':categorias,'form':formulario}
                messages.warning(request, 'Ya existe esta categoria')
                return render(request,'categoria/categorias.html',context)
            else:
                
                categoria.save()
                messages.success(request, 'Categoria creada con exito')
        return redirect('categoria')#redirigue a donde deseas

    else:
        categorias = Categorias.objects.all()
        formulario = CategoriasForm()
        context = {'categorias':categorias,'form':formulario}
        return render(request,'categoria/categorias.html',context)

class CategoriaUpdate(UpdateView):
    model = Categorias
    form_class = CategoriasForm
    template_name = 'categoria/editarCategoria.html'
    success_url = reverse_lazy('categoria')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = reverse_lazy('categoria')
        context['action'] = 'edit'

        return context

class deleteCategoria(DeleteView):
    model = Categorias
    template_name = 'categoria/categoria_eliminarModal.html'

    def post(self, request,pk, *args, **kwargs):        
        object = Categorias.objects.get(id=pk)
        object.delete()
        return redirect('categoria')
    
class crearProveedor(CreateView):
    model = Proveedores    
    form_class= ProveedoresForm
    template_name = 'proveedores/proveedorModal.html'
    paginate_by = 2
    success_url = reverse_lazy('proveedores')

    def get_queryset(self):
        return self.model.objects.all()

    def get_context_data(self, **kwargs):        
        context = {}
        context['title'] = 'INVENTARIO DE PROVEEDORES'
        context['proveedores'] = self.get_queryset()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):        
        return render(request,self.template_name,self.get_context_data())

class listaProveedores(ListView):
    model = Proveedores    
    form_class= ProveedoresForm
    template_name = 'proveedores/proveedores.html'
    

    def get_queryset(self):
        return self.model.objects.get_queryset().order_by('id')

    def get_context_data(self,*args, **kwargs):        
        context = {}
        context['title'] = 'INVENTARIO DE PROVEEDORES'
        context['proveedores'] = self.get_queryset()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):              
        return render(request,self.template_name,self.get_context_data())

class ProovedorUpdate(UpdateView):
    model = Proveedores    
    form_class= ProveedoresForm
    template_name = 'proveedores/proveedor_editModal.html'
    success_url = reverse_lazy('proveedores')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)        
        context['title'] = 'Editar Proveedor'
        context['proveedores'] = Proveedores.objects.all()        
        return context

class deleteProovedor(DeleteView):
    model = Proveedores
    template_name = 'proveedores/proveedor_eliminarModal.html'

    def post(self, request,pk, *args, **kwargs):        
        object = Proveedores.objects.get(id=pk)
        object.delete()
        return redirect('proveedores')
  