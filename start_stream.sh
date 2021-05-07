ffmpeg -stream_loop -1 -re -i test.mp4 -rtsp_transport tcp -vcodec h264 -f rtsp rtsp://localhost:8554/test
