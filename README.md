# blog---multi-level-comments-service

В сервисе многоуровневая система комментариев. Реализована возможность фильтровать комметарии по уровню вложенности через query_param(?level), так же можно просмотреть и отфильтровать по уровню вложенности все вложенные комментарии к конкретному комментарию независимо от уровня его вложенности.

## Зависимости.
- Python3
- Docker
- Django
- Django Rest Framework

### Локальный запуск проекта.
- Откройте терминал и перейдите в ту директорию, в которой будет располагаться проект.
- Склонируйтуе проект к себе на машину:
```python
git clone https://github.com/RomanMelnikS/kvartirka-blog.git
```
- Перейдите в корневую директорию проекта и создайте .env файл в соответствии с env.dist.
- Если вы используете Docker выполните комманду: 
 ```python
 docker-compose up
 ```
- Если вы не используете Docker создайте и активируйте виртуальное окружение:
```python
python -m venv 'venv'
source venv/Scripts/activate
pip install -r requirements.txt
```
- Выполните команды:
```python
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata fixtures.json
python manage.py runserver
```
Проект запустится локально на вашей машине и будет доступен по ссылке http://localhost/api/v1/.

Доступ к админ-панели http://localhost/admin/:
- login: admin
- password: admin

Описание API http://localhost/docs/redoc/ или http://localhost/docs/swagger/.

### Авторизация:
- Переходим на http://localhost/api/v1/users/token/login/ вводим необходимые данные.
- Получаем "access": "token" и "refresh": "token"
- В запросах передаём Headers: Authorization: Bearer {"accsess"}
- Если срок действия токена истёк, переходим на /api/clients/token/refresh/ и передаём refresh: "refresh"
- Получаем обновлённый "access": "token"
