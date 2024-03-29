from . import views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/criarDelivery/", views.criarDeliveryView, name="criarDelivery"),
    path("accounts/criarCliente/", views.criarClienteView, name="criarCliente"),
    path("pedeMais/", views.HomeView, name = 'home'),
    path("pedeMais/delivery/cadastrarEntregador/", views.cadastrarEntregador, name = 'cadastroEntregador'),
    path("pedeMais/delivery/produto/cadastrarProduto/", views.cadastroProduto, name = 'cadastroProduto'),
    path("pedeMais/delivery/produto/ListarProdutosCadastrados/<int:pk>/editar/", views.EditProduto.as_view(), name="editarProduto"),
    path("pedeMais/delivery/produto/ListarProdutosCadastrados/<int:pk>/remover/", views.removerProduto, name = "removerProduto"),
    path("pedeMais/delivery/produto/ListarProdutosCadastrados/", views.ListarProdutosCadastrados, name = 'listarProdutosCadastrados'),
    path("pedeMais/delivery/produto/ListarEntregadoresCadastrados/<slug:slug>/remover/", views.RemoverEntregadorView.as_view(), name = 'removerEntregador'),
    path("pedeMais/delivery/produto/ListarEntregadoresCadastrados/<slug:slug>/editar/", views.EditarEntregadorView, name = 'editarEntregador'),
    
    path("pedeMais/delivery/produto/ListarEntregadoresCadastrados/", views.ListarEntregadoresCadastrados, name = 'listarEntregadoresCadastrados'),
    path('pedeMais/carrinho/editarEndereco/<int:pk>', views.alterarEndereco, name="alterarEndereco"),
    path('pedeMais/carrinho/', views.CarrinhoDeliveryView, name="carrinhoView"),
    path('pedeMais/historicoPedido/', views.HistoricoPedidoView, name="historicoPedido"),
    path('pedeMais/carrinho/remover/<int:pk>/', views.removerItem, name = "excluir"),
    path("pedeMais/listDeliverys/", views.ListDeliveryView, name="listDeliverys"),
    path('pedeMais/listDeliverys/listProdutos/<slug:slug>/', views.ProdutosListView, name="listProdutos"),
    path('pedeMais/listDeliverys/listProdutos/detail/<slug:slug>/', views.ProdutoDetailView, name="listProdutoDetail"),
]

#path("pedeMais/delivery/produto/ListarProdutosCadastrados/editar/<int:pk>/", views.editarProduto, name = 'editarProduto'),