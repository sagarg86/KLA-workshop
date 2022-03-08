import yaml
import logging


with open('Milestone1A.yaml') as fh:

    read_data = yaml.load(fh, Loader=yaml.FullLoader)


Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile1.log",
                    filemode = "w",
                    format = Log_Format
                    )

logger = logging.getLogger('TaskA')
logger.error("Mywork entry")

