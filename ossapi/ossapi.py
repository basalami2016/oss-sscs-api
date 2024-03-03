import asyncio
import json
import logging
import argparse
import os
import sys
import asyncio
import time
import datetime
from ado.boards import WorkItemApi as worksItem


logging.basicConfig(
    #level=logging.DEBUG  
    level=logging.INFO,
    #format="[%(asctime)s] {%(module)s:%(lineno)d} %(levelname)s - %(message)s"
    format='%(asctime)s:%(levelname)s:%(message)s', 
    stream=sys.stderr,    
    datefmt="%H:%M:%S",
)

#logging.getLogger("azure.devops.connection").setLevel(logging.WARNING)
#logging.getLogger("urllib3").setLevel(logging.WARNING)
#logging.getLogger("msrest.authentication").setLevel(logging.DEBUG)

logging.getLogger("azure.devops.connection").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("msrest.authentication").setLevel(logging.INFO)

logging.getLogger("chardet.charsetprober").disabled = True

#logger = logging.getLogger("areq")
logger = logging.getLogger(__name__)

#Feel free to change to Log Level of choice
logging.getLogger("azure.devops.connection").setLevel(logging.INFO)
logging.getLogger("urllib3").setLevel(logging.INFO)
logging.getLogger("msrest.authentication").setLevel(logging.INFO)

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    global access_token
    global org_url

    logger.info(datetime.datetime.now())  
    parser = argparse.ArgumentParser(description='Get data from Azure DevOps' , prog = os.path.basename(sys.argv[0]))
    
    """ 
     parser.add_argument("-u", "--ado_org_url", required=True, help="Azure DevOps Organization URL e.g. https://dev.azure.com/provide-org-url")
     parser.add_argument("-t", "--pat-file", dest='pat_file', required=True, help="Personal Pccess Token")
    """
    parser.add_argument("-c", "--config_json", dest='config_json', required=True, help="Path to JSON Config File")   
    args = parser.parse_args()
   
    """ 
    with open(args.pat_file, 'r') as tf:
        pat = tf.readline().strip()

    if pat is not None:
       #pass  
       logger.info('{}'.format(pat))    

    if args.ado_org_url is not None:
       #pass 
       logger.info('{}'.format(pat)) 
    """ 
    
    if args.config_json is not None:
        with open(args.config_json, 'r') as file:
          configInfo = json.load(file)                   
          for infos in configInfo:   
            personal_access_token = infos['personal_access_token']
            organization_url =  infos['organization_url']                  
            logging.info('\r\n  %s \r\n  %s  \r\n ',   personal_access_token ,  organization_url,)
                              
    async with asyncio.TaskGroup() as tg:    
        logger.info(f"Start at {time.strftime('%X')}")    
        async with asyncio.TaskGroup() as tg: 
          taskm = tg.create_task(
             worksItem.getWorkItems(personal_access_token, organization_url)  
          )          
          
        logger.info(f"Start at {time.strftime('%X')}")         
        logger.info(taskm.result)     
    logger.info(f"Finished at {time.strftime('%X')}")  
     

asyncio.run(main()) 



