import ConfigParser
import logging
import logging.handlers
import os
import tarfile
import urllib
import yaml
import sys,traceback
import subprocess
from subprocess import Popen, PIPE

def exec_command(cmd):
    """
    exec command with communicate method
    """
    proc =  Popen(
            cmd, stdin=PIPE, stdout=PIPE, stderr=PIPE  
            )
    stdout, stderr = proc.communicate()
    if len(stderr) > 0 :
        return False,stderr[:-1]
    else :
        return True,stdout[:-1]


def exec_command_with_call(cmd):
    """
    exec command with call method
    """
    return subprocess.call(cmd)

def makedirs(path):
    """
    """
    if os.path.exists(path):
        print 'aleady exists'
    else :
        os.makedirs(path)

def remove_dir(path):
    """
    """
    if not os.path.exists(path):
        return

    for root,dirs,files in os.walk(path, topdown=False):
        for file in files:
            os.remove(os.path.join(root,file))

        #print root
        os.rmdir(root)
    return

def init_logger(level, log_file):
    """
    """
    fmt_str = '%(asctime)-15s %(name)s %(levelname)s %(message)s'
    formatter = logging.Formatter(fmt_str)
    log = logging.getLogger('llvmenv')

    ########################################
    # RotateHandler
    #
    rotate_handler = logging.handlers.RotatingFileHandler(log_file, maxBytes=1024*1024*10, backupCount=10)
    rotate_handler.setFormatter(formatter)
    log.addHandler(rotate_handler)

    ########################################
    # StreamHandler
    #
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    log.addHandler(stream_handler)

    level=level.lower()
    if level == 'debug':
        log.setLevel(logging.DEBUG)
    elif level == 'info':
        log.setLevel(logging.INFO)
    elif level == 'critical':
        log.setLevel(logging.CRITICAL)
    elif level == 'warn':
        log.setLevel(logging.WARN)
    elif level == 'error':
        log.setLevel(logging.ERROR)
    else:
        log.setLevel(logging.INFO)
    return


def download(url, target_file):
    try:
        (filename, headers) = urllib.urlretrieve(url, target_file)
    except IOError, e:
        traceback.print_exc(file=sys.stdout)
    urllib.urlcleanup()
    return filename

def decompress_xz(target_file, target_dir = None):
    """
    in python 2.x, xzlib is not included in standard library
    """
    cmd =['xz', '-d', target_file]
    exec_command(cmd)


def extract(archive, target_dir):
    """
    """
    tarball = tarfile.TarFile(archive)
    tarball.extractall(target_dir)


def get_logger():
    """
    """
    return logging.getLogger('llvmenv')

def load_config(file_path):
    """
    """
    print 'load config from ... %s ' % file_path
    conf = ConfigParser.SafeConfigParser()
    conf.read(file_path)
    return conf

def load_yaml(file_path):
    print 'load yaml file from ... %s ' % file_path
    data = yaml.safe_load(open(file_path))
    return data
