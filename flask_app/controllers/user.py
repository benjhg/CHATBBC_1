from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
from flask_app.models.messages import message
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
        return redirect('/dashboard')
    else:
        flash("Invalid Email or Password", "error")  # Cambiado a 'error'
        return redirect('/')


@app.route('/dashboard')
def dashboard():
    # Ejemplo de lista de mensajes del chat (simula mensajes de la base de datos)
    chat_messages = message.get_all_messages()
    return render_template('dashboard.html', chat_messages=chat_messages)


"""    if 'user_id' not in session:
        return redirect('logout')  # Redirigir al usuario a la página de inicio o de inicio de sesión

    user_id_sesion = session['user_id']
    
    # Obtener citas favoritas del usuario
    favorite_quotes = Quote.get_favorite_quotes_by_user_id(user_id_sesion)
    
    # Obtener todas las citas que no son favoritas
    non_favorite_quotes = Quote.get_non_favorite_quotes_by_user_id(user_id_sesion)
    
    # Obtener datos del usuario y todas las citas para mostrar en el dashboard
    user = User.get_by_id({'id': user_id_sesion})
    quotes_with_users = Quote.get_quotes_with_user_names()
    favorite_quote_ids = Quote.get_favorite_quote_ids(user_id_sesion)"""
    








@app.route('/user_profile/<int:user_id>')
def user_profile(user_id):
    user = User.obtener_id(user_id)  # Obtén el usuario por su ID desde la base de datos
    
    if user:
        quotes = Quote.get_quotes_with_user_ids(user_id)  # Obtén las citas publicadas por el usuario
        total_quotes = Quote.get_total_quotes_by_user_id(user_id)
        return render_template('show_user.html', user=user, quotes=quotes, total_quotes=total_quotes )
    else:
        flash('Usuario no encontrado', 'error')
        return redirect('/dashboard')





@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')