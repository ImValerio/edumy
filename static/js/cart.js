window.onload = () => {
    let updateBtns = document.getElementsByClassName('cart-update');
    let publishBtns = document.getElementsByClassName('publish-course');
    const notificationsBtn = document.getElementById('notifications-btn');

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

    for(let btn of publishBtns) {
        btn.addEventListener('click', async (e) => {
           const courseId = btn.dataset.course;
           await fetch(`${courseId}/publish`);

           document.querySelector('.button-modal').innerText = 'published';
           document.querySelector('.button-modal').classList = 'mr-3 text-success font-weight-bold bg-transparent border-0';
           $('#exampleModal').modal('hide');

        })
    }

    notificationsBtn.addEventListener('click',async ()=>{
        const userId = notificationsBtn.dataset.user;
        await fetch(`/${userId}/readNotifications`);
    })
}

