## Installation

1. Run `cd backend` to move to the backend directory
2. Make sure python is installed by running `python3 -V`
3. [Switch to a virtual env if you want] (optional, recommended)
5. Run `pip install -r requirements.txt` to install all the dependencies
6. Run `python manage.py migrate` to apply the models to database
7. Finally, run `python manage.py runserver` to start the server

## API Usage
1. Create a simple login view
```
POST /api/login 
```   
- Include `username` and `password` in the body field

2. Create a single user sign up view
```
POST /signup 
```
- Include `username` and `password` in the body field

3. Create a new note
```
POST /notes/create
```
- Include `title` and `content` in the body field
- Include `Authorization: Token <your-token>` in the Header field

4. Retrieve a specific note by its ID
```
GET /notes/{id}
```
- Include `Authorization: Token <your-token>` in the Header field

5. Share the note with other users. 
```
POST /notes/share
```
- Include `note_id` and `usernames` in the body field
- For multiples usernames, add multiple usernames key value pairs in the body
- Include `Authorization: Token <your-token>` in the Header field

6. Update an existing note.
```
PUT /notes/{id}
```
- Include `content` in the body field

7. GET all the changes associated with the note. 
```
GET /notes/version-history/{id}
```
- Include `Authorization: Token <your-token>` in the Header field
