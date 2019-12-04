from django.views.generic import *
from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.urls import reverse, reverse_lazy
from .form import *

from django.contrib.auth.models import User



def getGroup(pk):
    grupo = User.objects.get(id = pk).groups.all().first().__str__()

    return "c" if grupo == "Cliente" else "d"

def calcularValor(produtos):
    valorTotal = 0
    qntTotal = 0
    for x in produtos:
        valorTotal+=(x.valor*x.qnt)
        qntTotal+=x.qnt
    
    return valorTotal,  qntTotal

def PedidoDeliveryView(request):
    template_name = "delivery/carrinho.html"
    array={}
    array['type'] = getGroup(request.user.pk)

    # array = {}

    # user = User.objects.get(id = request.user.pk)
    # cliente = user.get_cliente.all().first()

    # try :
    #     pedido = Pedido.objects.get(cliente = cliente, status_pedido = False)
    #     produtos = Produto.objects.filter(pedido = pedido).all()
    #     array["objects"] = produtos
    #     valorTotal, qntTotal = calcularValor(produtos)
    #     array["valor"] = valorTotal
    #     array["qnt"] = qntTotal
    #     array["endereco"] = cliente.endereco.first()
    #     array["cliente"] = cliente

    # except :
    #     array["objects"] = "False"


    # if request.POST:

    #     pedido.quantidade_itens = qntTotal
    #     pedido.status_pedido = True
    #     pedido.valor_total = valorTotal

    #     pedido.save()

    #     return redirect("home")
    
    

    return render(request, template_name, array)





        

def ListDeliveryView(request):
    array = {}
    array["objects"] = Delivery.objects.all()
    array['type'] = getGroup(request.user.pk)

    template_name = "delivery/listDeliverys.html"



    return render(request, template_name, array)
    



class ProdutosListView(ListView):
    model = Produto
    template_name = "delivery/listProdutos.html"
    context_object_name = "objects"

    def get_queryset(self, *args, **kwargs):
        delivery = Delivery.objects.get(slug=self.kwargs['slug'])
        produtos = delivery.get_deliverys.all()
        return produtos


def HomeView(request):
        user = User.objects.get(id = request.user.pk)
        cliente = user.getCliente.all().first()
        array = {}
        array["cliente"] = cliente
        array['type'] = getGroup(request.user.pk)
        return render(request, "delivery/home.html", array)
    
class cadastroProduto(CreateView):
    model = Produto
    template_name = "delivery/cadastroProduto.html"
    success_url = reverse_lazy("home")

class ProdutoView(TemplateView):
    template_name = "delivery/viewProduto.html"


def ProdutoDetailView(request, slug):
    template_name = "delivery/listProdutoDetail.html"
    array = {}
    array["objects"] = Produto.objects.get(slug = slug)

    if request.GET:

        user = User.objects.get(id = request.user.pk)
        cliente = user.get_cliente.all().first()

        
        
        try:
            produto = Produto.objects.filter(slug = slug).first()
            pedido = Pedido.objects.filter(cliente = cliente, status_pedido = False).first()
            
            produto.pedido.add(pedido) 
            produto.qnt = request.GET["Quantidade"]
            produto.save()
            return redirect("carrinhoView")

        except:
            produto = Produto.objects.get(slug = slug)
            pedido  = Pedido()
            produto.pedido = pedido

            return redirect("carrinhoView")
            
    return render(request, template_name, array)
    



