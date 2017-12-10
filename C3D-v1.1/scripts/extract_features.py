import os
import sys
import numpy as np
import caffe

data_dir = sys.argv[1]
model_path = sys.argv[2]
deploy_prototxt_path = sys.argv[3]
imagemean_path = sys.argv[4]
output_dir = sys.argv[5]
layer = sys.argv[6]

# Create caffe Net object
net = caffe.Net(deploy_prototxt_path, model_path, caffe.TEST)

# Check if layer exists
if layer not in net.blobs:
    raise TypeError("Invalid layer name. Layer doesn't exist in net definition: " + layer)

# Create preprocessor
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_mean('data', np.load(imagemean_path).mean(1).mean(1))
transformer.set_transpose('data', (2,0,1))
transformer.set_raw_scale('data', 255.0)

# Reshape the data blob to accept AlexNet dimensions
net.blobs['data'].reshape(1,3,227,227)

# Preprocess and extract features from all files in a folder data_dir
for folder in os.listdir(data_dir):
    current_output_dir = output_dir + '/' + folder
    print 'In data folder: ' + folder + " , output folder: " + current_output_dir


    if not os.path.exists(current_output_dir):
            os.makedirs(current_output_dir)
    
    for image_file in os.listdir(data_dir + '/' + folder):
        print 'Processing image: ' + image_file
        # Load image
        img = caffe.io.load_image(data_dir + '/' + folder + '/' + image_file)
        
        # Preprocess the image using the transformer
        net.blobs['data'].data[...] = transformer.preprocess('data', img)
        
        # Feed forward the image in the net
        output = net.forward()

        # Save features
        output_file = current_output_dir + '/' + image_file + '_features.txt'

        with open(output_file, 'w') as f:
            np.savetxt(f, net.blobs[layer].data[0], fmt='%.4f', delimiter='\n')

    

        











