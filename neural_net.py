import random
import copy
import numpy as np

class Synapse:
    def __init__(self,neuron1,neuron2,weight,bias):
        self.weight = weight
        self.neuron1 = neuron1
        self.neuron2 = neuron2
    def get_value(self):
        return (self.neuron1.value)*self.weight

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
        self.outputs = []
        for i in range(rows):
            if i == 0:
                sublist = []
                for l in range(self.num_input_neurons):
                    neuron = Neuron(1)
                    sublist.append(neuron)
                self.neurons.append(sublist)
            elif i == rows-1:
                sublist = []
                for l in range(self.num_output_neurons):
                    neuron = Neuron(3)
                    sublist.append(neuron)
                self.neurons.append(sublist)
            else:
                sublist = []
                for l in range(neuron_per_row):
                    neuron = Neuron(2)
                    sublist.append(neuron)
                self.neurons.append(sublist)

        for i in self.neurons:
            for l in i:
                if not self.neurons.index(i) == self.rows - 1:
                    for q in range(len(self.neurons[self.neurons.index(i)+1])):
                        l.add_synapse(Synapse(l,self.neurons[self.neurons.index(i)+1][q],float(random.randint(0,100))/100,float(random.randint(0,100))/100))
                        self.num_synapses += 1
    def get_output(self,input,correct_output):
        for i in self.neurons:
            for l in i:
                l.values = []
        for i in self.neurons:
            #setting the values of the input neurons to the given input values
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
        self.ouputs.append(self.avg_fitness(outputs,correct_output))
        self.outputs.append(self.list_sigmoid(outputs))
        return self.list_sigmoid(outputs)
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
        output = 1/(1+np.exp(-5*input))*2-1
        return output
    def list_sigmoid(self,inputs):
        outputs = []
        for i in inputs:
            outputs.append(1/(1+np.exp(-5*i))*2-1)
        return outputs
    def avg_fitness(self,output,correct_output):
        fitnesses = []
        for i in range(len(correct_output)):
            fitnesses.append(correct_output[i]-self.sigmoid(output[i]))
        avg = 0
        for i in fitnesses:
            avg += i
        avg = avg/len(fitnesses)
        return avg



nets = []
possible_inputs = []
correct_output = []
def create_net_of_nets(num_nets):
    global nets,possible_inputs,correct_output
    nets = []
    possible_inputs = [
    [1,1,1,1],
    [-1,-1,-1,-1],
    [1,1,1,-1],
    [1,1,-1,-1],
    [1,-1,-1,-1],
    [-1,-1,-1,1],
    [-1,-1,1,1],
    [-1,1,1,1],
    [1,-1,1,-1],
    [-1,1,-1,1]
    ]
    correct_output = [
    [-1,-1,-1,-1],
    [1,1,1,1],
    [-1,-1,-1,1],
    [-1,-1,1,1],
    [-1,1,1,1],
    [1,1,1,-1],
    [1,1,-1,-1],
    [1,-1,-1,-1],
    [-1,1,-1,1],
    [1,-1,1,-1]
    ]

    for i in range(num_nets):
        nets.append(Net(2,1,4,4))

def new_gen():
    global nets,possible_inputs,correct_output
    for i in nets:
        i.ouputs = []
        i.outputs = []
    for i in possible_inputs:
        for l in nets:
            l.get_output(i,correct_output[possible_inputs.index(i)])

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

    for i in range(len(nets)):
        if i+1 == int(half):
            median = nets[i]
        if i+1 > half:
            nets[i] = copy.deepcopy(nets[int(i-half)])
            nets[i].mutate(2,1)
    return [nets[0].outputs,nets[0].get_fitness()]

if __name__ == '__main__':
    create_net_of_nets(100)
    for i in range(100):
        output = new_gen()
        print(output[0][0],output[1])
'''while True:
    inputs = input('Give new input: ')
    if not inputs == 'synapses':
        inputs = int(inputs)/127.5-1
        print(inputs)
        output = (nets[len(nets)-1].get_output([inputs],0))
        print(output)
        output = (output[0]+1)*127.5
        print(output)
    else:
        for i in nets[0].neurons:
            for l in i:
                for k in l.synapses:
                    print(k.weight)
'''
