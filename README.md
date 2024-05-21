create vnenv
```
python -m venv venv
```

activate

```
source venv/bin/activate 
```

install requirements
```
pip install -r .requirements.txt
```

DB COMMANDS TODO

run server
```
flask --app application db init
flask --app application db migrate -m "Initial migration."
```