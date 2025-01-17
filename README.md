# RAAI Module Vehicle Tracking Configurator

## Setup

You need to install all the required packages in the requirements.txt file. It is recommended to use a virtual environment.

```bash
python.exe -m venv venv
call venv\Scripts\activate.bat
pip install -r requirements.txt
```

## Download pre-recorded videos (optional)

You can use the [download_resources.py](utils/download_resources.py) script to download pre-recorded videos from the NG:ITL cloud. The downloaded files are stored in the [resources](resources) folder.

To use the pre-recorded videos you will need to make sure that no other program is using the `ipc:///tmp/RAAI/camera_frame.ipc` address.

## Starting

### Using the Camera Image Stream

Before you can start the configurator module, you will have to start the [raai_module_vehicle_tracking](https://github.com/vw-wob-it-edu-ngitl/raai_module_vehicle_tracking_configurator).

### Using a Video File

To start the program using a video file, you will have to [download the video file](#download-pre-recorded-videos-optional) as described above. Then you can start the configurator and use it like normal.

## Possible Ideas for Improvement

- Make it so that arrow-up and arrow-down can be used to change the selected config. (ROI <-> T-Points <-> Time Tracking)
- Implement time tracking.
- Give visual feedback if the config has been sent/received. (sent correctly / error received)
