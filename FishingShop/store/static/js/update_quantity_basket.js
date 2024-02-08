const updateQuantityForms = document.querySelectorAll('.basket__update_quantity_form');
updateQuantityForms.forEach(form => {
    form.addEventListener('change', () => {
        form.submit();
    });
});