## Run
``` sh
env FLASK_ENV=development FLASK_APP=main flask run
python3 main.py

# For simple http server case
python3 simple-http-server-gateway.py
```

## Static web assets

open http://127.0.0.1:5000/web/index.html

## Internal route
> Note: redirect only works in browser, test in browser

GET: http://127.0.0.1:5000/route1?name=levi
POST: http://127.0.0.1:5000/route1 with name in the form field

## External route
> Note: use VSCode Thunder client to test
> For Flask, use form in POST
> For simple http server, use json in POST

GET: http://127.0.0.1:5000/route2?page=2
POST: http://localhost:5000/route2 with name and job in form fields

## References
- https://spring.io/guides/gs/gateway/
