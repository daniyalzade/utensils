"""A collection of utility methods for configuring logging.
"""
import logging
import logging.handlers
requests_log = logging.getLogger("requests")
requests_log.setLevel(logging.WARNING)
import socket

LOG_FORMAT = '%(asctime)s %(levelname)s pid:%(process)d, file:%(filename)s:%(lineno)d> %(message)s'

STATUS_LOGGER = logging.getLogger("status_logger")
STATS_LOGGER = logging.getLogger("stats_logger")

_peripheral_loggers = {
    'stats': STATS_LOGGER,
    'status' : STATUS_LOGGER,
}

def type_of(inst, klass):
    return inst.__class__.__name__ == klass.__name__

def append_to_filename(filename, to_append):
    return filename.replace(".log", "_%s.log" % to_append)

def _get_stream_handler(logger):
    """
    Return the first stream handler the logger has, and None ow
    """
    for handler in logger.handlers:
        if type_of(handler, logging.StreamHandler):
            return handler
    return None

def _configure_error_recipients(formatter, error_recipients=None,
        **kwargs):
    """
    @param error_recipients: list(str)
    """
    if not error_recipients:
        return
    smtp_handler = logging.handlers.SMTPHandler('localhost',
                                                socket.gethostname(),
                                                error_recipients,
                                                'Log[ERROR]'
                                                )
    smtp_handler.setLevel(logging.ERROR)
    smtp_handler.setFormatter(formatter)
    logging.getLogger().addHandler(smtp_handler)
    logging.info('configured error_recipients: %s' % error_recipients)

def _configure_stream_handler(level, formatter):
    """
    Add a stream handler if it does not already exist
    """
    root_logger = logging.getLogger()
    handler = _get_stream_handler(root_logger)
    if handler:
        handler.setLevel(level)
        handler.setFormatter(formatter)
        return
    ch = logging.StreamHandler()
    ch.setLevel(level)
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)

def _get_log_level(options):
    """
    @param options: pychartbeat.Options
    @return log_level: int (backed by logging.LEVEL constant)
    """
    if 'loglevel' in options and options.loglevel:
        loglevel = options.loglevel.lower()
        if loglevel == 'debug': return logging.DEBUG
        if loglevel == 'info': return logging.INFO
        if loglevel == 'warning': return logging.WARNING
        if loglevel == 'error': return logging.ERROR
        if loglevel == 'fatal': return logging.FATAL
    if 'debug' in options:
        return logging.DEBUG if options.debug else logging.INFO
    return logging.INFO

def _options_to_config(options):
    logging_config = {'filename' : options.log_file} if 'log_file' in options else {}
    logging_config['console'] = options.console
    logging_config['enable_stats'] = options.enable_stats
    error_recipients = options.error_recipients if 'error_recipients' in options else None
    logging_config['error_recipients'] = error_recipients
    logging_config['level'] = _get_log_level(options)
    return logging_config

def _configure_peripheral_logger(filename, level, logger_type):
    peripheral_logger = _peripheral_loggers[logger_type]
    filename = append_to_filename(filename, logger_type)
    fh = logging.FileHandler(filename)
    fh.setLevel(level)
    fh.setFormatter(formatter)
    peripheral_logger.addHandler(fh)

def basicConfig(level=logging.INFO,
                options=None,
                console=True,
                error_log=None,
                enable_stats=False,
                error_recipients=None,
                **kwargs):
    """
    Utility method for configuring logging. Note that the allowed arguments
    are (and should better be) a supperset of python's logging.basicConfig

    @param level: Logging level
    @param error_log: If provided configures another file handler to
    output error logs to the provided file name
    @param extra_args: Optional.
    @param error_recipients: list(str)
    """
    if options:
        basicConfig(**_options_to_config(options))
        return
    logging_format = kwargs.get('format', LOG_FORMAT)
    logging.getLogger().setLevel(level)
    formatter = logging.Formatter(logging_format)
    #Even if no stream handlers given, logging just logs to STDOUT. So,
    #if don't want to log, just set the handler level high
    _configure_stream_handler(level if console else logging.CRITICAL, formatter)
    if kwargs.get('filename', None):
        filename = kwargs['filename']
        fh = logging.FileHandler(filename)
        fh.setLevel(level)
        fh.setFormatter(formatter)
        logging.getLogger().addHandler(fh)
        #TODO: Change the portion below to use _peripheral_logger_configuration
        if enable_stats:
            filename = append_to_filename(filename, "stats")
            fh = logging.FileHandler(filename )
            fh.setLevel(level)
            fh.setFormatter(formatter)
            STATS_LOGGER.addHandler(fh)
            STATS_LOGGER.propagate = False


    if error_log:
        eh = logging.FileHandler(error_log)
        eh.setLevel(logging.WARN)
        eh.setFormatter(formatter)
        logging.getLogger().addHandler(eh)

    _configure_error_recipients(formatter,
            error_recipients=error_recipients,
            **kwargs)

    logging.debug('logging configured')
