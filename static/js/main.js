/* === SCRIPT PRINCIPAL DE SUPERMARKET v2 === */
document.addEventListener('DOMContentLoaded', () => {
    
    // --- 1. LÓGICA DEL CARRITO (ROBUSTA) ---
    
    // Cargar carrito desde localStorage
    let cart = {};
    try {
        const storedCart = localStorage.getItem('shoppingCartData');
        if (storedCart) {
            cart = JSON.parse(storedCart);
        }
    } catch (e) {
        console.error("Error al cargar el carrito de localStorage:", e);
    }

    // Seleccionar elementos del DOM (solo si existen)
    const productCards = document.querySelectorAll('.product-card');
    const cartItemsList = document.getElementById('cart-items-list');
    const cartTotalPrice = document.getElementById('cart-total-price');
    const headerCartTotal = document.getElementById('header-cart-total');
    const checkoutBtn = document.getElementById('checkout-btn');

    // Función para guardar en localStorage
    function saveCart() {
        const cartDataToStore = Object.fromEntries(
            Object.entries(cart).filter(([, product]) => product.quantity > 0)
        );
        localStorage.setItem('shoppingCartData', JSON.stringify(cartDataToStore));
    }

    // --- *** FUNCIÓN updateCartView ACTUALIZADA *** ---
    function updateCartView() {
        if (!cartItemsList) {
            return; 
        }

        cartItemsList.innerHTML = ''; // Limpiar vista
        let grandTotal = 0;
        const productIds = Object.keys(cart);

        if (productIds.length === 0 || productIds.every(id => cart[id].quantity === 0)) {
            cartItemsList.innerHTML = '<p class="cart-empty-message">Tu carrito está vacío.</p>';
            if (checkoutBtn) checkoutBtn.style.display = 'none';
            grandTotal = 0;
            // Clear cart from object if all quantities became 0 somehow
            cart = {}; 
            localStorage.removeItem('shoppingCartData');
        } else {
            if (checkoutBtn) checkoutBtn.style.display = 'block';
            productIds.forEach(id => {
                const product = cart[id];
                if (product.quantity > 0) {
                    const itemTotal = product.price * product.quantity;
                    grandTotal += itemTotal;
                    
                    const cartItem = document.createElement('div');
                    cartItem.className = 'cart-item';
                    // ** AÑADIDO: Imagen y Botón Eliminar **
                    cartItem.innerHTML = `
                        <img src="${product.imageUrl || ''}" alt="${product.name}" class="cart-item-image">
                        <div class="cart-item-details">
                            <span class="cart-item-name">${product.name} (x${product.quantity})</span>
                            <span class="cart-item-price">$${itemTotal.toFixed(2)}</span>
                        </div>
                        <button class="cart-item-remove" data-id="${id}">&times;</button> 
                    `; // &times; es el símbolo '×'
                    cartItemsList.appendChild(cartItem);

                    // ** AÑADIDO: Listener para el botón eliminar **
                    const removeButton = cartItem.querySelector('.cart-item-remove');
                    if(removeButton){
                        removeButton.addEventListener('click', (event) => {
                            const productIdToRemove = event.target.getAttribute('data-id');
                            if (productIdToRemove && cart[productIdToRemove]) {
                                delete cart[productIdToRemove]; // Elimina del objeto cart
                                updateCartView(); // Actualiza la vista
                                // saveCart() se llama dentro de updateCartView
                            }
                        });
                    }
                } else {
                    // Si la cantidad es 0, nos aseguramos de eliminarlo del objeto
                    delete cart[id];
                }
            });
        }

        const formattedTotal = `$${grandTotal.toFixed(2)}`;
        if (cartTotalPrice) cartTotalPrice.textContent = formattedTotal;
        if (headerCartTotal) headerCartTotal.textContent = formattedTotal;
        
        saveCart(); // Guarda el estado final (con posibles eliminaciones)
    }

    // Lógica para agregar productos (ROBUSTA)
    productCards.forEach(card => {
        const plusBtn = card.querySelector('.plus');
        const minusBtn = card.querySelector('.minus');
        const quantityDisplay = card.querySelector('.quantity-display');
        const addToCartBtn = card.querySelector('.add-to-cart-btn');
        let quantity = 0;

        if (plusBtn && minusBtn && quantityDisplay && addToCartBtn) {
            const id = card.dataset.id;
            // Initialize display based on cart, if item already exists
            if (cart[id]) {
                 // We keep quantity 0 locally on card, display reflects cart total later
            } else {
                 quantityDisplay.textContent = 0; // Ensure it starts at 0 if not in cart
            }


            plusBtn.addEventListener('click', () => {
                quantity++;
                quantityDisplay.textContent = quantity;
            });

            minusBtn.addEventListener('click', () => {
                if (quantity > 0) {
                    quantity--;
                    quantityDisplay.textContent = quantity;
                }
            });

            addToCartBtn.addEventListener('click', () => {
                if (quantity === 0) return;
                const name = card.dataset.name;
                const price = parseFloat(card.dataset.price);
                // ** AÑADIDO: Obtener URL de imagen **
                const imageUrl = card.dataset.imageUrl; 

                if (!id || !name || isNaN(price) || !imageUrl) { // Check for imageUrl too
                    console.error('ERROR: Faltan data-id, data-name, data-price o data-image-url', card);
                    return;
                }
                if (cart[id]) {
                    cart[id].quantity += quantity;
                } else {
                    // ** AÑADIDO: Guardar imageUrl en el carrito **
                    cart[id] = { name, price, quantity, imageUrl }; 
                }
                quantity = 0; // Reset card counter
                quantityDisplay.textContent = 0;
                updateCartView(); // Update cart display
            });
        }
    });

    // Actualizar la vista del carrito al cargar la página
    updateCartView(); 

    // --- 2. LÓGICA DEL SIDEBAR (Funciona en todas las páginas) ---
    const menuIcon = document.querySelector('.menu-icon');
    const sidebar = document.getElementById('sidebar-nav');
    const closeBtn = document.getElementById('close-btn');
    const overlay = document.getElementById('sidebar-overlay');

    if (menuIcon && sidebar && closeBtn && overlay) {
        menuIcon.addEventListener('click', () => {
            sidebar.classList.add('active');
            overlay.classList.add('active');
        });
        closeBtn.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
        overlay.addEventListener('click', () => {
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        });
    }
});