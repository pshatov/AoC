with open('input.txt') as f:
    img_data = f.readline().strip()

img_w = 25
img_h = 6

layer_num_pixels = img_w * img_h
img_num_layers = len(img_data) // layer_num_pixels

print("img_num_layers = %d" % img_num_layers)

layer_data = []
for i in range(img_num_layers):
    a, b = layer_num_pixels*i, layer_num_pixels*(i+1)
    layer_data.append(img_data[a:b])

def _layer_count_digits(data, digit):
    result = 0
    for i in range(len(data)):
        if data[i] == digit: result += 1
    return result

def layer_count_zeros(data):
    return _layer_count_digits(data, "0")

def layer_count_ones(data):
    return _layer_count_digits(data, "1")

def layer_count_twos(data):
    return _layer_count_digits(data, "2")

min_zeros_index, min_zeros_count = -1, 0
for i in range(len(layer_data)):
    zeros_count = layer_count_zeros(layer_data[i])
    if min_zeros_index == -1:              min_zeros_index, min_zeros_count = i, zeros_count
    elif zeros_count < min_zeros_count: min_zeros_index, min_zeros_count = i, zeros_count
    
print("min_zeros_index = %d" % min_zeros_index)
print("min_zeros_count = %d" % min_zeros_count)
    
ones_count = layer_count_ones(layer_data[min_zeros_index])
twos_count = layer_count_twos(layer_data[min_zeros_index])

print("ones_count * twos_count = %d * %d = %d" % (ones_count, twos_count, ones_count * twos_count))
