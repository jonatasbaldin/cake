![Cheesecake](img/logo.png)

[![Build Status](http://cake.deployeveryday.com:8080/buildStatus/icon?job=cake)](http://cake.deployeveryday.com:8080/job/cake)

# Cake
Cake is an application that crawls over [TechCrunch](https://techcrunch.com) posts, stores data about authors, articles and provides a web API to consume it.
Why? This is a code challenge for [Cheesecake Labs](https://ckl.io). You know, needing a job :)

### Considerations
This is my first real project with Django and Djando REST Framework, so I had to study a lot and create this Cake in the last days. I tried to follow the recommendations and best practices available on the Internet and the documentations. With that in mind, here are some considerations:

- I didn't use GitHub's pull request and Git's branch because is a small and pretty straightforward project. 
- When collecting data with Scrapy, I tried `xpath`, `css` and even get some `ld+json` that was sitting there. I used all three to test it out.
- The crawler: In **production**, it runs the first time, collecting up to 1000 requests, which can be changed in `docker-compose-production.yml`. After that, a cron job runs every 15 minutes collecting up to 100 requests. This way things don't get out of control. In **development**, you can run the crawler as you wish.
- Collect more data with the crawler.
- Write more tests (they're never enough!).
- Use a DNS service to create an entry for the instance created.
- Improve production deployment. Here I'm experimenting with Ansible and EC2 on-the-fly, which may seen a bit raw now.

### API Endpoint
The production API endpoint can be consumed at `cake.deployeveryday.com/api/v1/`.   
The way the API was built, also allows PUT, PATCH and DELETE. But there's code to validate these methods. Maybe tomorrow I'll code that! :D    

Here are the GETs:
- `/api/v1/authors/`: get all the authors paginated.
- `/api/v1/authors/<id>`: get details on one author.
- `/api/v1/articles/`: get all the articles paginated.
- `/api/v1/articles/<id>`: get details on one article.

### Softwares used
Here's a list of softwares, libraries and servicesused in this project:
- Amazon AWS
- Ansible
- Docker
- docker-compose
- NGINX
- Django
- Django REST Framework
- Gunicorn
- coverage
- PostgreSQL
- psycopg2
- Scrapy
- Jenkins

### Architecture
![Architecture](img/architecture.png)

An overview of the infrastructure:
- All the requests go to **nginx**, which will server the `/static` files or proxy them to the **web** container.
- The **web**, which runs Gunicorn and Django, will process the request. It consults the **db** for data.
- **db** is a PostgreSQL server with persistent data on the host. It stores information about Authors and Articles.
- Finally **scrap**, which runs Scrapy, gets data from TechCrunch and stores on **db**.

Also, about the code deployment process:
- When the code hits the **master** branch, GitHub automatically sends a hook to [Jenkins](http://cake.deployeveryday.com:8080).
- Jenkins executes its build: gets the new code, executes the tests and docker-compose to bring the application up to date.

### Models Reference
![Models](img/models.png)

### Up and running: local!
It's a piece of *Cake* to run locally. Pun intended. You'll need `docker` and `docker-compose`.

Clone de repository:
```bash
git clone https://github.com/jonatasbaldin/cake.git
cd cake
```

Run docker-compose to build and migrate Django models:
```bash
docker-compose build
docker-compose up -d
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```

Run the crawler (here with 100 requests limit):
```bash
docker-compose run scrap scrapy crawl cake --set CLOSESPIDER_PAGECOUNT=100
```

You're ready to go! Consume the API at `http://localhost/api/v1/`.

### Up and running: production!

Clone de repository:
```bash
git clone https://github.com/jonatasbaldin/cake.git
cd cake
```

Export your AWS credentials and configure your environment:
```bash
export AWS_ACCESS_KEY_ID=<access_key>
export AWS_SECRET_ACCESS_KEY=<secret_key>

# Configure EC2 variables
vim ansible_vars.yml

# Configure APP_ALLOWED_HOSTS, the domain your instace will respond
vim docker-compose-production.yml
```

Run Ansible for the first time (no inventory):
```bash
ansible-playbook ansible_deploy.yml
```

The next time you run it, use the inventory file created:
```bash
ansigle-playbook -i ansible_inventory ansible_deploy.yml
```

Now, create an A DNS entry with the name specified in `APP_ALLOWED_HOSTS` poiting to your EC2 public IP.    
You're ready to go! Consume the API at `http://yourdomain.com/api/v1/`.

### Thanks!
