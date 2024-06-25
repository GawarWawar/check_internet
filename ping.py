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
    start_timer = time.perf_counter()
    
    site_to_ping = "google.com"
    volume_level = 100
    sound_to_play = "sounds/Gall_-_Embrace_the_Shadow.oga"
    is_help_flag = False
    log_level = logging.DEBUG
    log_file = 'process.log'
    
    USAGE_STRING = "Usage: python ping.py ping_or_request [flag] [flag_value]"
    # TODO: write full description of flags
    help_string = \
    """    -h, --help:
    -v, --volume:
    -s, --sound:
    -lv, --log_level:
    -lf, --log_file:
    """
    
    #TODO: Check the functionality of flags
    # Additionaly: create tests
    argc = len(sys.argv)
    
    for flag_position, flag in enumerate(sys.argv):
        next_position = flag_position + 1
        
        if tools.check_flag_to_keys(flag, ["-h", "--help"]):
            is_help_flag = True
                
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
    
    logger = logging.getLogger(str(datetime.datetime.now()))                              
    logger.setLevel(log_level)
    
    # FileHandler
    try:
        file_handler = logging.FileHandler(Path(__file__).parent.joinpath("logs/"+log_file))
    except FileNotFoundError:
        os.mkdir("logs")
        file_handler = logging.FileHandler(Path(__file__).parent.joinpath("logs/"+log_file))
        
    file_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )
    file_handler.setLevel(logging.DEBUG)  
    
    # ConsoleHandler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  
    console_handler.setFormatter(logging.Formatter('%(message)s'))
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    if sys.argv[1] == "ping":
        server= site_to_ping
        request_process = check_methods.ping_after_some_time
        message_starter = "Ping"
        
    elif sys.argv[1] == "request":
        server= "https://"+site_to_ping
        request_process = check_methods.make_request_after_some_time
        message_starter = "Request"
    else:
        logger.warning(USAGE_STRING)
        if is_help_flag:
            logger.warning(help_string)
        return 1
            
    if is_help_flag:
        logger.warning(USAGE_STRING)
        logger.warning(help_string)
        
    
    if argc >= 3:
        for flag_position, flag in enumerate(sys.argv, 2):
            next_position = flag_position + 1
            
            if tools.check_flag_to_keys(flag, ["-h", "--help"]):
                if tools.check_next_flag_bounds(argc, next_position):
                    print(USAGE_STRING)
                    # TODO: Import flags description
                    print()
                    
            if tools.check_flag_to_keys(flag, ["-v", "--volume"]):
                if tools.check_next_flag_bounds(argc, next_position):
                    volume_level = sys.argv[next_position]
                    
            if tools.check_flag_to_keys(flag, ["-s", "--sound"]):
                if tools.check_next_flag_bounds(argc, next_position):
                    sound_to_play = sys.argv[next_position]
                    
            if tools.check_flag_to_keys(flag, ["-s", "--sound"]):
                if tools.check_next_flag_bounds(argc, next_position):
                    sound_to_play = sys.argv[next_position]


    request_count = check_methods.make_request_until_its_successful(
        server= server,
        request_process= request_process,
        
        logger= logger,
        message_starter= message_starter,
        
        request_count = 0,
        start_time_to_wait=time.perf_counter(),
        
        time_to_wait=10
    )

    
    sounds_player : vlc.MediaPlayer = vlc.MediaPlayer(
        Path(__file__).parent.joinpath(sound_to_play)
    )
    sounds_player.audio_set_volume(volume_level)
    sounds_player.play()

    while sounds_player.is_playing() == 0:
        ...
    while sounds_player.is_playing() == 1:
        ...
        
    logger.info(f"Successful request was made after {request_count} attempts")
    logger.info(f"The whole program took {time.perf_counter() - start_timer} seconds to run")
    return 0

if __name__ == "__main__":
    main()