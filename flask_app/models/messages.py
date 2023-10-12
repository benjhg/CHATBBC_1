from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class message:
    db_name = "global_chat"
    def __init__(self, data):
        self.content = data.get('content')
        self.user_id = data.get('user_id')
        self.sent_at = data.get('sent_at')

    classmethod
    def save(cls, data):
        query = "INSERT INTO messages (`content`,`user_id`,`sent_at`) VALUES (%(content)s, %(user_id)s, now());"
        return connectToMySQL(cls.db_name).query_db(query, data)
    
    @classmethod
    def get_all_messages(cls):
        query = "SELECT content FROM messages;"
        results = connectToMySQL(cls.db_name).query_db(query)
        return [messages['content']for messages in results ]

    @classmethod
    def update(cls, data):
        query = "UPDATE `citas`.`quotes` SET `text` = %(text)s, `updated_at` = NOW() WHERE `id` = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def delete_quote(cls, quote_id):
        try:
            # Eliminar entradas de la tabla favorites vinculadas a la cita
            delete_favorites_query = "DELETE FROM favorites WHERE quote_id = %(quote_id)s;"
            data = {'quote_id': quote_id}
            connectToMySQL(cls.db_name).query_db(delete_favorites_query, data)

            # Eliminar la cita de la tabla quotes
            delete_quote_query = "DELETE FROM quotes WHERE id = %(quote_id)s;"
            connectToMySQL(cls.db_name).query_db(delete_quote_query, data)

            return True
        except Exception as e:
            print(f"Error al eliminar la cita: {e}")
            return False

    @classmethod
    def get_name_by_id(cls, data):
        query = "SELECT quotes.id, quotes.text, users.name FROM quotes LEFT JOIN users ON quotes.user_id = users.id WHERE quotes.id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query, data)
        if results:
            return results[0]['users.name']
        else:
            return None

    @classmethod
    def get_quotes_with_user_names(cls):
        query = "SELECT quotes.id, quotes.text, users.name, users_id FROM quotes LEFT JOIN users ON quotes.users_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        quotes_with_names = []
        for row in results:
            quote_with_name = {
                'id': row['id'],
                'text': row['text'],
                'user_name': row['name'],
                'user_id': row['users_id']
                
            }
            quotes_with_names.append(quote_with_name)
        return quotes_with_names



    
    @staticmethod
    def get_quotes_with_user_ids(user_id):
        query = "SELECT * FROM quotes WHERE users_id = %(user_id)s;"
        data = {
            'user_id': user_id
        }
        results = connectToMySQL('citas').query_db(query, data)

        quotes = []
        for row in results:
            quote = {
                'id': row['id'],
                'text': row['text'],
                'user_id': row['users_id']  # Usa el nombre correcto de la columna
            }
            quotes.append(quote)

        return quotes




    @classmethod
    def get_all_id(cls):
        query = "SELECT text FROM quotes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        return [quote['user_id']for quote in results ]
    



    @staticmethod
    def get_quotes_with_user_ids(user_id):
        query = "SELECT * FROM quotes WHERE users_id = %(user_id)s;"
        data = {
            'user_id': user_id
        }
        results = connectToMySQL('cls.db_name').query_db(query, data)

        quotes = []
        for row in results:
            quote = {
                'id': row['id'],
                'text': row['text'],
                'user_id': row['users_id']  # Agrega el user_id a cada cita
            }
            quotes.append(quote)

        return quotes
        




    @classmethod
    def get_all(cls):
        query = "SELECT * FROM quotes;"
        results = connectToMySQL(cls.db_name).query_db(query)
        quotes = []
        for row in results:
            quotes.append(cls(row))
        return quotes

    def validate_message(text):
        is_valid = True

        if len(text) < 3:
            flash("La cita debe tener al menos 3 caracteres.", 'quote_error')
            is_valid = False

        return is_valid

    @classmethod
    def get_by_id(cls, quote_id):
        # Realiza una consulta para obtener la cita por su ID
        query = "SELECT * FROM quotes WHERE id = %(id)s;"
        data = {'id': quote_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        
        if result:
            return cls(result[0])
        return None

    @classmethod
    def get_total_quotes_by_user_id(cls, user_id):
        query = "SELECT COUNT(*) FROM quotes WHERE users_id = %(user_id)s;"
        data = {
            'user_id': user_id
        }
        result = connectToMySQL(cls.db_name).query_db(query, data)
        # La consulta devuelve una lista de resultados, así que necesitas extraer el valor del conteo
        total_quotes = result[0]['COUNT(*)']
        return total_quotes
    
    
    @classmethod
    def get_favorite_quote_ids(cls, user_id):
        query = "SELECT quotes.id, quotes.text FROM quotes JOIN favorites ON quotes.id = favorites.quote_id WHERE favorites.user_id = %(user_id)s;"
        data = {'user_id': user_id}
        results = connectToMySQL(cls.db_name).query_db(query, data)

        # Obtén los identificadores de las citas favoritas como una lista
        favorite_quote_ids = [result['id'] for result in results]

        return favorite_quote_ids


    @classmethod
    def add_to_favorites(cls, quote_id, user_id):
        try:
            # Verificar si la cita ya está en favoritos del usuario
            query = "SELECT * FROM favorites WHERE user_id = %(user_id)s AND quote_id = %(quote_id)s;"
            data = {
                "user_id": user_id,
                "quote_id": quote_id
            }
            result = connectToMySQL(cls.db_name).query_db(query, data)

            # Si la cita no está en favoritos, agregarla
            if not result:
                insert_query = "INSERT INTO favorites (user_id, quote_id) VALUES (%(user_id)s, %(quote_id)s);"
                connectToMySQL(cls.db_name).query_db(insert_query, data)
                return True
            else:
                return False  # La cita ya está en favoritos del usuario

        except Exception as e:
            print(f"Error al agregar cita a favoritos: {e}")
            return False

### Método `remove_from_favorites` en la Clase `Quote`:

    @classmethod
    def remove_from_favorites(cls, quote_id, user_id):
        try:
            # Eliminar la entrada correspondiente en la tabla favorites
            delete_favorites_query = "DELETE FROM favorites WHERE user_id = %(user_id)s AND quote_id = %(quote_id)s;"
            data = {
                "user_id": user_id,
                "quote_id": quote_id
            }
            connectToMySQL(cls.db_name).query_db(delete_favorites_query, data)

            return True
        except Exception as e:
            print(f"Error al eliminar la cita de favoritos: {e}")
            return False
        

    @classmethod
    def get_favorite_quotes_by_user_id(cls, user_id):
        query = "SELECT q.id, q.text, q.users_id, u.name as user_name FROM quotes q JOIN users u ON q.users_id = u.id WHERE q.id IN (SELECT quote_id FROM favorites WHERE user_id = %(user_id)s);"
        data = {'user_id': user_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        favorite_quotes = []
        for row in result:
            quote = {
                'id': row['id'],
                'text': row['text'],
                'user_id': row['users_id'],
                'user_name': row['user_name']
            }
            favorite_quotes.append(quote)
        return favorite_quotes 
        

    @classmethod
    def get_non_favorite_quotes_by_user_id(cls, user_id):
        query = "SELECT q.id, q.text, q.users_id, u.name as user_name FROM quotes q JOIN users u ON q.users_id = u.id WHERE q.id NOT IN (SELECT quote_id FROM favorites WHERE user_id = %(user_id)s);"
        data = {'user_id': user_id}
        result = connectToMySQL(cls.db_name).query_db(query, data)
        non_favorite_quotes = []
        for row in result:
            quote = {
                'id': row['id'],
                'text': row['text'],
                'user_id': row['users_id'],
                'user_name': row['user_name']
            }
            non_favorite_quotes.append(quote)
        return non_favorite_quotes        