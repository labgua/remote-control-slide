urlsock = 'ws://localhost:8000/websocketserver';

function make_socket(){
	// Create WebSocket connection.
	const socket = new WebSocket(urlsock);

	// Connection opened
	socket.addEventListener('open', function (event) {
		console.log("Socket Opened!")
	});

	// Listen for messages
	socket.addEventListener('message', function (event) {

		msg = event.data;

	    console.log('Message from server ', msg);

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
}