 // Agrega el siguiente código JavaScript en tu página HTML o archivo .js

        // Función para abrir el popup del botón de pago de PayPal
        function openPayPalPopup() {
            // Configura las opciones del botón de pago de PayPal
            paypal.Buttons({
                createOrder: function(data, actions) {
                    // Configura y devuelve el objeto de orden de PayPal
                    return actions.order.create({
                        purchase_units: [{
                            amount: {
                                value: '20.00',
                                currency_code: 'USD'
                            },
                            // Otros detalles de la compra
                            item_name: 'Product 1',
                            invoice: generateUUID(),
                            // ...
                        }]
                    });
                },
                onApprove: function(data, actions) {
                    // Ejecuta alguna acción después de que el pago es aprobado
                    // Por ejemplo, muestra un mensaje de éxito y redirige a una página
                    // personalizada para completar la transacción
                    window.location.href = '/paypal-return';
                },
                onCancel: function(data) {
                    // Ejecuta alguna acción cuando el usuario cancela el pago
                    // Por ejemplo, muestra un mensaje de cancelación y redirige a una página
                    // personalizada para gestionar el cancelamiento
                    window.location.href = '/paypal-cancel';
                }
            }).render('#paypal-button-container');
        }
        
        // Genera un UUID único para el campo 'invoice' de la orden
        function generateUUID() {
            return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                var r = Math.random() * 16 | 0,
                    v = c === 'x' ? r : (r & 0x3 | 0x8);
                return v.toString(16);
            });
        }
        
        // Llama a la función para abrir el popup del botón de pago de PayPal
        openPayPalPopup();