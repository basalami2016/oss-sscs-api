import logging
from pprint import pprint
from requests import exceptions
from azure.devops.connection import Connection
from msrest.authentication import BasicAuthentication
import pprint
#from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class WorkItemApi:  
    
  async  def __init__(self):
      pass

  @staticmethod
  async def getWorkItems(personal_access_token, organization_url):         
        try: 
            credentials = BasicAuthentication('', personal_access_token)
            connection = Connection(base_url=organization_url, creds=credentials)                  
            wit_client = connection.clients.get_work_item_tracking_client()    
            desired_ids = range(1, 51)
            work_items = wit_client.get_work_items(ids=desired_ids, error_policy="omit")
            for id_ , work_item in zip(desired_ids, work_items):
               if work_item is not None:                
                 print("{0} {1}: {2} {3}".format(work_item.fields["System.WorkItemType"],  work_item.id,  work_item.fields["System.Title"], work_item.fields["System.Description"] , ), )                                                  
        except exceptions.HTTPError as httpErr: 
             logger.error('{}'.format(httpErr))             
        except exceptions.ReadTimeout as timeoutErr: 
             logger.error('{}'.format(timeoutErr))  
        except exceptions.ConnectionError as connErr: 
             logger.error('{}'.format(connErr))  
        except exceptions.RequestException as requestErr: 
             logger.error('{}'.format(requestErr))  

                      
                 
class ProjectApi:  
    
  async  def __init__(self):
      pass  

  @staticmethod
  async def getAllProjects(self, personal_access_token, organization_url):       
        try:      
            credentials = BasicAuthentication('', personal_access_token)
            connection = Connection(base_url=organization_url, creds=credentials)
            core_client = connection.clients.get_core_client()
            get_projects_response = core_client.get_projects()
            index = 0
            #while get_projects_response is not None:
            for project in get_projects_response:                
                pprint.pprint("[" + str(index) + "] " + project.name)                  
            get_projects_response = None
        except exceptions.HTTPError as httpErr: 
             logger.error('{}'.format(httpErr))             
        except exceptions.ReadTimeout as timeoutErr: 
             logger.error('{}'.format(timeoutErr))  
        except exceptions.ConnectionError as connErr: 
             logger.error('{}'.format(connErr))  
        except exceptions.RequestException as requestErr: 
             logger.error('{}'.format(requestErr))      
                    
                 
  
  