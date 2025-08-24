# env:
# check env
- uv venv
# activate env
- source .venv/bin/activate
# check libraries
- pip3 list
# deactivate env
- deactivate

# fastapi
# run server
- uvicorn books:app --reload
- fastapi dev books.py
- fastapi run books.py
# create database
- uvicorn main:app --reload
- fastapi dev main.py
- fastapi run main.py
# enter database
- sqlite3 app.db
# sqlite methods
- .schema
- .exit
- .mode box
- .mode table
# data manipulation
- insert into todo (title, description, priority, complete) values ('test title', 'test description', '4', False);
- select * from todo;
# migrations
- alembic init alembic
- alembic revision -m "" (modify the upgrade/downgrade methods and add the column to models/post methods)
- alembic upgrade accb075dcdb5
- alembic downgrade accb075dcdb5
