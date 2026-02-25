from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Product, ProductLike, ProductReview
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ProductReviewForm
from orders.models import Order
from .forms import ProductReviewForm
from django.http import JsonResponse
from django.core.paginator import Paginator



def product_reviews(request, product_id):

    rating = request.GET.get("rating")
    page = request.GET.get("page", 1)

    reviews = ProductReview.objects.filter(product_id=product_id).order_by("-created_at")

    if rating:
        reviews = reviews.filter(rating=rating)

    paginator = Paginator(reviews, 5)
    page_obj = paginator.get_page(page)

    data = []

    for r in page_obj:
        data.append({
            "user": r.user.username,
            "rating": r.rating,
            "text": r.comment,
            "date": r.created_at.strftime("%Y-%m-%d"),
        })

    return JsonResponse({
        "reviews": data,
        "has_next": page_obj.has_next(),
    })

@login_required
def add_or_edit_review(request, product_id):
    user = request.user
    
    
    has_purchased = Order.objects.filter(
        user=user,
        items__product_id=product_id  
    ).exists()
    
    
    product = get_object_or_404(Product, id=product_id)
    if not has_purchased:
        messages.success(request, "Вы можете оставлять отзывы только на купленные товары")
        return redirect('shop:product_detail', id=product.id, slug=product.slug)
    

    try:
        review = ProductReview.objects.get(user=request.user, product=product)
        is_editing = True
    except ProductReview.DoesNotExist:
        review = None
        is_editing = False
    
    if request.method == 'POST':
        form = ProductReviewForm(request.POST, instance=review)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.product = product
            review.save()
            
            if is_editing:
                messages.success(request, 'Ваш отзыв успешно обновлен!')
            else:
                messages.success(request, 'Спасибо за ваш отзыв!')
            
            return redirect('shop:product_detail', id=product.id, slug=product.slug)
    else:
        form = ProductReviewForm(instance=review)
    
    return render(request, 'add_review.html', {
        'form': form,
        'product': product,
        'is_editing': is_editing,
        'review': review
    })




@login_required
def delete_review(request, product_id):
    """Удаление отзыва"""
    product = get_object_or_404(Product, id=product_id)
    review = get_object_or_404(ProductReview, user=request.user, product=product)
    
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Ваш отзыв удален')
    
    return redirect('shop:product_detail', id=product.id, slug=product.slug)



@require_POST
@login_required
def add_like(request, id):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    product = get_object_or_404(Product, id=id)  
    
    if user_id and action:  
        try:
            user = User.objects.get(id=user_id)  
            
            if action == 'like':
                ProductLike.objects.get_or_create(
                    user=request.user,
                    product=product
                )
                return JsonResponse({'status': 'ok'})
                
            elif action == 'unlike':
                ProductLike.objects.filter(
                    user=request.user,      
                    product=product         
                ).delete()
                return JsonResponse({'status': 'ok'})
                
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    
    return JsonResponse({'status': 'error'})