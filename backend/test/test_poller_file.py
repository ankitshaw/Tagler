import sys
sys.path.insert(1, '/workspaces/Tagler-Hackathon/backend')

from tagler.poller.file import FilePoller
import time
import logging as LOGGER
LOGGER.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=LOGGER.DEBUG)

x = FilePoller("/workspaces/Tagler-Hackathon/backend/test/test_log.txt")
while True:
    for i in x.poll():
        print(i)
    
    LOGGER.debug("Sleeping for 10 secs")
    time.sleep(5)
