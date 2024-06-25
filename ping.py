import datetime
import logging
import os
from pathlib import Path
import sys
import time
import vlc

from utils import check_methods


def main():
    start_timer = time.perf_counter()
    
    if len(sys.argv) != 2:
        print("Usage: python ping.py ping_or_request")
        return 1
    elif sys.argv[1] == "ping":
        server= "google.com"
        request_process = check_methods.ping_after_some_time
        message_starter = "Ping"
        
    elif sys.argv[1] == "request":
        server= "https://google.com"
        request_process = check_methods.make_request_after_some_time
        message_starter = "Request"

    else:
        print("Usage: python ping.py ping_or_request")
        return 1
    
    logger = logging.getLogger(str(datetime.datetime.now()))
    logger.setLevel(logging.DEBUG)
    
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # FileHandler
    try:
        file_handler = logging.FileHandler(Path(__file__).parent.joinpath('logs/process.log'))
    except FileNotFoundError:
        os.mkdir("logs")
        file_handler = logging.FileHandler(Path(__file__).parent.joinpath('logs/process.log'))
        
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  
    
    # ConsoleHandler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)  
    console_handler.setFormatter(formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


    request_count = check_methods.make_request_until_its_successful(
        server= server,
        request_process= request_process,
        
        logger= logger,
        message_starter= message_starter,
        
        request_count = 0,
        start_time_to_wait=time.perf_counter(),
        
        time_to_wait=10
    )

    
    p = vlc.MediaPlayer(Path(__file__).parent.joinpath("sounds/Gall_-_Embrace_the_Shadow.oga"))
    p.play()

    while p.is_playing() == 0:
        ...
    while p.is_playing() == 1:
        ...
        
    logger.info(f"Successful request was made after {request_count} attempts")
    logger.info(f"The whole program took {time.perf_counter() - start_timer} seconds to run")
    return 0

if __name__ == "__main__":
    main()