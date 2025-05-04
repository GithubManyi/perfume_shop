from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q, Avg
from .models import Perfume, Review
from .forms import ReviewForm
from random import choice
from django.contrib import messages



def home(request):
    query = request.GET.get('q')
    
    # Initialize the queryset with all perfumes
    perfumes = Perfume.objects.all()

    # Get all perfumes with a photo and convert to list
    perfumes_with_photos = list(Perfume.objects.filter(photo__isnull=False))

    # Pick one random perfume for the background (if available)
    random_background = choice(perfumes_with_photos) if perfumes_with_photos else None



    # If there is a search query, filter the perfumes based on that
    if query:
        perfumes = perfumes.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(price__icontains=query)
        )

    # Filtering products based on offers and availability
    weekly_offers = perfumes.filter(weekly_offer=True)
    new_arrivals = perfumes.filter(new_arrival=True)
    discounted_products = perfumes.filter(discounted=True)
    
    # Optionally, filter based on availability
    is_available_products = perfumes.filter(is_available=True)
    sold_out_products = perfumes.filter(is_available=False)

    # Order by latest product and annotate with the average rating
    perfumes = perfumes.order_by('-id').annotate(avg_rating=Avg('reviews__rating'))

    # Prepare context for rendering
    context = {
        'perfumes': perfumes,
        'weekly_offers': weekly_offers,
        'new_arrivals': new_arrivals,
        'discounted_products': discounted_products,
        'is_available_products': is_available_products,
        'sold_out_products': sold_out_products,
        'query': query,
        'background_perfume': random_background,
    }

    return render(request, 'products/home.html', context)


def product_detail(request, pk):
    perfume = get_object_or_404(Perfume, pk=pk)
    reviews = perfume.reviews.all()
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.perfume = perfume
            new_review.save()
            return redirect('product_detail', pk=pk)

    return render(request, 'products/product_detail.html', {
        'perfume': perfume,
        'reviews': reviews,
        'form': form
    })




# Helper to get cart from session
def get_cart(request):
    return request.session.get('cart', {})

# View: Add to cart


def add_to_cart(request, product_id):
    product = get_object_or_404(Perfume, id=product_id)
    cart = get_cart(request)

    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    request.session.modified = True  # This is crucial
    messages.success(request, f"{product.name} added to cart.")
    return redirect('view_cart')  # Redirect to cart page immediately


# View: Remove from cart
def remove_from_cart(request, product_id):
    cart = get_cart(request)

    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
        messages.success(request, "Item removed from cart.")

    return redirect('view_cart')
#view display cart
def view_cart(request):
    cart = request.session.get('cart', {})
    print(f"DEBUG: Cart contains {len(cart)} product IDs: {list(cart.items())}")
    
    cart_items = []
    total = 0
    missing_products = []

    for product_id, quantity in cart.items():
        try:
            product = Perfume.objects.get(id=product_id)
            subtotal = product.price * quantity
            total += subtotal
            
            # Get image URL with multiple fallbacks
            image_url = None
            if hasattr(product, 'photo') and product.photo:
                try:
                    image_url = product.photo.url
                except ValueError:
                    print(f"DEBUG: Product {product_id} has photo field but no file")
            
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'subtotal': subtotal,
                'image_url': image_url
            })
            
        except Perfume.DoesNotExist:
            print(f"DEBUG: Product ID {product_id} doesn't exist in database")
            missing_products.append(product_id)
            continue
        except Exception as e:
            print(f"DEBUG: Error with product {product_id}: {str(e)}")
            continue

    # Clean up invalid product IDs from session
    for pid in missing_products:
        cart.pop(str(pid), None)
    if missing_products:
        request.session['cart'] = cart
        request.session.modified = True

    context = {
        'cart_items': cart_items,
        'total': total,
        'cart_count': sum(cart.values()),
        'debug_info': {
            'session_cart': cart,
            'missing_products': missing_products,
            'actual_count': len(cart_items)
        }
    }
    return render(request, 'cart.html', context)




def update_cart(request, product_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        cart = get_cart(request)
    
        
        if quantity > 0:
            cart[str(product_id)] = quantity
        else:
            del cart[str(product_id)]
            
        request.session['cart'] = cart
        request.session.modified = True
        messages.success(request, "Cart updated successfully")
    return redirect('view_cart') 


def checkout(request):
    return render(request, 'checkout.html')
