import random

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
            outputs.append(i.value)
        return outputs
    def mutate(self,num_of_synapses_changed,amount_of_mutation):
        for loops in range(num_of_synapses_changed):
            synapapse_to_change = random.randint(0,self.num_synapses)
            synapses_found = 0
            for i in self.neurons:
                for l in i:
                    for q in l.synapses:
                        if synapses_found == synapapse_to_change:
                            amount = random.uniform(-amount_of_mutation,amount_of_mutation)
                            while q.weight + amount < 0  or q.weight + amount > 1:
                                amount = random.uniform(-amount_of_mutation,amount_of_mutation)
                            q.weight += amount
                        synapses_found += 1

def sort(training_output,outputs):
    for i in outputs:
        i.append(abs(i[0][0]-training_output))
    sorted = []
    for i in outputs:
        if len(sorted)==0:
            sorted.append(i)
        elif i[2] >= sorted[0][2]:
            sorted.insert(0,i)
        elif not i[2] < sorted[len(sorted)-1][2]:
            for k in sorted:
                if i[2] >= k[2]:
                    sorted.insert(sorted.index(k),i)
                    break
        else:
            sorted.append(i)
    return sorted

nets = []
for i in range(1000):
    nets.append(Net(2,0,3,1))
for loop in range(200):
    training_inputs = [0]
    for l in range(2):
        training_inputs.append(random.randint(0,1))

    outputs = []
    for i in nets:
        outputs.append([i.get_output(training_inputs),i])

    outputs = sort(training_inputs[0],outputs)
    #for i in outputs:
    #    print(i[0])
    #print(training_inputs[0],outputs[len(outputs)-1][0])
    #for i in outputs[len(outputs)-1][1].neurons:
    #    for l in i:
    #        for q in l.synapses:
    #            print(q.weight)
    #print('')
    half = int(len(nets)/2)
    for i in range(half):
        #nets[nets.index(outputs[i][1])] = Net(2,0,3,1)
        nets[nets.index(outputs[i][1])] = nets[nets.index(outputs[i+half][1])]
    for i in nets:
        i.mutate(2,.1)

while True:
    training_inputs = raw_input('Give new input: ')
    training_inputs = list(training_inputs)
    for i in range(len(training_inputs)):
        training_inputs[i] = int(training_inputs[i])
    print(outputs[len(outputs)-1][1].get_output(training_inputs))
