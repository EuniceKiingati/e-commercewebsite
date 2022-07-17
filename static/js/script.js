let closer = document.querySelector('#closer');

closer.onclick = () =>{
    closer.style.display = 'none';
    navbar.classList.remove('active');
    cart.classList.remove('active');
    loginForm.classList.remove('active');
}

let navbar = document.querySelector('.navbar');

document.querySelector('#menu-btn').onclick = () =>{
    closer.style.display = 'block';
    navbar.classList.toggle('active');
}

let cart = document.querySelector('.shopping-cart');

document.querySelector('#cart-btn').onclick = () =>{
    closer.style.display = 'block';
    cart.classList.toggle('active');
}

let loginForm = document.querySelector('.login-form');

document.querySelector('#login-btn').onclick = () =>{
    closer.style.display = 'block';
    loginForm.classList.toggle('active');
}

let searchForm = document.querySelector('.header .search-form');

document.querySelector('#search-btn').onclick = () =>{
    searchForm.classList.toggle('active');
}

window.onscroll = () =>{
    searchForm.classList.remove('active');
}

let slides = document.querySelectorAll('.home .slides-container .slide');
let index = 0;

function next(){
    slides[index].classList.remove('active');
    index = (index + 1) % slides.length;
    slides[index].classList.add('active');
}

function prev(){
    slides[index].classList.remove('active');
    index = (index - 1 + slides.length) % slides.length;
    slides[index].classList.add('active');
}


function updateUserorder(productId, action){
    console.log('user is logged in, sending data...')
    var url='/update_item/'

    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action': action})
    })
    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data:', data)
        location.reload()
    })
}


// cart js
var user = '{{ request.user}}'
var updateBtns=document.getElementsByClassName('update-cart')
for(var i=0; i<updateBtns.length; i++){
    updateBtns[i].addEventListener('click', function(){
        var productId=this.dataset.product
        var action=this.dataset.action
        console.log('productId:', productId, 'action:', action)
        console.log('USER:', user )
        if(user==='AnonymousUser'){
            console.log('not logged in')
        }else{
            updateUserorder(productId, action)
        }
    })

}