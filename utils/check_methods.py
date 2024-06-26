from collections.abc import Callable
import logging
import os
import requests
import subprocess
import time
from urllib3 import exceptions



def ping_after_some_time(
    server: str,
    request_count: int,
    logger: logging.Logger,
    start_time_to_wait:float,
    time_to_wait: int = 1,
    n_of_pings: int = 1
):
    end_time_to_wait = time.perf_counter()    
    while end_time_to_wait - start_time_to_wait < time_to_wait:
        end_time_to_wait = time.perf_counter()
    command = ['ping', "-c", str(n_of_pings), str(server)]
    with open(os.path.abspath(logger.handlers[0].stream.name), "a") as file:
        pinging = subprocess.call(
            command, 
            stdout=file,
            stderr=file
        )
    
    end_time_to_wait = time.perf_counter()
    
    logger.debug(f"Ping numder {request_count} took {end_time_to_wait-start_time_to_wait} time to get")
    
    return pinging
        
def make_request_after_some_time(
    server: str,
    request_count: int,
    logger: logging.Logger,
    start_time_to_wait:float = time.perf_counter(),
    time_to_wait: int = 1
) -> tuple:

    end_time_to_wait = time.perf_counter()
    while end_time_to_wait - start_time_to_wait < time_to_wait:
        end_time_to_wait = time.perf_counter()
    try: 
        server_request = requests.get(
            server, 
            timeout=10
        )
    # If we recieve exeption that indicates that connection wasn`t aquired,
    # we return None to indicate it  
    except (requests.exceptions.ReadTimeout, ConnectionResetError, exceptions.ProtocolError, requests.exceptions.ConnectionError) as occured_exception:
        end_time_to_wait = time.perf_counter()
        logger.debug(
            f"While getting request numder {request_count} recieve {occured_exception}. It took {end_time_to_wait-start_time_to_wait} time to get exception"
        )
        return None
    else:
        end_time_to_wait = time.perf_counter()
        logger.debug(f"Request numder {request_count} took {end_time_to_wait-start_time_to_wait} time to get")
        return server_request
    
def make_request_until_its_successful(
    server: str,
    request_process: Callable,
    
    logger: logging.Logger,
    message_starter: str,
    
    request_count: int,
    start_time_to_wait:float, # Cannot use = time.perf_counter() ->  
        # If we use it like this, in loop it will bug out and use only the 1st value
        
    time_to_wait:int = 1
) -> tuple:

    # We need server_request_status_code to start up cycle
    is_going = 1
    start_time_to_wait = start_time_to_wait - time_to_wait
    while (
        is_going != 0
    ):  
        request_count += 1
        server_request = request_process(
            server=server,
            request_count=request_count,
            logger = logger,
            start_time_to_wait=start_time_to_wait,
            time_to_wait=time_to_wait
        )
        
        # After make_request_after_some_time returns requests.Response,
        # we can read its status_code and if it indicates about successful response, programme proceed
        
        if not server_request is None:
            if isinstance(server_request, requests.Response):
                server_request_status_code = server_request.status_code
                if server_request_status_code == 200:
                    is_going = 0

            elif isinstance(server_request, int): 
                server_request_status_code = server_request
                is_going = server_request
               
            if request_count == 1:
                logger.info(f"Process started. {message_starter} numder {request_count} returned {server_request_status_code} status_code.")
            else:
                logger.debug(f"{message_starter} numder {request_count} returned {server_request_status_code} status_code.")
        
        start_time_to_wait = time.perf_counter()

    del start_time_to_wait
    return request_count
