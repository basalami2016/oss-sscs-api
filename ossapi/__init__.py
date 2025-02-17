from ado.boards import WorkItemApi


import os
import re
import logging
import codecs
from logging.handlers import RotatingFileHandler

class AuditEventLogger:
    """Class for keeping track of event in the ossbot.
    NOTE For BOT instantiate in in each method to provide use info, IP Address etc actitivies to perform, channels info etc
    Stackoverflow: How to write to a file, using the logging Python module
    - record the following information with each event:
        - identity of the user that caused the event,
        - a description of the event (supplied by the caller),
        - whether the event succeeded or failed (indicated by the caller),
        - severity level of the event (indicated by the caller),
        - that this is a security relevant event (indicated by the caller),
        - hostname or IP where the event occurred (and ideally the user's source IP as well),
        - a time stamp      
    """   

    def __init__(self, classzname: str, user: str, ip: str, email: str, channel: str):
                     
        formatter = logging.Formatter(
            "%(asctime)s %(module)s:%(lineno)d %(processName)s %(name)s %(levelname)s %(message)s",
            "%a, %d %b %Y %H:%M:%S"            
        ) 
        file_handler = RotatingFileHandler(
            "app.log",
            maxBytes=1024 * 1024, 
            backupCount=5,  
        )
        file_handler.setFormatter(formatter) 
        console_handler = logging.StreamHandler()  
        console_handler.setFormatter(formatter)
             
        clogger = logging.getLogger(classzname)  
        clogger.addHandler(file_handler) 
        clogger.addHandler(console_handler)     
        clogger.setLevel(logging.DEBUG) 
        self.logger = AdapterHandler(clogger, {"Process ID": os.getpid(), "IP Address": ip, "User": user, "Channel": channel, "Email": email, }, )
        self.pattern = re.compile("[^[a-zA-Z0-9 .-]+$]")  
        self.msg = None                         
                                                
    async def logEvent(self, message: any, level: str):  
        try: 
            if message is None:  
                raise ValueError("message is a required argument.")
            
            if level is None:  
                raise ValueError("EventLogLevel is a required argument.")  

            sanitize = self.sanitize_message(message)    
                 
            match level:
                case "CRITICAL":                   
                    self.logger.critical(self.msg)

                case "ERROR":
                    self.logger.error(self.msg)                  

                case "WARNING":                   
                    self.logger.warning(self.msg)

                case "INFO":                              
                    self.logger.info(sanitize)

                case "DEBUG":                   
                    self.logger.debug(self.msg)
              
        except Exception as ex:
            pass

        else:  # executed if NO exception occurs in the try block
            pass

        finally:  # ALWAYS be executed, regardless of whether an exception occurred
            pass

    def sanitize_message(self, message):
        if self.pattern.fullmatch(message):            
           return message
        else: 
           message = codecs.encode(message, "utf-8")
           return message

    
class AdapterHandler(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return (
            "[Process ID: %s] [IP: %s] [User: %s] [Channel: %s] [Email: %s] [Message: %s]"
            % (
                self.extra["Process ID"],
                self.extra["IP Address"],
                self.extra["User"],
                self.extra["Channel"],
                self.extra["Email"],
                msg,
            ),
            kwargs,
        )
