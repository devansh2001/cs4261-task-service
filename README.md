# Task Service

### References
- https://docs.docker.com/language/python/build-images/
- https://dev.to/ejach/how-to-deploy-a-python-flask-app-on-heroku-using-docker-mpc
- https://www.youtube.com/watch?v=4eQqcfQIWXw
- https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python

### Important Commands
All are from : https://www.youtube.com/watch?v=4eQqcfQIWXw

Tagging Docker image
```docker tag task-service registry.heroku.com/cs4261-task-service/web```

Pushing docker image to heroku 
```docker push registry.heroku.com/cs4261-task-service/web```

Releasing docker image (make the app accessible online)
```heroku container:release web -a cs4261-task-service```