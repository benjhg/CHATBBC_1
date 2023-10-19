from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
from flask_app.models.messages import Message
from flask_app.models.games import UserGame
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        # Validar el formulario
        is_valid = User.validate_register(request.form)

        if is_valid:
            # Cifrar la contraseña antes de guardarla en la base de datos
            hashed_password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

            # Crear un diccionario con los datos del usuario
            user_data = {
                "username": request.form['username'],
                "email": request.form['email'],
                "password": hashed_password,
                "alias": request.form['alias']
            }

            # Guardar el usuario en la base de datos
            user_id = User.save(user_data)

            # Establecer la sesión del usuario
            session['user_id'] = user_id

            return redirect('/dashboard')
        else:
            return redirect('/')
    

@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if user and bcrypt.check_password_hash(user.password, request.form['password']):
        session['user_id'] = user.id
        print(session['user_id'])
        return redirect('/dashboard')
    else:
        flash("Correo o Contraseña invalidos ", "danger")
        return redirect('/')


@app.route('/dashboard')
def dashboard():
    # Obtén los mensajes del chat (simulación de mensajes desde la base de datos)
    chat_messages = Message.get_all_messages()
    user_id_sesion = session['user_id']
    return render_template('Dashboard.html', chat_messages=chat_messages, user_id_sesion=user_id_sesion)


@app.route('/user_profile/<int:user_id>')
def user_profile(user_id):
    user = User.obtener_id(user_id)  # Obtén el usuario por su ID desde la base de datos
    
    if user:
        games = UserGame.get_all_games(user_id)
        games_favorite = UserGame.get_user_games(user_id)
        return render_template('show_user.html', user=user, games=games,games_favorite=games_favorite )
    else:
        flash('Usuario no encontrado', 'error')
        return redirect('/dashboard')


# Ruta para agregar un juego a la lista de favoritos del usuario
@app.route('/añadir_juego/<int:game_id>', methods=['POST'])
def add_favorite(game_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión para añadir juegos a tu lista.', 'warning')
        return redirect('/')

    UserGame.add_game_to_user(user_id, game_id)
    flash('Juego añadido a tu lista exitosamente.', 'success')
    return redirect(url_for('user_profile', user_id=user_id))  # Usar url_for para generar la URL dinámicamente


@app.route('/remove_game/<int:game_id>', methods=['POST'])
def remove_game_from_favorites(game_id):
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión para administrar tu lista de favoritos.', 'warning')
        return redirect('/login')

    UserGame.remove_game_from_user(user_id, game_id)
    flash('Juego eliminado de tu lista de favoritos exitosamente.', 'success')
    return redirect(url_for('user_profile', user_id=user_id))


# Ruta para mostrar el formulario de edición de perfil
@app.route('/edit_profile', methods=['GET'])
def edit_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión para editar tu perfil.', 'warning')
        return redirect('/login')
    
    profile_data = User.get_by_id(user_id)  # Utiliza el método adecuado para obtener el usuario de la base de datos
    if not profile_data:
        flash('Usuario no encontrado.', 'error')
        return render_template('edit_profile.html', profile_data=profile_data)  # O a la página que corresponda en tu aplicación


@app.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Debes iniciar sesión para editar tu perfil.', 'warning')
        return redirect('/login')

    # Obtén los datos del formulario
    new_username = request.form.get('username')
    new_email = request.form.get('email')
    new_alias = request.form.get('alias')
    new_password = request.form.get('password')

    # Actualiza el perfil del usuario en la base de datos (utiliza el método adecuado)
    updated = User.update_user_profile(user_id, new_username, new_email, new_alias, new_password)

    if updated:
        flash('Perfil actualizado exitosamente.', 'success')
    else:
        flash('Error al actualizar el perfil. Por favor, inténtalo de nuevo.', 'error')

    return redirect(url_for('user_profile', user_id=user_id))



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')