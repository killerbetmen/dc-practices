# DC Practice Task

An application is written on FastAPI. You can view/create/edit/delete messages, you can also find the number of views per message.

## To setup the project on your local machine:

1. Click on `Fork`.
2. Go to your fork and `clone` the project to your local machine.
3. Install the requirements `pip install -r requirements.txt`.
4. Set database url 
```
export DATABASE_URL="postgresql://user:password@localhost:port/dbname
```
5. Set username and password for authentication 
```
export USER="username"
export PASSWORD="password"
```
6. Run the development server 
```
uvicorn app.views:app --host=0.0.0.0 --port=${PORT:-8000}
```
7. Run tests `pytest`
An application will be available at 0.0.0.0:8000.


## Application routes
### GET `/`
Welcome page  

*Request example:* `https://dc-practices.herokuapp.com/`
*Response example:* 
```
{"message" : "Hello DaftCode"}
```

### GET `/messages`
Method for getting a list of all messages

*Request example:* `https://dc-practices.herokuapp.com/messages`
*Response example:* 
```
[{
    "Message": "Example text",
    "Views": 3,
    "MessageID": 1
  },
  {
    "Message": "Bonjour",
    "Views": 1,
    "MessageID": 2
  },...
```

### GET `/messages/{message_id}`
Get a message and number of views by `message_id`

*Request example:* `https://dc-practices.herokuapp.com/messages/2`
*Response example:* 
```
{
  "message": {
    "Message": "Bonjour",
    "Views": 2,
    "MessageID": 2
  }
}
```

### GET `/users/me`
Get current user (if you're not authorized you will get HTTP 401 Unauthorized error) 

*Request example:* `https://dc-practices.herokuapp.com/users/me`
*Response example:*
```
{"username": "USERNAME"}
```

  
### POST `/add_message`
Method for creating a new message

*Example of usage:* 
```
curl -X 'POST'
   'https://dc-practices.herokuapp.com/add_message'
   -H 'accept: application/json'
   -H 'Content-Type: application/json'
   -d '{"Message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."}'
   --user USERNAME:PASSWORD
```
*Response example:* 
```
{
  "MessageID": 5,
  "Message": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
  "Views": 0
}
```

### PUT `/update_message/{message_id}`
Update message text by using `message_id`

*Example of usage:* 
```
curl -X 'PUT' \
  'https://dc-practices.herokuapp.com/update_message/6'
  -H 'Content-Type: application/json'
  -d '{"Message": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."}'
  --user USERNAME:PASSWORD
```

*Response example:* 
```
{
  "MessageID": 6,
  "Message": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
  "Views": 0
}
```

### DELETE `/delete_message/{message_id}`
Method for deleting messages by `message_id`. If `message_id` doesn't exist in database you will get HTTP 404 NOT FOUND error.

*Request example:* `https://dc-practices.herokuapp.com/delete_message/6` (you will be asked to provide username and password) or using `curl`:
```
curl -X 'DELETE'
  'https://dc-practices.herokuapp.com/delete_message/6'
  --user USERNAME:PASSWORD
```

*Response example:* 
```
No content
```