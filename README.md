# FastAPI - ReqRes Clone

## Описание

Этот проект реализует простое API с использованием FastAPI, которое имитирует сервис ReqRes (https://reqres.in), предоставляя основные функции для работы с пользователями (создание, получение, обновление и удаление).

Проект включает микросервис на FastAPI, который предоставляет следующие эндпоинты:
- Получение списка пользователей
- Получение информации о пользователе по ID
- Создание нового пользователя
- Обновление информации о пользователе
- Удаление пользователя

## Структура проекта

Проект состоит из одного файла:

```
fastapi-reqres-clone/
├── app/
│   └── microservice.py        # Основной файл с кодом приложения
├── tests/
│   └── tests_reqres_api.py    # Файл с автотестами
├── requirements.txt           # Зависимости проекта
└── README.md                  # Документация

```


### Структура кода в `microservice.py`

В `microservice.py` реализован код приложения FastAPI, который содержит все необходимые эндпоинты для работы с пользователями. Также добавлены примеры тестов для проверки работы API с использованием `pytest`.

## Установка

Чтобы установить и запустить проект, выполните следующие шаги:


Клонируйте репозиторий:

   ```bash
      git clone https://github.com/fastapi-reqres-clone.git
```
Перейдите в каталог проекта:
```bash
    cd qaguru-advanced-playground
```

Создайте и активируйте виртуальную среду:
```bash
    python3 -m venv .venv
source .venv/bin/activate  # Для Linux/MacOS
.venv\Scripts\activate     # Для Windows
```

Установите зависимости:
```bash
  pip install -r requirements.txt
```
## Запуск приложения

Для того чтобы запустить приложение, используйте команду:

```bash
  uvicorn microservice:app --reload --port 8000
```

Теперь ваше приложение будет доступно по адресу http://127.0.0.1:8000.

API

Получить список пользователей
GET /api/users

Возвращает список всех пользователей.

Пример ответа:

```
[
  {
    "id": 1,
    "name": "John Doe",
    "job": "Software Engineer"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "job": "Project Manager"
  }
]
```

Получить пользователя по ID
GET /api/users/{user_id}

Получает информацию о пользователе по его ID.
Пример ответа:

```
{
  "id": 1,
  "name": "John Doe",
  "job": "Software Engineer"
}
```
Создать нового пользователя
POST /api/users

Создает нового пользователя.

Пример тела запроса:

```
{
  "name": "Morpheus",
  "job": "Leader"
}
```
Пример ответа:

```
{
  "id": 3,
  "name": "Morpheus",
  "job": "Leader"
}
```
Обновить пользователя
PUT /api/users/{user_id}

Обновляет информацию о пользователе.

Пример тела запроса:

```
{
  "name": "Morpheus",
  "job": "Zion Resident"
}
```
Пример ответа:

```
{
  "id": 2,
  "name": "Morpheus",
  "job": "Zion Resident"
}
```
Удалить пользователя
DELETE /api/users/{user_id}

Удаляет пользователя по ID.

Пример ответа:

```
{
  "message": "User deleted successfully"
}
```
Тесты

Для тестирования API используются pytest. Тесты проверяют работу всех эндпоинтов API.

Запуск тестов
Для запуска тестов выполните команду:

```pytest```

Тесты находятся в файле test_api.py и охватывают следующие аспекты:

Получение списка пользователей<br>
Получение пользователя по ID<br>
Создание нового пользователя<br>
Обновление пользователя<br>
Удаление пользователя
