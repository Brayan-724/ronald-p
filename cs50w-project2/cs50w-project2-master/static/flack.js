document.addEventListener('DOMContentLoaded', () => {

    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    // When connected, configure button
    socket.on('connect', () => {

        // Notify the server user has joined
        socket.emit('afiliado');

        // Forget user's last channel when clicked on '+ Channel'
        document.querySelector('#nuevocanal').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });
        console.log(document.getElementById("salir2"));

        // When user leaves channel redirect to '/'
        document.getElementById("salir2").addEventListener('click', () => {

            // Notify the server user has left
            socket.emit('salir');

            localStorage.removeItem('last_channel');
            window.location = ('/');
            console.log(window.location);
        })

        // Forget user's last channel when logged out
        document.querySelector('#salir').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        // 'Enter' key on textarea also sends a message
        // https://developer.mozilla.org/en-US/docs/Web/Events/keydown
        document.querySelector('#comment').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });

        // Send button emits a "message sent" event
         document.getElementById("send-button").addEventListener("click", () => {

            // Save time in format HH:MM:SS
            let timestamp = new Date();
            timestamp = timestamp.toLocaleTimeString();

            // Save user input
            let msg = document.getElementById("comment").value;
            console.log(timestamp, msg);
            socket.emit('enviar mensaje', msg, timestamp);

            // Clear input
            document.getElementById("comment").value = '';
        });
    });

    // When user joins a channel, add a message and on users connected.
    socket.on('estado', data => {
        console.log(data);
        // Broadcast message of joined user.
        let row = '<' + `${data.msg}` + '>'
         document.getElementById("chat").value += row + '\n';

        // Save user current channel on localStorage
        localStorage.setItem('last_channel', data.channel)
    })

    // When a message is announced, add it to the textarea.
    socket.on('anuncio', data => {
        console.log(data)
        // Format message
        let row = '<' + `${data.timestamp}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`
        document.getElementById("chat").value += row + '\n'
    })


});