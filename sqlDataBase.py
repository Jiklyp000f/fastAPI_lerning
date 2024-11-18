import sqlite3

db = sqlite3.connect('users.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
    login TEXT UNIQUE,
    password TEXT,
    cash BIGINT
    )""")

db.commit()

user_login = input('Введите логин: ')
user_password = input('Введите пароль: ')


sql.execute("SELECT login FROM users WHERE login = ?", (user_login,))
if sql.fetchone() is None:
    sql.execute("INSERT INTO users VALUES (?, ?, ?)", (user_login, user_password, 0))
    db.commit()
    print('Вы успешно зарегистрировались!')
else:
    print('Такой логин уже существует.')

for value in sql.execute("SELECT * FROM users"):
    print(value[0])

db.close()
