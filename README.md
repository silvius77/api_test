# api_test
Выполнено несколько разнообразных тестов с использованием Postman для примера.

Выполнены тесты на Python с использованием PyTest.

Покрытие тестами реализовано в **85,7 %**

<hr>

Методы покрытые тестами (с параметрами) 6шт: 

- GET https://reqres.in/api/users

- GET https://reqres.in/api/users?page=[INT]

- GET https://reqres.in/api/users/[ID]

- POST https://reqres.in/api/users/[ID]

- PATCH https://reqres.in/api/users/[ID]

- DELETE https://reqres.in/api/users/[ID]

Методы без покрытия тестами 1шт: 

- PUT https://reqres.in/api/users


<br/>

**Формула расчёта:**

<**Покрытые тесты**> / <**Общее кол-во**> * 100

6/7*100 = 85,7%