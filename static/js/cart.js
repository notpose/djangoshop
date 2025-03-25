document.addEventListener('DOMContentLoaded', function() {
    console.log('Cart.js loaded');
    // Обработка форм добавления в корзину
    document.querySelectorAll('.add-to-cart-form').forEach(form => {
        console.log('Found cart form:', form);
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Form submitted');
            
            const productId = this.dataset.productId;
            const button = this.querySelector('button');
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            button.disabled = true;
            
            fetch(`/cart/add/${productId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => {
                console.log('Response received:', response);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log('Data received:', data);
                if (data.status === 'success') {
                    // Обновляем бейдж корзины
                    const cartBadge = document.querySelector('.badge.bg-accent.rounded-pill');
                    if (cartBadge) {
                        cartBadge.textContent = data.cart_total + ' ₽';
                    }
                    
                    // Обновляем кнопку
                    button.classList.remove('btn-outline-success');
                    button.classList.add('btn-success');
                } else if (data.status === 'removed') {
                    button.classList.remove('btn-success');
                    button.classList.add('btn-outline-success');
                }
            })
            .catch(error => {
                console.error('Error:', error);
            })
            .finally(() => {
                button.disabled = false;
            });
        });
    });
}); 