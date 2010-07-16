import logging
logger = logging.getLogger('eduintelligent.trainingcenter')


def LOG(message, summary='',severity=logging.INFO):
    logger.log(severity, '%s \n%s', summary, message)