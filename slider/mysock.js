urlsock = 'ws://localhost:8000/websocketserver';

function make_socket(){
	// Create WebSocket connection.
	const socket = new WebSocket(urlsock);

	// Connection opened
	socket.addEventListener('open', function (event) {
		console.log("Socket Opened!")
		document.querySelector("#btn_connect").setAttribute("disabled", "true");
	});

	// Listen for messages
	socket.addEventListener('message', function (event) {

		msg = event.data;

	    console.log('Message from server ', msg);

	    if( msg.startsWith('url') ){
	    	var url = msg.split("##")[1];
	    	load_doc(url);
	    }

	    if( msg.startsWith('p') ){
	    	page = parseInt(msg.split('p')[1]);
	    	pageNum = page
	    	renderPage(page)
	    }
/*
	    if( msg == 'next' ){
	    	onNextPage();
	    }
	    if( msg == 'prev' ){
			onPrevPage();
	    }
*/
	});

	// Connection closed
	socket.addEventListener('close', function (event) {
		console.log("Socket Closed!")
		document.querySelector("#btn_connect").removeAttribute("disabled");
	});
}