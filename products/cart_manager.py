class CartManager:
    def __init__(self, request):
        self.request = request
        self.cart = self.request.session.get('cart', {})

    def save(self):
        """Sepeti oturuma kaydeder."""
        self.request.session['cart'] = self.cart
        self.request.session.modified = True

    def add_to_cart(self, product_id, measure=None):
        """Ürünü sepete ekler veya miktarını artırır."""
        key = f"{product_id}_{measure.strip()}" if measure and isinstance(measure, str) else str(product_id)
        
        if key in self.cart:
            self.cart[key]['quantity'] += 1
        else:
            self.cart[key] = {
                'product_id': product_id,
                'measure': measure,
                'quantity': 1,
                'key':key
            }
        self.save()

    def remove_from_cart(self, key):
        """Ürünü sepetten key ile çıkarır."""
        if key in self.cart:
            del self.cart[key]
            self.save()

    def update_quantity(self, key, increment=True):
        """Ürün miktarını artırır veya azaltır."""
        if key in self.cart:
            if increment:
                self.cart[key]['quantity'] += 1
            else:
                self.cart[key]['quantity'] -= 1
                if self.cart[key]['quantity'] <= 0:
                    del self.cart[key]
            self.save()

    def get_cart_summary(self):
        """Sepet içeriği ve toplam bilgilerini döndürür."""
        from .models import Product
        cart_items = []
        total_quantity = 0
        total_price = 0
        total_miktar = 0
        top = 0
        top_money = 0
        whatsapp_message = "Sepet Özeti:%0A"

        # Ürünleri filtrele
        product_ids = [item['product_id'] for item in self.cart.values()]
        products = Product.objects.filter(id__in=product_ids)

        for product in products:
            # Tüm ürün-measure kombinasyonlarını kontrol et
            for key, item in self.cart.items():
                if item['product_id'] == product.id:
                    measure = item.get('measure', 'Belirtilmemiş')
                    quantity = item['quantity']
                    subtotal = product.price * quantity
                    total_quantity += quantity
                    total_price += subtotal
                    total_miktar = product.quantity * quantity
                    top += total_miktar

                    if top_money != "Teklif Alın":
                        if subtotal == 0:
                            top_money = "Teklif Alın"
                        else:
                            top_money += subtotal

                    # WhatsApp mesajını genişlet
                    whatsapp_message += f"%0A- {product.name} ({measure}) - {total_miktar} adet - "
                    whatsapp_message += f"{subtotal} TL%0A" if subtotal > 0 else "Teklif Alın%0A"

                    cart_items.append({
                        'key': key,  # Key'i sepet işlemleri için kullan
                        'id': product.id,
                        'slug': product.slug,
                        'name': product.name,
                        'measure': measure,
                        'image': product.main_image.url if product.main_image else '',
                        'price': product.price,
                        'quantity': quantity,
                        'miktar': total_miktar,
                        'subtotal': subtotal,
                    })

        # Yüzdelik hesaplama
        top_percentage = (top / 1000) * 100
        if top_percentage > 100:
            top_percentage = 100

        # WhatsApp mesajına toplam bilgileri ekle
        whatsapp_message += f"%0AToplam Adet: {top}%0A"
        whatsapp_message += f"Toplam Fiyat: {top_money if top_money == 'Teklif Alın' else f'{top_money} TL'}"
        if top_money == "Teklif Alın":
            whatsapp_message += (
                f"%0A%0ASepetimde fiyatı belirtilmeyen ürünler bulunmaktadır. "
                f"Bu ürünler için fiyat bilgisi rica ediyorum. Teşekkürler!"
            )
        else:
            whatsapp_message += (
                f"%0A%0Awww.kiliccivata.com adresinden geliyorum. Yukarıda belirtilen ürünleri sipariş vermek istiyorum. "
                f"Lütfen tarafıma geri dönüş yapar mısınız?"
            )

        whatsapp_url = f"https://wa.me/905332646598?text={whatsapp_message.replace(' ', '%20')}"

        return {
            'items': cart_items,
            'total_quantity': total_quantity,
            'total_price': total_price,
            'top': top,
            'top_percentage': top_percentage,
            'top_money': top_money,
            'whatsapp_url': whatsapp_url,
        }