from django.contrib import admin

from .models import *

admin.site.register(Delivery)
admin.site.register(Usuario)
admin.site.register(Pedido)
admin.site.register(Cliente)
admin.site.register(Endereco)
admin.site.register(Produto)