def criarDeliveryView(request):
    array = {}
    endereco = EnderecoForm(request.POST or None)
    delivery = DeliveryForm(request.POST or None)
    user = UserCreationFormWithEmail(request.POST or None)

    array["endereco"] = endereco
    array["delivery"] = delivery
    array["user"] = user
    array["erro"] = False
    array["mensagem"] = ""

    if request.POST:
        array["erro"] = False
        array["mensagem"] = ""

        # Endereco
        rua = request.POST['rua']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        pais = request.POST['pais']
        # User
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        #Delivery
        nome_restaurante = request.POST["nome_restaurante"]
        cnpj = request.POST["cnpj"]
        descricao  = request.POST["descricao"]
        telefone1 = request.POST["telefone1"]
        telefone2 = request.POST["telefone2"]
        imagem = request.POST["img"]


        
        objEndereco = Endereco.objects.filter(rua=rua, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais).first()
        objUser = User.objects.filter(username=username, password=password1, email=email).first()


        if(objEndereco is None):
            objEndereco = Endereco(rua=rua, numero=numero, complemento=complemento,bairro=bairro, cidade=cidade, estado=estado, pais=pais)
            objEndereco.save()

        
        if(objUser is None):
            objUser = User(username=username, password=password1, email=email)
            objUser.save()
        else:
            array["erro"] = True
            array["mensagem"] = "Usuário existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)



        objDelivery =  Delivery.objects.filter(nome_restaurante=nome_restaurante, cnpj = cnpj, user=objUser, endereco=objEndereco , descricao = descricao).first()

        if(objDelivery is None):

            objDelivery = Delivery(nome_restaurante=nome_restaurante, descricao = descricao, cnpj = cnpj, user=objUser, telefone1 = telefone1, telefone2 = telefone2, img = imagem)
            objDelivery.save()
            objDelivery.endereco.add(objEndereco)
        else:
            
            array["erro"] = True
            array["mensagem"] = "Cliente existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)


    
        
        return redirect("login")
    
    else:
        return render(request,"delivery/cadastroDelivery.html", array)
        




def criarClienteView(request):
    array = {}
    endereco = EnderecoForm(request.POST or None)
    cliente = ClienteForm(request.POST or None)
    user = UserCreationFormWithEmail(request.POST or None)

    array["endereco"] = endereco
    array["cliente"] = cliente
    array["user"] = user
    array["erro"] = False
    array["mensagem"] = ""
    

    if request.POST:

        array["erro"] = False
        array["mensagem"] = ""

        # Endereco
        rua = request.POST['rua']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        bairro = request.POST['bairro']
        cidade = request.POST['cidade']
        estado = request.POST['estado']
        pais = request.POST['pais']
        # User
        username = request.POST["username"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        email = request.POST["email"]
        # Cliente
        nome = request.POST["nome"]
        genero = request.POST["genero"]
        cpf = request.POST["cpf"]
        idade = request.POST["idade"]
        telefone1 = request.POST["telefone1"]
        telefone2 = request.POST["telefone2"]
        imagem = request.POST["img"]


        objEndereco = Endereco.objects.filter(rua=rua, numero=numero, complemento=complemento, bairro=bairro, cidade=cidade, estado=estado, pais=pais).first()
        objUser = User.objects.filter(username=username, password=password1, email=email).first()


        if(objEndereco is None):
            objEndereco = Endereco(rua=rua, numero=numero, complemento=complemento,bairro=bairro, cidade=cidade, estado=estado, pais=pais)
            objEndereco.save()

        
        if(objUser is None):
            objUser = User(username=username, password=password1, email=email)
            objUser.save()
        else:
            array["erro"] = True
            array["mensagem"] = "Usuário existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)
    

        objCliente =  Cliente.objects.filter(nome=nome, genero=genero, cpf=cpf, idade=idade, user=objUser, endereco=objEndereco).first()

        if(objCliente is None):

             

            objCliente = Cliente(nome=nome, genero=genero, cpf=cpf, idade=idade, user=objUser, telefone1 = telefone1, telefone2 = telefone2, img = imagem)
            objCliente.save()
            objCliente.endereco.add(objEndereco)
        else:
            
            array["erro"] = True
            array["mensagem"] = "Cliente existente, tente novamente."
            return render(request,"delivery/cadastroCliente.html", array)
        
        return redirect("login")

    else:

        return render(request,"delivery/cadastroCliente.html", array)




