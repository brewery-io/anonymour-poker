import os
import json

class Config:

    @staticmethod
    def get():

        this = os.path.dirname(os.path.abspath(__file__))
        f = open(os.path.join(this, '../../config/config.json'))
        res = json.load(f.read())
        f.close()
        return res
