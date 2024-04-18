from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from .forms import ProductForm
from django.views.decorators.http import require_POST, require_http_methods
from django.db.models import Count


def index(request):
    return render(request, 'products/index.html')


def products(request):
    sort = request.GET.get('sort', '')
    if sort == 'likes':
        products = Product.objects.annotate(counts=Count(
            'like_users')).order_by('-counts', '-pk')
        context = {'products': products}
        return render(request, 'products/products.html', context)
    else:
        products = Product.objects.all().order_by('-pk')
        context = {'products': products}
        return render(request, 'products/products.html', context)


@require_http_methods(["GET", "POST"])
def create(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.author = request.user
                product.save()
                return redirect('products:product_detail', product.pk)
        else:
            form = ProductForm()
        context = {'form': form}
        return render(request, 'products/create.html', context)
    return redirect('accounts:login')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)


@require_http_methods(["GET", "POST"])
def product_update(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.author == request.user:
            if request.method == "POST":
                form = ProductForm(request.POST, instance=product)
                if form.is_valid():
                    product = form.save()
                    return redirect('products:product_detail', product.pk)
            else:
                form = ProductForm(instance=product)
            context = {
                'form': form,
                'product': product,
            }
            return render(request, 'products/product_update.html', context)
        return redirect('products:product_detail', product.pk)
    return redirect('accounts:login')


@require_POST
def product_delete(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.author == request.user:
            product.delete()
            return redirect('products:products')
        return redirect('products:product_detail', product.pk)
    return redirect('accounts:login')


@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
        else:
            product.like_users.add(request.user)
        return redirect('products:product_detail', product.pk)
    return redirect('products:login')
