function getCsrfToken() {
    const tokenElement = document.querySelector('input[name="csrfmiddlewaretoken"]');
    if (tokenElement) {
        return tokenElement.value;
    } else {
        console.error('CSRF token bulunamadı.');
        return null;
    }
}

function addToCart(productId) {
    console.log("Adding product to cart:", productId); // Test için
    fetch(`/add-to-cart/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        console.log('Response:', response);
        return response.json();
    })
    .then(data => {
        console.log('JSON Data:', data);

        // Sepete eklendi mesajını göster
        const messageBox = document.createElement('div');
        messageBox.textContent = 'Ürün sepete eklendi!';
        messageBox.style.position = 'fixed';
        messageBox.style.bottom = '20px';
        messageBox.style.right = '20px';
        messageBox.style.padding = '10px 20px';
        messageBox.style.backgroundColor = '#4caf50';
        messageBox.style.color = 'white';
        messageBox.style.borderRadius = '5px';
        messageBox.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
        messageBox.style.zIndex = '1000';

        document.body.appendChild(messageBox);

        // Mesajı 3 saniye sonra kaldır
        setTimeout(() => {
            messageBox.remove();
        }, 3000);
    })
    .catch(error => console.error('Fetch error:', error));
}
function updateCartQuantity(productId, action) {
    fetch(`/update-cart/${productId}/${action}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Ürün miktarı güncellendi:', data.cart);

            // Sayfayı yenile
            location.reload();
        } else {
            console.error('Ürün miktarı güncellenemedi:', data.message);
            alert(data.message || 'Bir hata oluştu.');
        }
    })
    .catch(error => console.error('Fetch hatası:', error));
}

function removeFromCart(productId) {
    fetch(`/remove-from-cart/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken(),
            'Content-Type': 'application/json',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Sepetten kaldırıldı mesajını göster
            const messageBox = document.createElement('div');
            messageBox.textContent = 'Ürün sepetten kaldırıldı!';
            messageBox.style.position = 'fixed';
            messageBox.style.bottom = '20px';
            messageBox.style.right = '20px';
            messageBox.style.padding = '10px 20px';
            messageBox.style.backgroundColor = '#f44336';
            messageBox.style.color = 'white';
            messageBox.style.borderRadius = '5px';
            messageBox.style.boxShadow = '0 4px 8px rgba(0, 0, 0, 0.2)';
            messageBox.style.zIndex = '1000';

            document.body.appendChild(messageBox);

            // Mesajı 1 saniye sonra kaldır
            setTimeout(() => {
                messageBox.remove();
                location.reload(); // Sayfayı yeniden yükle
            }, 1000);
        } else {
            alert('Bir hata oluştu.');
        }
    })
    .catch(error => console.error('Fetch error:', error));
}