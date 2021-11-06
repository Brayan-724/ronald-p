import os


from flask import Flask, render_template, session, request, redirect, jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from collections import deque
from helpers import login_demanding

app = Flask(__name__)
app.config["SECRET_KEY"] = "my secret key"
socketio = SocketIO(app)


channelsnew = []
peoplelog = []
channelsmsg = dict()



#channelsnew Guarsa los canales.
#peoplelog Guarda los usuarios que han entrado.
#Instancia del dict.


@app.route("/")
@login_demanding
def index():
    return render_template("index.html", channels=channelsnew)

@app.route("/login", methods=['GET','POST'])
def login():

    #Guarda el usuario en el form

    session.clear()
    #Olvida cada username en este caso.
    username = request.form.get("username")
    
    if request.method == "POST":

        if len(username) < 1 or username == '':
            return render_template("bad.html", message="El nombre de usuario no puede estar vacía")

        if username in peoplelog:
            return render_template("bad.html", message="El usuario ya exite")
        peoplelog.append(username)

        session['username'] = username

        #Recuerda el usuario de sesión
        session.permanent = True

        return redirect("/")
    else:
        return render_template("login.html")

@app.route("/getchannel/<channel>", methods=['GET'])
def get_channel(channel):
    exists = channel in channelsnew
    status_ = 200 if exists else 404
    return app.response_class(
        response="",
        status=status_
    )

@app.route("/logout", methods=['GET'])
def logout():
    # Remove from list
    try:
        peoplelog.remove(session['username'])
    except ValueError:
        pass
    session.clear()
    return redirect("/")


@app.route("/new", methods=['POST'])
def create():
    """ Create a channel and redirect to its page """
    # Obtiene un canal del form
    nuevocanal = request.form.get("channel")

    if nuevocanal in channelsnew:
        return render_template("bad.html", message=" Este canal ya existe ")
    channelsnew.append(nuevocanal)
    #Cada canal esta en deque y tambien está el metodo popleft
    channelsmsg[nuevocanal] = deque()
    #Agrega canales al dict
    return redirect("/channels/" + nuevocanal)


@app.route("/channels/<channel>", methods=['GET','POST'])
@login_demanding
def enter_channel(channel):
# Updates user current channel y muestra la página del canal para enviar y recibir mensajes en el canal.
    session['current_channel'] = channel
    if request.method == "POST":
        return redirect("/")
    else:
        return render_template("canal.html", channels= channelsnew, messages=channelsmsg[channel])

@socketio.on("afiliado", namespace='/')
def afiliado():
#Aqui es la función para enviar mensajes.
    room = session.get('current_channel')

    join_room(room)
    
    emit('estado', {
        'userafiliado': session.get('username'),
        'channel': room,
        'msg': session.get('username') + ' has entered the channel'}, 
        room=room) #Es el json como tal. las propiedades.





@socketio.on("salir", namespace='/')
def salir():
    """ enviar mensajes to announce that user has salir the channel """

    room = session.get('current_channel')

    leave_room(room)

    emit('estado', {
        'msg': session.get('username') + ' has salir the channel'}, 
        room=room) #Es el json como tal. las propiedades.







@socketio.on('enviar mensaje')
#Recibe mensajes con marca de tiempo y transmite en el canal 
def send_msg(msg, timestamp):

    room = session.get('current_channel')

    if len(channelsmsg[room]) > 100: # Pop de los mensajes antiguos.
        channelsmsg[room].popleft()
    # Guarda los primeros 100 canales
    channelsmsg[room].append([timestamp, session.get('username'), msg])
    
    username = session.get('username')
    print(room, timestamp, msg) 

    emit('anuncio', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg}, 
        room=room) #Es el json como tal. las propiedades.
