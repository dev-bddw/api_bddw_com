cd /home/ubuntu/django-projects/api_bddw_com
git pull origin production
sudo docker compose -f production.yml down
sudo docker compose -f production.yml run --rm django python manage.py migrate
sudo docker compose -f production.yml up --build -d
