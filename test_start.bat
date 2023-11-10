call .venv/Scripts/activate
START "Image Stream" py vehicle_tracking_configurator/test_image_transpmitter.py
START "Main" py main.py