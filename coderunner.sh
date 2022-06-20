vncserver
EXPORT DISPLAY=: 1
. apivenv/bin/activate

port=$1
ip=$(hostname -I | awk '{print $1}')
(uvicorn main:app --host "$ip" --port "$port")

