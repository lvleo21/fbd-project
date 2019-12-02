from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse


class Endereco(models.Model):
    rua = models.CharField(max_length=200)
    numero = models.IntegerField(verbose_name = "Número")
    complemento = models.CharField(max_length=200)
    bairro = models.CharField(max_length=50)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    pais = models.CharField(max_length=2, help_text="EX.: BR", verbose_name = "País")

    class Meta:
        verbose_name_plural = "Endereços"

    def __str__(self):
        return self.rua


class Produto(models.Model):

    CATEGORIA_CHOICE = (
        ("refeicao", "Refeição"),
        ("bebida", "Bebida"),
        ("sobremesas", "Sobremesa"),
    )

    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, null=True, blank=True)
    valor = models.DecimalField(decimal_places=2,max_digits=8)
    categoria_produto  = models.CharField(max_length=50, choices=CATEGORIA_CHOICE, verbose_name = "Categoria")
    observacoes = models.TextField()
    data_validade = models.DateTimeField()
    peso = models.DecimalField(decimal_places=3,max_digits=5, help_text="(g)")
    restaurante = models.ManyToManyField("Delivery", related_name="get_deliverys")
    pedido = models.ManyToManyField("Pedido", blank=True, null  = True, related_name="getPedido")
    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)
    qnt = models.IntegerField(verbose_name="Quantidade", null=True, blank=True)


    class Meta:
        verbose_name_plural = "Produtos"
        verbose_name = "Produto"

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse ("listProdutoDetail", args=[self.slug])



class Cliente(models.Model):

    GENERO_CHOICES = (
        ("M", "Masculino"),
        ("F", "Feminino"),
        ("O", "Outro"),
    )

    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, help_text="EX.:nome-segundo", null = True, blank=True)
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    cpf = models.CharField(max_length=11, help_text="EX.: 99999999999")
    idade = models.IntegerField()
    endereco = models.ManyToManyField(Endereco)
    
    telefone1 = models.CharField(max_length=14, help_text="EX.:99999999999999")
    telefone2 = models.CharField(max_length=14, null=True, blank=True, help_text="EX.:9999999999999")

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="get_cliente")
    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)


    class Meta:
        verbose_name_plural = "Clientes"

    def __str__(self):
        return self.nome



class Delivery(models.Model):
    nome_restaurante = models.CharField(max_length=100, help_text="Nome do Delivery: ")
    slug = models.SlugField(max_length=250, help_text="EX.:nome-segundo")
    
    cnpj = models.CharField(max_length=18, help_text="99.999.999/9999-99", verbose_name="CNPJ")
    endereco = models.ManyToManyField(Endereco)
    descricao = models.TextField(verbose_name="Descrição")

    telefone1 = models.CharField(max_length=14, help_text="EX.:99999999999999")
    telefone2 = models.CharField(max_length=14, null=True, blank=True, help_text="EX.:9999999999999")

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="get_delivery")

    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)

    class Meta:
        verbose_name_plural = "Delivery's"

    def __str__(self):
        return self.nome_restaurante

    def get_absolute_url(self):
        return reverse ("listProdutos", args=[self.slug])
    
    


class Pedido(models.Model):

    STATUS_CHOICE = ( 
        ("1","Pagamento Pendente"),
        ("2","Pagamento Realizado"),
    )
    
    ENTREGA_CHOICE = (
        ("1", "Preparando"),
        ("2", "A Caminho"),
        ("3", "Entregue"),
    )

    entregador = models.ManyToManyField("Entregador", blank=True , null=True)
    quantidade_itens = models.IntegerField(blank=True , null=True)
    status_pedido = models.BooleanField(default=False)  
    entrega = models.CharField(max_length=50, choices=ENTREGA_CHOICE)
    endereco_entrega = models.ManyToManyField(Endereco, blank=True , null=True)
    valor_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null = True)
    cliente = models.OneToOneField(Cliente,  blank=True, null = True, on_delete= models.PROTECT, related_name="getCliente")
    status_pagamento = models.CharField(max_length=50, choices=STATUS_CHOICE, blank=True, null = True)
    
    class Meta:
        verbose_name_plural = "Pedidos"

    def __str__(self):
        return "Pedido: nº{}".format(self.pk)


class Entregador(models.Model):
    nome = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250, help_text="EX.:nome-segundo")
    cpf = models.CharField(max_length=11, help_text="EX.: 99999999999")
    
    telefone1 = models.CharField(max_length=14, help_text="EX.:99999999999999")
    telefone2 = models.CharField(max_length=14, null=True, blank=True, help_text="EX.:9999999999999")

    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT, related_name="get_entregador")
    img = models.ImageField(help_text="Tamanho máximo 50x50", verbose_name="Imagem", null = True, blank=True)

    endereco = models.ManyToManyField(Endereco)
    filiado = models.OneToOneField(Delivery, on_delete=models.PROTECT)
    placa_veiculo = models.CharField(max_length=8, verbose_name="Placa do Veículo", help_text="EX.: AAA-9999")


    class Meta:
        verbose_name_plural = "Entregadores"

    def __str__(self):
        return self.nome



@receiver(post_save, sender = Produto)
def insert_slug_pruduto(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)
        return instance.save()

@receiver(post_save, sender = Cliente)
def insert_slug_cliente(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)
        return instance.save()

@receiver(post_save, sender = Delivery)
def insert_slug_delivery(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome_restaurante)
        return instance.save()

@receiver(post_save, sender = Entregador)
def insert_slug_entregador(sender, instance, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.nome)
        return instance.save()