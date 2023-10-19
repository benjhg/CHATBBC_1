from flask_app.config.mysqlconnection import connectToMySQL

class UserGame:
    
    db_name = "global_chat"
    def __init__(self, data):
        self.id = data.get('id')
        self.users_id = data.get('user_id')
        self.game_id = data.get('game_id')
        self.created_at = data.get('created_at')

    @classmethod
    def get_all_games(cls, user_id):
        query = """
            SELECT games.id, games.title, games.genre, 
                   CASE WHEN user_games.games_id IS NOT NULL THEN 1 ELSE 0 END AS is_favorite
            FROM games
            LEFT JOIN user_games ON games.id = user_games.games_id AND user_games.users_id = %(user_id)s;
        """
        data = {
            'user_id': user_id
        }
        games = connectToMySQL(cls.db_name).query_db(query, data)
        return games

    @classmethod
    def add_game_to_user(cls, user_id, game_id):
        query = "INSERT INTO user_games (users_id, games_id) VALUES (%(user_id)s, %(game_id)s);"
        data = {
            'user_id': user_id,
            'game_id': game_id
        }
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def remove_game_from_user(cls, user_id, game_id):
        query = "DELETE FROM user_games WHERE users_id = %(users_id)s AND games_id = %(games_id)s;"
        data = {
            'users_id': user_id,
            'games_id': game_id
        }
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def get_user_games(cls, user_id):
        query = """
            SELECT games.id, games.title, games.genre
            FROM games
            JOIN user_games ON games.id = user_games.games_id
            WHERE user_games.users_id = %(user_id)s;
        """
        data = {
            'user_id': user_id
        }
        games = connectToMySQL(cls.db_name).query_db(query, data)
        return games