PORT=8000
if lsof -Pi :$PORT -sTCP:LISTEN > /dev/null ; then
    echo "Port $PORT is in use. Killing process..."
    sudo fuser -k $PORT/tcp || true
fi

echo "Starting server on port $PORT"
python manage.py runserver