Small script to check if internet is present. It makes request every 10 seconds and can be altered by the flags which are given to the script through console.
Usage: python ping.py ping_or_request [flag] [flag_value]
To see all aviable flags, us -h or --help
Aviable flags:
    -h, --help: display message of all aviable flags;
    -wl, --web_link: change link at which will be requests/pings directed;
    -v, --volume: change level of volume. Can be set from 0 to 100;
    -s, --sound: change sound that will play, when internet is functional. File should be in the same directory of the ping.py script;
    -lv, --log_level: set the log_level of the whole script;
    -lf, --log_file: change file in which logs will be written. File will be created in the logs directory, which will be located in the same directory as the ping.py script.