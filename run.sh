#!/bin/sh
docker build -t webapp . 
docker run -p 5000:5000 webapp


