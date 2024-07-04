# Autotests

##  Запуск проекта

1. Перейти в папку с проектом:
 `cd autotests`
<br/>
<br/>
2. **Установить** venv **активировать** venv и **установить зависимости** проекта: 
    - `python -m venv venv`
    - `source venv/bin/activate`
    - `pip install -r requirements.txt`
<br/>
<br/>
3. Переименовать файл **.env.example** в **.env**:
    `mv .env.example .env`
<br/>
<br/>
4.  Запустить тесты с помощью команды:
    `pytest`
