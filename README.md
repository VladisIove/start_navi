# Create virtualenv

python -m venv env
source env/bin/activate

# Download requirements

pip install -r requirements.txt

# Create database in postgresql

DATABASE = star_navi
USERNAME = star_navi
PASSWORD = star_navi
PORT = 5432
HOST = localhost

# Up Api

python main.py

# Requests

## Signup

- Curl request
  curl -X POST http://127.0.0.1:5000/signup -d '{"password":"1234", "email":"foo1@gmail.com"}' -H 'Content-Type: application/json'

  password: str - required
  email: str - required

- Respone
  {
  "token": str
  }

## Login

- Curl request
  curl -X POST http://127.0.0.1:5000/login -d '{"password":"1234", "email":"foo1@gmail.com"}' -H 'Content-Type: application/json'

  password: str - required
  email: str - required

- Response
  {
  "token": str
  }

## Create Post

- Curl request
  curl -X POST http://127.0.0.1:5000/createPost -d '{"text":"Bla", "author_id":2}' -H 'Authorization: Bearer <JWT>' -H 'Content-Type: application/json'

  text: str - required
  author_id: int - required

- Response
  {
  'id': int,
  'text': str,
  'author_id': int
  }

## Like/Unlike Post

- Curl request
  curl -X POST http://127.0.0.1:5000/toogleLikePost -d '{"user_id":"1", "post_id":"1"}' -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT>'

  user_id: int - required
  post_id: int - required

- Response
  {
  'id': int,
  'user_id': int,
  'post_id': int,
  'craeted': bool
  }

## Analitic likes by date

- Curl request
  curl -X POST http://127.0.0.1:5000/analiticLikes'?date_from=06-06-2018&date_to=16-08-2020' -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT>'

- Response
  [
  {
  "date": str,
  "count_like": int
  }
  ]

## User activity

- Curl request
  curl -X POST http://127.0.0.1:5000/userActivity -d '{"user_id":"1"}' -H 'Content-Type: application/json' -H 'Authorization: Bearer <JWT>'

  user_id: int - required

- Response
  [
  {
  "created": str,
  "id": int,
  "type_active": str,
  "user_id": int
  },
  ...
  ]
