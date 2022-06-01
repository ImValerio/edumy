window.onload = () => {
    let updateBtns = document.getElementsByClassName('cart-update');

    for(let btn of updateBtns) {
        btn.addEventListener('click', async (e) => {
            const prodId = btn.dataset.product;
            const op = btn.dataset.action;
            await fetch(`../cart/${op}/${prodId}`);

            if (op === 'remove'){
                const priceElement = document.getElementById('tot-price');
                const totPrice = Number(priceElement.innerText);
                const newPrice = totPrice - Number(btn.dataset.price);
                newPrice > 0 ?
                    priceElement.innerText = newPrice.toString() : priceElement.parentElement.innerText = 'The cart is empty...';
            }

            btn.parentElement.parentElement.remove();

        })
    }
}

