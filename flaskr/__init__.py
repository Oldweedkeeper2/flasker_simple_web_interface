import os  # Импортируем стандартный модуль os для работы с операционной системой

from flask import Flask  # Импортируем класс Flask из модуля flask


# Фабричная функция для создания экземпляра приложения
def create_app(test_config=None):
    # Создаем экземпляр приложения Flask
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../instance/static',
                instance_relative_config=True)
    # Устанавливаем базовую конфигурацию для приложения
    app.config.from_mapping(
            SECRET_KEY='dev',  # Ключ для шифрования сессий и других нужд
            DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),  # Путь к файлу базы данных
    )
    
    # Загружаем дополнительную конфигурацию из файла, если не в режиме тестирования
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Иначе загружаем конфигурацию для тестирования
        app.config.from_mapping(test_config)
    
    # Удостоверяемся, что папка instance существует
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass  # Если папка уже существует, пропускаем создание
    
    # Простой маршрут, который возвращает строку "Hello, World!"
    # @app.route('/hello')
    # def hello():
    #     return 'Hello, World!'
    
    from . import db
    db.init_app(app)
    from . import auth
    app.register_blueprint(auth.bp)
    
    from flaskr import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule('/', endpoint='index')
    return app  # Возвращаем созданный экземпляр приложения
