#heroku login;
docker build -t task-service .;
docker tag task-service registry.heroku.com/cs4261-task-service/web;
docker push registry.heroku.com/cs4261-task-service/web;
heroku container:release web -a cs4261-task-service;
#heroku logs --tail --app cs4261-task-service;