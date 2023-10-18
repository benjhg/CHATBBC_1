from flask import render_template,redirect, session,request, flash, url_for
from flask_app import app
from flask_app.models.messages import Message
from flask_app.models.users import User
from flask_app.controllers import user
from flask_app.config.mysqlconnection import connectToMySQL
import mysql.connector

@app.route('/add_message', methods=['POST'])
def add_message():
    # Obtén el contenido del mensaje del formulario
    content = request.form.get('content')

    # Obten el user_id del usuario autenticado (puedes usar session['user_id'] si está configurado)
    user_id =  session['user_id']  # Cambia esto según cómo obtienes el ID del usuario autenticado

    # Valida el contenido del mensaje
    if not content:
        flash('El mensaje no puede estar vacío.', 'error')
        return redirect(url_for('dashboard'))  # Redirige de vuelta al dashboard en caso de error

    # Guarda el mensaje en la base de datos utilizando el método save de la clase Message
    message_data = {
        'content': content,
        'user_id': user_id
    }
    Message.save(message_data)  # Asegúrate de que 'Message' esté correctamente importado y configurado

    flash('Mensaje añadido correctamente.', 'success')
    return redirect(url_for('dashboard'))  # Redirige al dashboard después de añadir el mensaje

if __name__ == '__main__':
    app.run(debug=True)






@app.route('/edit_quote/<int:quote_id>', methods=['GET', 'POST'])
def edit_quote(quote_id):
    # Obtén la cita de la base de datos usando el ID
    quote = Quote.get_by_id(quote_id)

    # Verifica si la cita existe y si pertenece al usuario actual
    if not quote or quote.users_id != session.get('user_id'):
        flash('No tienes permisos para editar esta cita.', 'error')
        return redirect('/dashboard')  # Redirige al usuario de vuelta al dashboard

    if request.method == 'POST':
        # Obtén el nuevo texto de la cita del formulario de edición
        new_text = request.form['new_text']

        # Validar la cita usando la función validate_quote
        if not Quote.validate_quote(new_text):
            print('La cita debe tener al menos 3 caracteres.')
        else:
            # Actualiza el texto de la cita en la base de datos
            Quote.update({'id': quote_id, 'text': new_text})

            flash('Cita editada con éxito.', 'success')
            return redirect('/dashboard')  # Redirige al usuario de vuelta al dashboard después de la edición

    # Si es una solicitud GET o si la validación falla, muestra el formulario de edición con la cita actual
    return render_template('edit_quote.html', quote=quote, quote_id=quote_id)



@app.route('/delete_quote', methods=['POST'])
def delete_quote():
    quote_id = request.form.get('quote_id')
    is_favorite = request.form.get('is_favorite') == 'true'
    user_id = session.get('user_id')

    if quote_id:
        if is_favorite:
            # Si es una cita favorita, eliminarla de la tabla de favoritos primero
            success = Quote.remove_from_favorites(quote_id, user_id)
            if success:
                # Luego, eliminar la cita de la tabla de citas
                Quote.delete_quote(quote_id)
                flash('Cita eliminada con éxito.', 'success')
            else:
                flash('Error al eliminar cita de favoritos.', 'error')
        else:
            # Si no es una cita favorita, eliminarla directamente de la tabla de citas
            Quote.delete_quote(quote_id)
            flash('Cita eliminada con éxito.', 'success')
    else:
        flash('ID de cita no proporcionado.', 'error')

    return redirect('/dashboard')



@app.route('/add_to_favorites/<int:quote_id>', methods=['POST'])
def add_to_favorites(quote_id):
    if request.method == 'POST':
        # Obtiene el ID del usuario de la sesión (debes tener implementada la autenticación del usuario)
        user_id = session.get('user_id')
        
        # Verifica si el usuario está autenticado
        if user_id:
            # Llama al método add_to_favorites de la clase Quote para agregar la cita a favoritos
            if Quote.add_to_favorites(quote_id, user_id):
                flash('Cita agregada a favoritos con éxito.', 'success')
            else:
                flash('La cita ya está en tus favoritos.', 'warning')
        else:
            flash('Debes iniciar sesión para agregar citas a favoritos.', 'error')
        
        return redirect('/dashboard')  # Redirige al usuario al dashboard o a donde desees después de la operación




@app.route('/remove_from_favorites/<int:quote_id>', methods=['POST'])
def remove_from_favorites(quote_id):
    success = Quote.remove_from_favorites(quote_id, session['user_id'])

    if success:
        flash('Cita eliminada de favoritos.', 'success')
    else:
        flash('Error al eliminar cita de favoritos.', 'error')

    return redirect('/dashboard')





