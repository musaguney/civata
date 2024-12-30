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
        total_miktar = 0
        top = 0
        top_money = 0
        whatsapp_message = "Sepet Özeti:%0A"  # WhatsApp mesajını hazırlamak için başlangıç
        

        for product in products:
            quantity = self.cart[str(product.id)]
            subtotal = product.price * quantity
            total_quantity += quantity
            total_price += subtotal
            total_miktar = product.quantity * quantity
            top += total_miktar 
            # Koşullar:
            if top_money != "Teklif Alın":  # Eğer "Teklif Alın" tetiklenmediyse
                if subtotal == 0:
                    top_money = "Teklif Alın"  # Eğer bir ürünün fiyatı sıfırsa
                else:
                    top_money += subtotal  # Fiyat sıfır değilse toplama devam et
                    
            # WhatsApp mesajını ürün bilgileriyle genişlet
            whatsapp_message += f"%0A- {product.name} ({total_miktar} adet) -  "
            whatsapp_message += f"{subtotal} TL%0A" if subtotal > 0 else "Teklif Alın%0A"
            
            cart_items.append({
                'id': product.id,
                'slug': product.slug,
                'name': product.name,
                'image': product.main_image.url if product.main_image else '',
                'price': product.price,
                'quantity': quantity,
                'miktar': total_miktar,
                'subtotal': subtotal,
            })
            
        # Toplam miktarı yüzdeye dönüştür ve 100'ü geçmesini önle
        top_percentage = (top / 1000) * 100  # 1000'e göre yüzdelik
        if top_percentage > 100:
            top_percentage = 100  # Maksimum %100 olarak sınırla

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
        
        # WhatsApp URL'sini oluştur
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
