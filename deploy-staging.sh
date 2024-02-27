cd /home/ubuntu/django-projects/api_bddw_com
git pull origin staging
sudo docker compose -f staging.yml down
sudo docker compose -f staging.yml up --build -d
sudo docker compose -f staging.yml run --rm django python manage.py migrate
