# back\_multimedia

Run app commands local
```
export MONGODB_URL="mongodb+srv://admin_user:<password>@multimedia.a0iq4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

uvicorn app:app --reload
```

Deploy en Heroku
```
git push heroku main
heroku logs --source app --tail

heroku config:set MONGO_URL="<url>"

```