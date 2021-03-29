# Core_Python_Flask-

# Run RTSP/TCP server
cd rtsp-simple-server/
docker run --rm -it -v $PWD/rtsp-simple-server.yml:/rtsp-simple-server.yml -p 8554:8554 aler9/rtsp-simple-server

# Run stream video by ffmpeg
ffmpeg -stream_loop -1 -re -i [path of video] -rtsp_transport tcp -vcodec h264 -f rtsp [rtsp_link]

# Download weights model check in 
https://drive.google.com/drive/folders/1jyn8JziGoBCCob4_CNRkp-jGWlsrOa-a?usp=sharing
