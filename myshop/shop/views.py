from .models import Category, Product
from cart.forms import CartAddProductForm
from .recommender import Recommender
from django.shortcuts import render, get_object_or_404
from like_and_rating.models import ProductLike  
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Exists, OuterRef, Value, BooleanField, Avg  
from django.db.models.functions import Coalesce

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    products = products.annotate(
        avg_rating=Coalesce(Avg('reviews__rating'), Value(0.0)))

    # Аннотируем, лайкнул ли текущий пользователь
    if request.user.is_authenticated:
        products = products.annotate(
            user_liked=Exists(
                ProductLike.objects.filter(
                    user=request.user,
                    product=OuterRef('pk')
                )
            )
        )
    else:
        
        products = products.annotate(
            user_liked=Value(False, output_field=BooleanField())
        )

    # Сортировка: сначала лайкнутые пользователем
    products = products.order_by('-user_liked')

  
    paginator = Paginator(products, 3)
    page = request.GET.get('page')
    products_only = request.GET.get('products_only')

    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        if products_only:
            return HttpResponse('')
        products_page = paginator.page(paginator.num_pages)

    # Для AJAX-запросов
    if products_only:
        return render(request, 'shop/product/list_products.html', {
            'products': products_page,
        })

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products_page,
    })
def product_detail(request, id, slug):
    product = get_object_or_404(Product, 
                                id=id, slug=slug,
                                available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product],
                                                 max_results=4)
    product_with_rating = Product.objects.filter(id=product.id).annotate(
        avg_rating=Coalesce(Avg('reviews__rating'), Value(0.0))
    ).first()
    
   
    product.avg_rating = product_with_rating.avg_rating
    
    return render(request, 'shop/product/detail.html', 
                  {'product': product,
                   'cart_product_form': cart_product_form,
                   'recommended_products': recommended_products})

# Create your views here.
