#!/usr/bin/env python
from migrate.versioning.shell import main

if __name__ == '__main__':
    main(repository='./migrations', url='postgresql://sunshuai:123456@localhost/tempDB', debug='False')
