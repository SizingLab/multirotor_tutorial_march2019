#!/usr/bin/env python
# -*- coding: utf-8 -*-


# ======================================================================================================================
# Scott Delbecq
# ISAE Supaero
# ======================================================================================================================

from .model_serializer import ModelSerializer
import pandas as pd
import ipywidgets as widgets


class CoreModel(object):
    """
    Core model class.
    ----------
    
    """

    def __init__(self, name, **kwargs):
        
        # Name
        self.name = name

        # Inputs 
        self.inputs = []

        # Outputs
        self.outputs = []

        # Parameters
        self.parameters = dict()
        
        # Dataframe
        self.data_frame = pd.DataFrame()

    def _set_inputs(self, inputs):
        for inp in inputs:
            self.parameters[inp] = inputs[inp]
        
    def add_input(self, name, value=1.0, unit='-', comment=''):
        self.parameters[name] = value
        self.inputs.append(name)
        self._declare_variable(name, value=str(value), unit=unit, comment=comment)

    def add_output(self, name, unit='-', comment=''):
        self.parameters[name] = float('nan')
        self.outputs.append(name)
        self._declare_variable(name, value='nan', unit=unit, comment=comment)

    def get_values(self, parameters):
        # The returned values are in the same order as the requested parameters
        if len(parameters) == 1:
            param_values = self.parameters[parameters[0]]
        else:
            param_values = []
            for param in parameters:
                param_values.append(self.parameters[param])
        
        return param_values
    
    def _update(self):
        for i, (param, value) in enumerate(self.parameters.items()):
            self.data_frame.loc[self.data_frame['Variable'] == param, 'Value'] = value

    def compute(self, inputs=None):
        if inputs != None:
            self._set_inputs(inputs)
        self.computation_script()
        
    def _declare_variable(self, name, value='0.0', unit='-', comment=''):
        data =  [{'Component': self.name, 'Variable': name, 'Value': value, 'Unit': '[' + unit + ']', 'Comment': comment}]
        col_names = ['Component', 'Variable', 'Value', 'Unit', 'Comment']
        self.data_frame = self.data_frame.append(data)[col_names]
          
    def f(self, Component):
        return self.data_frame[self.data_frame.Component==Component]
    
    def print_variables(self):
        self._update()
        widgets.interact(self.f, Component=set(self.data_frame.Component))
    
    def initialization(self):
        
        pass

    def computation_script(self):

        pass

    
class Model(CoreModel):
    """
    Model class.
    ----------
    
    """

    def __init__(self, name, **kwargs):
        super(Model, self).__init__(name, **kwargs)
        # Submodels 
        self.submodels = dict()

    def add_submodel(self, submodel, name=None):
        if name == None:
            name = submodel.name
        else:
            submodel.name = name
            
        existing_parameters = self.parameters.keys()
        
        for i, (param, value) in enumerate(submodel.parameters.items()):
            if param not in existing_parameters:
                self.parameters[param] = value
                
        self.submodels[name] = submodel
        self.data_frame = self.data_frame.append(submodel.data_frame)
    
    def run_submodel(self, name):
        submodel = self.submodels[name]
        
        inputs = {}
        outputs = submodel.outputs
        
        for inp in submodel.inputs:
            inputs[inp] = self.parameters[inp]
        
        submodel.compute(inputs)
        
        for out in outputs:
            self.parameters[out] = submodel.parameters[out]
    
    def initialization(self):

        pass

    def computation_script(self):

        pass

    
class ExampleModel(CoreModel):
    """
    Example model class.
    ----------
    """

    def initialization(self):
        
        # Inputs 
        self.add_input('a', value=1.0)
        self.add_input('b', value=2.0)
        
        # Outputs
        self.add_output('y')

    def computation_script(self):
        p = self.parameters
        a = p['a']
        b = p['b']

        y = a + b

        p['y'] = y


if __name__ == "__main__":
    
    
    model = ExampleModel('example')
    model.initialization()
    
    inputs = {'a': 4.0, 'b': 2.0}
    
    model.compute(inputs)
    res = model.parameters['y']
    print(model.parameters)

    print("The result is : ", res)

    ms = ModelSerializer()

    ms.save_model(model, 'example_model')

    new_model = ms.load_model('example_model')










