document.addEventListener("DOMContentLoaded", () => {

  const csrfMeta = document.querySelector('meta[name="csrf-token"]');
  if (!csrfMeta) {
    console.error("CSRF token meta not found");
    return;
  }

  const csrftoken = csrfMeta.getAttribute('content');

  document.addEventListener('click', (e) => {

    // + / - quantity
    if (e.target.classList.contains('qty-btn')) {
      const btn = e.target;
      const row = btn.closest('tr');
      const itemId = row.dataset.itemId;
      const action = btn.dataset.action;

      fetch(`/update-quantity/${itemId}/${action}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
      })
      .then(res => res.json())
      .then(data => {
        if (data.quantity === 0) {
          row.remove();
        } else {
          row.querySelector('.qty').innerText = data.quantity;
        }

        document.getElementById('total-qty').innerText = data.total_qty;
        document.getElementById('total-price').innerText = data.total_price;
      })
      .catch(err => console.error(err));
    }

    // Remove item
    if (e.target.classList.contains('remove-btn')) {
      const btn = e.target;
      const row = btn.closest('tr');
      const itemId = row.dataset.itemId;

      fetch(`/remove-from-cart/${itemId}/`, {
        method: 'POST',
        headers: { 'X-CSRFToken': csrftoken }
      })
      .then(res => res.json())
      .then(data => {
        row.remove();
        document.getElementById('total-qty').innerText = data.total_qty;
        document.getElementById('total-price').innerText = data.total_price;
      })
      .catch(err => console.error(err));
    }

  });

});
