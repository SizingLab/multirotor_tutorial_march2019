#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ======================================================================================================================
# Scott Delbecq
# ISAE Supaero
# ======================================================================================================================

import cloudpickle


class ModelSerializer(object):

    def __init__(self, **kwargs):
        super(ModelSerializer, self).__init__(**kwargs)
        
    def save_model(self, model, file_name: 'default_model'):

        with open(file_name + '.mdl', 'wb') as file:
            cloudpickle.dump(model, file)

    @staticmethod    
    def load_model(file_name):
        with open(file_name + '.mdl', 'rb') as file:
           model =  cloudpickle.load(file)
        return model
