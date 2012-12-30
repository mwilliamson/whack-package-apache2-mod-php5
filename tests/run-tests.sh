cd $(dirname $0)

if [ ! -d _virtualenv ];
then
    virtualenv _virtualenv
fi

_virtualenv/bin/pip install -r requirements.txt
source _virtualenv/bin/activate
nosetests installation_test.py -m'^$'
