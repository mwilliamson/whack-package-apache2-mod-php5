import os
import subprocess
import time

from nose.tools import istest, assert_equals
from starboard import find_local_free_tcp_port as find_port
import requests

from tempdir import create_temporary_dir


@istest
def php_files_are_served():
    with create_temporary_dir() as temp_dir:
        port = find_port()
        install_apache2(temp_dir, port=port)
        write_php_file(temp_dir)
        process = subprocess.Popen(
            ["bin/httpd", "-DNO_DETACH"],
            cwd=temp_dir
        )
        try:
            assert_php_file_is_visible(port=port)
        finally:
            process.terminate()


def install_apache2(directory, port):
    path = os.path.join(os.path.dirname(__file__), "..")
    subprocess.check_call(["whack", "install", path, directory,"--no-cache"])
    
    conf_path = os.path.join(directory, "conf/httpd.conf")
    with open(conf_path, "r") as conf_file:
        original_conf_contents = conf_file.read()
    conf_contents = original_conf_contents.replace("Listen 80", "Listen {0}".format(port))
    with open(conf_path, "w") as conf_file:
        conf_file.write(conf_contents)

def write_php_file(apache_root):
    path = os.path.join(apache_root, "htdocs/hello.php")
    with open(path, "w") as php_file:
        php_file.write("<?php echo 'Hello from PHP';\n")

def assert_php_file_is_visible(port):
    time.sleep(1)
    url = "http://localhost:{0}/hello.php".format(port)
    response_text = requests.get(url).text
    assert_equals("Hello from PHP", response_text)
