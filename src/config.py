class developmentConfig():
    DEBUG = True
    MYSQL_HOST = '127.0.0.1'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = ''
    MYSQL_DB = 'abaco'
    MYSQL_CURSORCLASS = "DictCursor"

config = {
    'development':developmentConfig
}