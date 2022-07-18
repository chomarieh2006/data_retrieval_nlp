import torch

class my_dataset(torch.utils.data.Dataset):
    def __init__(self, start, end):
        self.X = list(range(start, end))

        def my_function(x):
            y = 2 * x * x * x + 3 * x * x - 4 * x + 5
            return y

        self.label = []
        for i, x in enumerate(self.X):
            self.label.append(my_function(x))

    def __len__(self):
        return len(self.label)

    def __getitem__(self, index):
        x = self.X[index]
        y = self.label[index]

        return x, y


dtype = torch.float
device = torch.device("cpu")

a = torch.tensor(1.0, dtype = dtype, device = device, requires_grad = True)
b = torch.tensor(1.0, dtype = dtype, device = device, requires_grad = True)
c = torch.tensor(1.0, dtype = dtype, device = device, requires_grad = True)
d = torch.tensor(1.0, dtype = dtype, device = device, requires_grad = True)

params = {'batch_size': 1,
          'shuffle': True,
          'num_workers': 6}

training_set = my_dataset(-10, 11)
training_generator = torch.utils.data.DataLoader(training_set, batch_size = 1)


lr = 0.0001

for epoch in range(0, 100):
    for x, y_ in training_generator:

        y = a*x*x*x + b*x*x + c*x + d
        err = torch.sqrt((y - y_)*(y - y_))
        err.backward()

        print(err)

        with torch.no_grad():
            a.data = a - lr*a.grad
            b.data = b - lr*b.grad
            c.data = c - lr*c.grad
            d.data = d-  lr*d.grad

            a.grad = None
            b.grad = None
            c.grad = None
            d.grad = None


print (a, b, c, d)
