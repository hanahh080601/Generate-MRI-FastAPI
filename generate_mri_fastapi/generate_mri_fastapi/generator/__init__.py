from generator.generator import GeneratorModel
import torch

stargan_both_generator = GeneratorModel(model='stargan', mode='both')
resunet_both_generator = GeneratorModel(model='resunet', mode='both')
stargan_single_generator = GeneratorModel(model='stargan', mode='single')
resunet_single_generator = GeneratorModel(model='resunet', mode='single')

