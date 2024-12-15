class CartManager:
    def __init__(self, request):
        self.request = request
        self.cart = self.request.session.get('cart', {})

    def save(self):
        """Sepeti oturuma kaydeder."""
        self.request.session['cart'] = self.cart
        self.request.session.modified = True

    def add_to_cart(self, product_id):
        """Ürünü sepete ekler veya miktarını artırır."""
        product_id = str(product_id)
        if product_id in self.cart:
            self.cart[product_id] += 1
        else:
            self.cart[product_id] = 1
        self.save()

    def remove_from_cart(self, product_id):
        """Ürünü sepetten çıkarır."""
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, increment=True):
        """Ürün miktarını artırır veya azaltır."""
        product_id = str(product_id)
        if product_id in self.cart:
            if increment:
                self.cart[product_id] += 1
            else:
                self.cart[product_id] -= 1
                if self.cart[product_id] <= 0:
                    del self.cart[product_id]
            self.save()

    def get_cart_summary(self):
        """Sepet içeriği ve toplam bilgilerini döndürür."""
        from .models import Product
        products = Product.objects.filter(id__in=self.cart.keys())
        cart_items = []
        total_quantity = 0
        total_price = 0

        for product in products:
            quantity = self.cart[str(product.id)]
            subtotal = product.price * quantity
            total_quantity += quantity
            total_price += subtotal
            cart_items.append({
                'id': product.id,
                'name': product.name,
                'image': product.main_image.url if product.main_image else '',
                'price': product.price,
                'quantity': quantity,
                'subtotal': subtotal,
            })

        return {
            'items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
        }
