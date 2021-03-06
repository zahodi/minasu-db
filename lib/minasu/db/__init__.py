from .. import settings
from ..db import bucket as bucket_module
import os, shutil, yaml
#import psutil # no longer used?
import sys


class db():
    def __init__(
        self,
        instance_name,
        instance_dir=settings.default_settings["instance_dir"]
    ):
        self.instance_name = instance_name
        self.instance_dir  = instance_dir
        self.instance_path = self.instance_dir + "/" + self.instance_name
        self.data = {}

    def lock():
        '''Temporary method to store lock logic

        '''
        program = (self.instance_name in (p.name() for p in psutil.process_iter()))
        lock_dir = '/tmp/minasu/' + self.instance_name
        if os.path.exists(lock_dir) or program:
            print("Minasu instance: %s, is already running" % self.instance_name)
            print("Exiting")
            sys.exit()
        else:
            os.makedirs(lock_dir)


    # create a new db at folder location
    # def load(self) -> results[JSON]:
    # create path if doesn't exist
    # for each dir (bucket)
    #     for each yml file
    #         yaml.load()

    def load(self):
        self.data["instance_name"] = self.instance_name
        self.data["instance_dir"]  = self.instance_dir + "/"
        self.data["instance_path"] = self.instance_path + "/"
        instance = {}

        if not os.path.exists(self.instance_path):
            try:
                os.mkdir(self.instance_path)
            except OSError as e:
                if e.errno != errno.EEXIST:
                    raise
            instance["created"] = True

        else:
            instance["created"] = False
            buckets = {}
            list_of_buckets = os.listdir(self.instance_path)
            for bucket in list_of_buckets:
                bucket_path = self.instance_path + "/" + bucket + "/"
                for item in os.listdir(bucket_path):
                    if item.lower().endswith(('.yml', '.yaml')):
                        buckets[bucket] = {}
                        with open(bucket_path + item, 'r') as stream:
                            try:
                                buckets[bucket][item] = yaml.safe_load(stream)
                            except yaml.YAMLError as exc:
                                print(exc)
                                print("Unable to open %s" % item)
                                print("Verify that %s contains valid yaml" % item)
                                print("Exiting")
                                sys.exit(1)

            self.data["buckets"] = buckets

        return self.data

    def destroy(self):
        '''Recursively remove a directory and all of its contents

        Add more info here
        '''
        data = {}

        if os.path.exists(self.instance_path):
            shutil.rmtree(self.instance_path)
            data["destroyed"] = True
        else:
            data["destroyed"] = False

        return data

    def unload(self):
        ''''
        - verify that queue is empty
        - remove lockdir
        - clear self.data
        - manually close the open file?
          # when running tox we get:
          # /home/shaun/.pyenv/versions/3.6.3/lib/python3.6/unittest/case.py:605: ResourceWarning: unclosed file <_io.TextIOWrapper name='./tests/testdb/bucket1/file1.yml' mode='w' encoding='UTF-8'>

        '''
        pass

    def bucket(
        self,
        bucket_name=None
    ):
        return bucket_module.bucket(self,bucket_name)
