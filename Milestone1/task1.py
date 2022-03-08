import yaml
import logging

#Creating and Configuring Logger


#Testing our Logger


with open('Milestone1A.yaml') as fh:

    read_data = yaml.load(fh, Loader=yaml.FullLoader)


Log_Format = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename = "logfile1.log",
                    filemode = "w",
                    format = Log_Format,
                    level = logging.ERROR)

logger = logging.getLogger()

logger.error("my workflow entry")

