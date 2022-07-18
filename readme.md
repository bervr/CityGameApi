<h1>Readme для тестового проекта
</h1>

<h2>Вводная часть</h2>
Это API игрового движка, для городских командных игр, подробнее в ТЗ.
<h2>Установка</h2>
Проект на Django. Подразумевается что вы знаете как это установить и запустить, или у вас уже все установлено и запущено 
<p>Для сборки и запуска выполните</p>
`docker-compose up`
<p>При первом запуске выполните
`docker-compose run web python manage.py create_sql_view`
это создаст необходимые вьюхи в базе данных</p>
<p>Для заполнения тестовыми данными и создания тестовых пользователейвы выполните:</p>
`docker-compose run web python manage.py fill_db`
<p>Создастся одна тестовая игра с 3 уровнями и 2 пользователя. Вход в админку: <p> пользователь
'django'</p> <p>пароль '12345'</p>
<p>Либо при первом запуске нужно будет вручную создать учетную запись админа вызвав</p>
`docker-compose run web python manage.py createsuperuser`
<p>чтобы остановить работу выполните </p>
`docker-compose down`

<h2>Авторизация</h2>
Для доспупа в админку нужно зайти по 
https://your_url_here/admin и аутентифицироваться под учеткой имеющей права админа.

Для доступа к функциям API нужно авторизоаться с правами пользователя  
https://your_url_here/api-auth/login/

<h2>API</h2>

Ссылка  в API  https://your_url_here/api

<p>GET game/{int:game}/level/ - все уровни игры game</p>
<p>GET game/{int:game}/level/{int:id} - уровень игры с заданым номером</p>
<p>GET /level/{int:game}/{int:id}/promt/{int:num}  - подсказка num, для уровня id, игры game</p>
<p>POST /answer/ - отправить ответ </p>

```
content : {
    "game": id,     - id игры
    "level": id,    - id уровня   
    "answer": ""    - ответ
}
   ```

<p>GET /stat/ - статистика уровней</p>




