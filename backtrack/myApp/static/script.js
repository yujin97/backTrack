let temp = document.querySelector('#temp');

let del = document.getElementsByClassName('delete');

const sth = () => {
	console.log('got you!');
}

const deleteHandler = id => { // For sending get request to the server
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", "http://localhost:8000/orders/customerOrdersDelete?id="+id, true); // need to change the url
	xhttp.send();
}

temp.addEventListener('click', sth);
for(let i =0; i<del.length; i++){
	del[i].addEventListener('click',() => deleteHandler(del[i].id));
}