@echo off
cd C:\Users\Administrator\Desktop\rs_project2
docker-compose stop
docker rmi it21/rs
docker-compose up -d