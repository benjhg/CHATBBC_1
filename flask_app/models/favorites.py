from flask_app.config.mysqlconnection import connectToMySQL

class Favorite:
    
    db_name = "citas"
    def __init__(self, user_id, quote_id, updated_at, created_at):
        self.user_id = user_id
        self.quote_id = quote_id
        self.updated_at = updated_at
        self.created_at = created_at

    

    @classmethod
    def save(cls, data):
        query = "INSERT INTO favorites (user_id, quote_id) VALUES (%(user_id)s, %(quote_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)
