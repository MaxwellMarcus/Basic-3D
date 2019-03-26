import random

class Synapse:
    def __init__(self,neuron1,neuron2,weight):
        self.weight = weight
        self.neuron1 = neuron1
        self.neuron2 = neuron2
    def get_value(self):
        return self.neuron1.value*self.weight

class Neuron:
    def __init__(self,type):
        self.value = 0
        self.type = type
        self.synapses = []
        self.values = []
    def add_synapse(self,x):
        self.synapses.append(x)
    def set_new_value(self):
        val = 0
        for i in self.values:
            val += i
        val /= len(self.values)
        self.value = val

class Net:
    def __init__(self,rows,neuron_per_row,input):
        self.rows = rows
        self.neuron_per_row = neuron_per_row
        self.neurons = []
        for i in range(rows):
            if i == 0:
                sublist = []
                for l in range(neuron_per_row):
                    neuron = Neuron(1)
                    sublist.append(neuron)
                self.neurons.append(sublist)#dont forget to add the other types of neurons
            elif i == rows-1:
                sublist = []
                for l in range(neuron_per_row):
                    neuron = Neuron(3)
                    sublist.append(neuron)
                self.neurons.append(sublist)#dont forget to add the other types of neurons
            else:
                sublist = []
                for l in range(neuron_per_row):
                    neuron = Neuron(2)
                    sublist.append(neuron)
                self.neurons.append(sublist)#dont forget to add the other types of neurons

        for i in self.neurons:
            for l in i:
                if not self.neurons.index(i) == self.rows - 1:
                    for q in range(self.neuron_per_row):
                        l.add_synapse(Synapse(l,self.neurons[self.neurons.index(i)+1],float(random.randint(-10,10))/10))
    def get_output(self):
        for i in self.neurons:
            for l in i:
                for q in l.synapses:
                    q.neuron2.set_value(q.get_value())
