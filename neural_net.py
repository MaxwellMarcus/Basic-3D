import random
import copy
import numpy as np

class Synapse:
    def __init__(self,neuron1,neuron2,weight):
        self.weight = weight
        self.neuron1 = neuron1
        self.neuron2 = neuron2
    def get_value(self):
    #    print(type(self.neuron1.value),type(self.weight))
        return self.neuron1.value*self.weight

class Neuron:
    def __init__(self,type):
        self.value = 0
        self.type = type
        self.synapses = []
        self.values = []
    def add_synapse(self,x):
        self.synapses.append(x)
    def normalize_values(self):
        val = 0
        for i in self.values:
            val += i
        val = float(val) / len(self.values)
        self.value = val

class Net:
    def __init__(self,rows,neuron_per_row,num_input_neurons=1,num_output_neurons=1):
        self.rows = rows
        self.neuron_per_row = neuron_per_row
        self.neurons = []
        self.num_output_neurons = num_output_neurons
        self.num_input_neurons = num_input_neurons
        self.num_synapses = 0
        self.ouputs = []
        for i in range(rows):
            if i == 0:
                sublist = []
                for l in range(self.num_input_neurons):
                    neuron = Neuron(1)
                    sublist.append(neuron)
                self.neurons.append(sublist)#dont forget to add the other types of neurons
            elif i == rows-1:
                sublist = []
                for l in range(self.num_output_neurons):
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
                    for q in range(len(self.neurons[self.neurons.index(i)+1])):
                        l.add_synapse(Synapse(l,self.neurons[self.neurons.index(i)+1][q],float(random.randint(0,100))/100))
                        self.num_synapses += 1
    def get_output(self,input):
        for i in self.neurons:
            for l in i:
                l.values = []
        for i in self.neurons:
            if self.neurons.index(i) == 0:
                z = 0
                for l in i:
                    l.value = input[z]
                    z += 1

        for i in self.neurons:
            for l in i:
                for q in l.synapses:
                    q.neuron2.values.append(q.get_value())
                    q.neuron2.normalize_values()
        outputs = []
        for i in self.neurons[len(self.neurons)-1]:
            outputs.append((i.value))
        self.ouputs.append((input[0] - self.sigmoid(outputs[0])))
        return self.list_sigmoid(outputs)#self.sigmoid(outputs)
    def mutate(self,num_of_synapses_changed,amount_of_mutation):
        for loops in range(num_of_synapses_changed):
            synapapse_to_change = random.randint(0,self.num_synapses)
            synapses_found = 0
            for i in self.neurons:
                for l in i:
                    for q in l.synapses:
                        if synapses_found == synapapse_to_change:
                            amount = random.uniform(-amount_of_mutation,amount_of_mutation)
                            q.weight += amount
                        synapses_found += 1
    def get_fitness(self):
        fitness = 0
        for i in self.ouputs:
            fitness += abs(i)
        fitness /= len(self.ouputs)
        return fitness
    def sigmoid(self,input):
        output = 1/(1+np.exp(-input))
        return output
    def list_sigmoid(self,inputs):
        outputs = []
        for i in inputs:
            outputs.append(1/(1+np.exp(-i)))
        return outputs

nets = []
possible_inputs = [
[0,0,1],
[0,1,1],
[1,0,0],
[1,0,1],
[1,1,0],
[1,1,1],
]
for i in range(100):
    nets.append(Net(2,0,3,1))
    #nets[i].neurons[0][0].synapses[0].weight = 24.00872169
    #nets[i].neurons[0][1].synapses[0].weight = -0.40452123
    #nets[i].neurons[0][2].synapses[0].weight = -10.80022737
for loop in range(100):
    for i in nets:
        i.ouputs = []
    #i = [random.randint(0,1),random.randint(0,1),random.randint(0,1)]
    #while i == [0,1,0] or i == [0,0,0]:
    #    i = [random.randint(0,1),random.randint(0,1),random.randint(0,1)]
    for i in possible_inputs:
        for l in nets:
            l.get_output(i)

    sortable = {}
    for i in range(len(nets)):
        add = 0
        addable = False
        while not addable:
            try:
                sortable[nets[i].get_fitness()+add]
                add -= .01
            except:
                addable = True
        sortable.update({nets[i].get_fitness()+add: nets[i]})
    nets = []
    for i in sorted(sortable):
        nets.append(sortable[i])
    half = len(nets)/2
    #for i in nets:
        #print(i.get_fitness())

    for i in range(len(nets)):
        if i+1 == int(half):
            median = nets[i]
        if i+1 > half:
            nets[i] = copy.deepcopy(nets[int(i-half)])
            nets[i].mutate(1,1)
    #for i in nets[len(nets)-1].ouputs:
    #    if i < 0:
    #        print(i)
    #print('')
    print(nets[0].get_fitness())
while True:
    training_inputs = input('Give new input: ')
    if not training_inputs == 'synapses':
        if training_inputs == '010' or training_inputs == '000':
            print('Nope')
            break
        training_inputs = list(training_inputs)
        for i in range(len(training_inputs)):
            training_inputs[i] = int(training_inputs[i])
        print(nets[len(nets)-1].get_output(training_inputs))
    else:
        for i in nets[0].neurons:
            for l in i:
                for k in l.synapses:
                    print(k.weight)
