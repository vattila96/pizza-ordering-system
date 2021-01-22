# Pizza ordering system.
Forked from: https://github.com/thejungwon/docker-webapp-django

## Migration errors
If you have some migration errors run the following code snippets:
```
./kill_app.sh
docker volume list
docker volume rm container_pgdata
```

## Prerequists
- Clone this directory
- Install docker for any desktop platforms (Linux, Windows, MacOS)
- Open a shell in the cloned direcetory (the folder called pizza-ordering-system)
- Run './encode_data.sh' script. You can enter anything here but email sending needs valid gmail account's username and password (see [feature/12](https://github.com/fovecsernyes/pizza-ordering-system/tree/feature/12)).
- Type in './build_images.sh' and wait until the Docker images are ready (only neccessary for the first time and after changes in the Dockerfile)
- Type in './run_app.sh' and wait until everything is up
- The website should be reachable from any browsers at localhost:8000
- For killing it, type in './kill_app.sh'

## Important
- Please do not forget that Python usees **snake_case**!
- Use a plugin in your IDE that understands `.editorconfig`
- Apply formatting rules often!

## Built With

* [Django](https://www.djangoproject.com/) - Web framework
* [PostgreSQL](https://www.postgresql.org/) - Database
* [Unsplash](https://source.unsplash.com/) - External API
* [Bootstrap](https://getbootstrap.com/) - Front-end framework

