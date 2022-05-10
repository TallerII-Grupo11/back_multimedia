# Spotifiuby back\_multimedia

[![codecov](https://codecov.io/gh/TallerII-Grupo11/back_multimedia/branch/main/graph/badge.svg?token=5CIK0SM2UN)](https://codecov.io/gh/TallerII-Grupo11/back_multimedia)
[![Linters](https://github.com/TallerII-Grupo11/back_multimedia/actions/workflows/linter.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_multimedia/actions/workflows/linter.yaml)
[![Tests](https://github.com/TallerII-Grupo11/back_multimedia/actions/workflows/test.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_multimedia/actions/workflows/test.yaml)
[![Deploy](https://github.com/TallerII-Grupo11/back_multimedia/actions/workflows/deploy.yaml/badge.svg)](https://github.com/TallerII-Grupo11/back_multimedia/actions/workflows/deploy.yaml)


### Docker

Run app commands local
```
docker build -t back-multimedia:0.1 .
docker run -p 5000:5000 --env-file .env back-multimedia:0.1
```

### Manual Deploy to Heroku

```
heroku config:set port=5000
heroku config:set version="1.0.0"
heroku config:set title="Back_Multimedia"
heroku config:set db_path="mongodb+srv://<user>:<pass>@multimedia.a0iq4.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

heroku container:push web -a spotifiuby-multimedia
heroku container:release web -a spotifiuby-multimedia


```

### Test

Run tests using [pytest](https://docs.pytest.org/en/6.2.x/)

``` bash
pytest tests/
```
