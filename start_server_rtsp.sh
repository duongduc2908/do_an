cd rtsp-simple-server/
sudo docker run --rm -it -v $PWD/rtsp-simple-server.yml:/rtsp-simple-server.yml -p 8554:8554 aler9/rtsp-simple-server
