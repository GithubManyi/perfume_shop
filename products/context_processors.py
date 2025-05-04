# your_app/context_processors.py

def cart_item_count(request):
    cart = request.session.get('cart', {})
    total_items = sum(cart.values())  # Sum up the items in the cart
    return {'cart_item_count': total_items}
