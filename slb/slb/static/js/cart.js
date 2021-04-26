var updateBtns = document.getElementsByClassName('update-cart')


for(i = 0; i < updateBtns.length; i++){
	updateBtns[i].addEventListener('click', function(){
		var equipmentId = this.dataset.equipment
		var action = this.dataset.action
		updateUserOrder(equipmentId, action)

	})
}

function addCookieItem(houseId, action){
	console.log('User is not authenticated..')

	if (action == 'add'){
		if(rcart[houseId] == undefined){
			rcart[houseId] = {'quantity':1}
		}else{
			rcart[houseId]['quantity'] += 1  
		}
	}


	if (action == 'remove'){
		rcart[houseId]['quantity'] -= 1

		if(rcart[houseId]['quantity'] <= 0){
			console.log('item should be deleted')
			delete rcart[houseId];
		}
	}

	console.log('rcart:', rcart)

	document.cookie = 'rcart=' + JSON.stringify(rcart) + ";domain;path=/"
	location.reload()

}


function updateUserOrder(equipmentId, action){
	console.log('user is authenticated, sending data.....')

    console.log('houseId: ',equipmentId, 'action:', action)

	// console.log('USER: ',user)
		

	var url = '/update_item/'

	fetch(url, {
		method: 'POST',
		headers:{
			'content-Type': 'application/json',
			'X-CSRFToken':csrftoken,
		},
		body:JSON.stringify({'equipmentId': equipmentId, 'action':action})
	})
	.then((response) => {
		return response.json();

	})
	.then((data) => {
		console.log('data:', data)
		location.reload()
	})
}

