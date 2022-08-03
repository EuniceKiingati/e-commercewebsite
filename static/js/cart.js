function updateUserorder(productId, action){
    console.log('user is logged in, sending data...')
    var url='/update_item/'
    // the url above is where we wanna send data to
    fetch(url, {
        method:'POST',
        headers:{
            'Content-Type':'application/json',
            'X-CSRFToken':csrftoken,
        },
        body:JSON.stringify({'productId':productId, 'action': action})//need to send data as a string
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

//validate phone number in phone form field
function validatePhoneNumber(input_str) {
    var re = '^(?:254|\+254|0)?((?:(?:7(?:(?:[01249][0-9])|(?:5[789])|(?:6[89])))|(?:1(?:[1][0-5])))[0-9]{6})$'
    
  
    return re.test(input_str);
  }
  function validateForm(event) {
    var phone = document.getElementById('myform_phone').value;
    if (!validatePhoneNumber(phone)) {
  
  document.getElementById('phone_error').classList.remove('hidden');
    } else {
        
        document.getElementById('phone_error').classList.add('hidden');
        alert("Phone number valid")
    }
    event.preventDefault();
  }