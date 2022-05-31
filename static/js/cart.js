window.onload = () => {
    let updateBtns = document.getElementsByClassName('cart-update')
    console.log(updateBtns)
    for(let btn of updateBtns) {
        console.log(btn)
        btn.addEventListener('click', async (e) => {
            const prodId = btn.dataset.product
            const op = btn.dataset.action
            const res = await fetch(`../cart/${op}/${prodId}`)
            btn.parentElement.parentElement.remove();
            console.log(res)
        })
    }
}

