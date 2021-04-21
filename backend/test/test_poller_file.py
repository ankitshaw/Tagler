import sys
sys.path.insert(1, '/workspaces/Tagler-Hackathon/backend')

from tagler.poller.file import FilePoller
from tagler.poller.sql import SqlPoller
import time
import logging as LOGGER
LOGGER.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=LOGGER.DEBUG)

x = FilePoller("/workspaces/Tagler-Hackathon/backend/test/test_log.txt")
s = SqlPoller(conn_string="sqlite:///tagler.db",)
s.set_query_details("logs","1","exception_input","exception_tag")
while True:
    for i in s.poll():
        print(i)
    
    LOGGER.debug("Sleeping for 5 secs")
    time.sleep(5)
