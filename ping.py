import datetime
import logging
import os
from pathlib import Path
import sys
import time
import vlc

from utils import check_methods
from utils import tools


def main():
    # Constant string for logging to remind user of usage of programs and/or flags
    USAGE_STRING = "Usage: python ping.py ping_or_request [flag] [flag_value]"
    HELP_REMINDER = "To see all aviable flags, us -h or --help"
    HELP_STRING = \
    """ Aviable flags:
    -h, --help: display this message of flags functions;
    -wl, --web_link: change link at which will be requests/pings directed;
    -v, --volume: change level of volume. Can be set from 0 to 100;
    -s, --sound: change sound that will play, when internet is functional. File should be in the same directory of the ping.py script;
    -lv, --log_level: set the log_level of the whole script;
    -lf, --log_file: change file in which logs will be written. File will be created in the logs directory, which will be located in the same directory as the ping.py script."""

    start_timer = time.perf_counter()
    
    # Set up the conditionals that can be change via flags
    site_to_ping = "google.com"
    volume_level = 100
    sound_to_play = "sounds/Gall_-_Embrace_the_Shadow.oga"
    is_help_flag = False
    log_level = logging.DEBUG
    log_file = 'process.log'

    # Get flags and chang conditionals    
    #TODO: Check the functionality of flags
    # Additionaly: create tests
    argc = len(sys.argv)
    
    for flag_position, flag in enumerate(sys.argv):
        next_position = flag_position + 1
        
        if tools.check_flag_to_keys(flag, ["-h", "--help"]):
            is_help_flag = True
                
        if tools.check_flag_to_keys(flag, ["-wl", "--web_link"]):
            if tools.check_next_flag_bounds(argc, next_position):
                site_to_ping = int(sys.argv[next_position])
        
        if tools.check_flag_to_keys(flag, ["-v", "--volume"]):
            if tools.check_next_flag_bounds(argc, next_position):
                volume_level = int(sys.argv[next_position])
                
        if tools.check_flag_to_keys(flag, ["-s", "--sound"]):
            if tools.check_next_flag_bounds(argc, next_position):
                sound_to_play = sys.argv[next_position]
                
        if tools.check_flag_to_keys(flag, ["-lv", "--log_level"]):
            if tools.check_next_flag_bounds(argc, next_position):
                log_level = sys.argv[next_position]
                
        if tools.check_flag_to_keys(flag, ["-lf", "--log_file"]):
            if tools.check_next_flag_bounds(argc, next_position):
                log_file = sys.argv[next_position]
    
    # Set up logger instance
    logger = logging.getLogger(str(datetime.datetime.now()))                              
    logger.setLevel(log_level)
    
    # Create and setup FileHandler
    log_file = Path(__file__).parent.joinpath("logs/"+log_file)
    try:
        file_handler = logging.FileHandler(log_file)
    except FileNotFoundError:
        os.mkdir("logs")
        file_handler = logging.FileHandler(log_file)
        
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    file_handler.setLevel(logging.DEBUG)  
    
    # Create and setup ConsoleHandler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    # Ensure that program was given more then 2 flags
    if argc < 2:
        logger.warning(USAGE_STRING)
        logger.warning(HELP_REMINDER)
        return 1
    # Setup the method of pinging
    if sys.argv[1] == "ping":
        server= site_to_ping
        request_process = check_methods.ping_after_some_time
        message_starter = "Ping"
    elif sys.argv[1] == "request":
        server= "https://"+site_to_ping
        request_process = check_methods.make_request_after_some_time
        message_starter = "Request"
    # Give warning if the method was given wrong
    else:
        logger.warning(USAGE_STRING)
        if is_help_flag:
            logger.warning(HELP_STRING)
        return 1
    
    if is_help_flag:
        logger.warning(USAGE_STRING)
        logger.warning(HELP_STRING)

    # Start pinging process
    request_count = check_methods.make_request_until_its_successful(
        server= server,
        request_process= request_process,
        
        logger= logger,
        message_starter= message_starter,
        
        request_count = 0,
        start_time_to_wait=time.perf_counter(),
        
        time_to_wait=10
    )

    # Play sound
    tools.play_sound(
        Path(__file__).parent.joinpath(sound_to_play), 
        volume_level
    )
            
    logger.info(f"Successful request was made after {request_count} attempts")
    logger.info(f"The whole program took {time.perf_counter() - start_timer} seconds to run")
    return 0

if __name__ == "__main__":
    main()