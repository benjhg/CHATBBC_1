from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.users import User
from flask_bcrypt import Bcrypt
from flask_app.models.messages import Quote
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def save():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        alias = request.form['alias']

        # Validar el formulario (puedes implementar la función validate_register en tu clase User si es necesario)
        if not User.validate_register(request.form):
            flash('Por favor, completa todos los campos.', 'register')
            return redirect("/")

        # Cifrar la contraseña antes de almacenarla en la base de datos
        pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Crear un diccionario con los datos del usuario
        user_data = {
            "username": username,
            "email": email,
            "password": pw_hash,  # Guarda la contraseña cifrada
            "alias": alias
        }

        # Guardar el usuario en la base de datos
        User.save(user_data)

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'register')
        return redirect("/")
    


@app.route('/login', methods=['POST'])
def login():
    user = User.get_by_email(request.form)

    if user and bcrypt.check_password_hash(user.password, request.form['password']):
        session['user_id'] = user.id
        return render_template('Dashboard1.html')
    else:
        flash("Invalid Email or Password", "login")
        return redirect('/')


@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('logout')  # Redirigir al usuario a la página de inicio o de inicio de sesión

    user_id_sesion = session['user_id']
    
    # Obtener citas favoritas del usuario
    favorite_quotes = Quote.get_favorite_quotes_by_user_id(user_id_sesion)
    
    # Obtener todas las citas que no son favoritas
    non_favorite_quotes = Quote.get_non_favorite_quotes_by_user_id(user_id_sesion)
    
    # Obtener datos del usuario y todas las citas para mostrar en el dashboard
    user = User.get_by_id({'id': user_id_sesion})
    quotes_with_users = Quote.get_quotes_with_user_names()
    favorite_quote_ids = Quote.get_favorite_quote_ids(user_id_sesion)
    return render_template("Dashboard.html", user=user, favorite_quotes=favorite_quotes, non_favorite_quotes=non_favorite_quotes, quotes_with_users=quotes_with_users, favorite_quote_ids=favorite_quote_ids)

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