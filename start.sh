/home/aditya/Desktop/Code/Automation/DigitalizeADC/backend/virtualenv/bin/gunicorn adc.wsgi:application --bind 127.0.0.1:8000 --pid /tmp/gunicorn.pid