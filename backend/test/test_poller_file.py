#import sys
#sys.path.insert(1, '/workspaces/Tagler-Hackathon/backend')
import logging as LOGGER
import time

from tagler.poller.file import FilePoller
from tagler.poller.sql import SqlPoller
from tagler.publisher.sql import SqlPublisher

LOGGER.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s', level=LOGGER.DEBUG)

#x = FilePoller("/workspaces/Tagler-Hackathon/backend/test/test_log.txt")
s = SqlPoller(conn_string="sqlite:///tagler.db",)
sp = SqlPublisher(s.conn)
s.set_query_details("logs",2,"exception_input","exception_tag")
sp.set_query_details("logs","id","exception_tag")

while True:
    for i in s.poll():
        print(i)
        #tagging nlp model
        #es rule extract
        #if confident update predicted tag and extract heal condition else update Not Processed and skip heal
        sp.prepare_update(i[0],"System Exception")

    sp.write_result()    
    LOGGER.debug("Sleeping for 5 secs")
    time.sleep(5)
