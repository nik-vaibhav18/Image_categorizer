# Image_categorizer
This app uses OpenAI GPT-4o to analyze an image and generate a JSON metadata 

## Streamlit App demo:
<img width="954" alt="image" src="https://github.com/user-attachments/assets/d9ee8efd-23be-441e-afa6-00f93288712e">

## Uploaded images extracted Infomation using gpt-4o
<img width="678" alt="image" src="https://github.com/user-attachments/assets/4118ce78-2803-466c-b64a-11c35e7e42d5">
<img width="663" alt="image" src="https://github.com/user-attachments/assets/b8f17989-21a4-4ce8-ad7f-24d84857fa13">

## Azure Blob container for storing files
<img width="935" alt="image" src="https://github.com/user-attachments/assets/b0cc4978-fb73-463a-bf07-d1e2893a1535">

## Azure CosmosDB for saving response of gpt-4o about image along with meta data of blob image file
<img width="944" alt="image" src="https://github.com/user-attachments/assets/a6557439-6519-4440-8483-350ae9d9d66b">


# to build docker container 
``` bash
docker build -t image-categorizer.v1.0 .
```

# docker conatiner running
```bash
docker ps
```

# to run the image and create container
```bash
 docker run -p 8501:8501 <image id>
```

# after killing still few images meta data will be running see using
```bash
docker ps -a
```

# to see docker images
```bash
docker images
```

# push new image to repo to share with anyone
```bash
docker tag local-image:tagname new-repo:tagname
docker push new-repo:tagname
```

# Docker container URl
```
https://hub.docker.com/repository/docker/nik18/image-categorizer/general
```







