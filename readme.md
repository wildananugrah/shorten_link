# How to Run:
```cmd
docker build -t [your-image-name]:[your-image-tag] -f [your-dockerfile] .
docker run -d --name [your-container-name] -e DATABASE_HOST=[your-mongo-host] -e DATABASE_PORT=[your-mongo-port] -e WEB_HOST=[your-web-host] -p 8080:8080 [your-image-name]
```
Database: MongoDB