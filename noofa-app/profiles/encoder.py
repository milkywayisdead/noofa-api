import numpy

noofa_encoder = {
    numpy.int64: lambda x: x.item(),
}