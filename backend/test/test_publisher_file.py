import sys
sys.path.insert(1, '/workspaces/Tagler-Hackathon/backend')

from tagler.poller.file import FilePoller
from tagler.publisher.file import FilePublisher
import time
import logging as LOGGER
LOGGER.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=LOGGER.DEBUG)

x = FilePoller("/workspaces/Tagler-Hackathon/backend/test/test_log.txt")
fp = FilePublisher("/workspaces/Tagler-Hackathon/backend/test/i.txt","/workspaces/Tagler-Hackathon/backend/test/o.txt")
while True:
    for i in x.poll():
        print(i)
        fp.append(i,"ok")

    LOGGER.debug("Sleeping for 10 secs")
    time.sleep(5)
