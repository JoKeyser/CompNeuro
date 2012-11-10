# feedforward neural network trained with backpropagation
# input(2) -> hidden(2) -> output(1)
# trained on the XOR problem
# Paul Gribble, November 2012
# paul [at] gribblelab [dot] org

# ipython --pylab

##########################
# some utility functions #
##########################

import time
#random.seed(int(time.time()))
random.seed(100)


# sigmoid activation function
def tansig(x):
	return tanh(x)

# derivative of sigmoid function
# (needed for calculating error gradients using backprop)
def dtansig(x):
	# in case x is a vector, multiply() will do element-wise multiplication
	return 1.0 - (multiply(x,x))

# a function that will compute activations of a layer
def layer_forward(act, wgt):
	return tansig( act * wgt )

# a function to compute errors for a layer
def layer_errors(deltas, wgt):
	return deltas * transpose(wgt)

# a function that will compute error gradients for a layer
def layer_deltas(err, act):
	return multiply(dtansig(act), err) # element-wise multiply

# a function to update weights
# N is learning rate parameter and M is momentum parameter
def layer_update_weights(wgt, deltas, act, wgt_prev_change):
	return transpose(act)*deltas



##########################
#     the good stuff     #
##########################

# load up some training examples
#    we will try to get our nnet to learn
#    the XOR mapping
#    http://en.wikipedia.org/wiki/XOR_gate

# numpy matrix of input examples
# 4 training examples, each with 2 inputs
xor_in = matrix([	[0.0, 0.0],
					[0.0, 1.0],
					[1.0, 0.0],
					[1.0, 1.0]	])

# numpy matrix of corresponding outputs
# 4 training examples, each with 1 output
xor_out = matrix([	[0.0],
					[1.0],
					[1.0],
					[0.0]	])

# initialize our nnet : input(2+bias) -> hidden(2+bias) -> output(1)
# initialize network weights to small random values
wgt_hid = rand(2,2)*0.4 - 0.2		# [inp1,inp2]       x-> [hid1,hid2]
wgt_out = rand(2,1)*0.4 - 0.2		# [hid1,hid2      ] x-> [out1]
wgt_out_prev_change = zeros(shape(wgt_out)) # for first epoch
wgt_hid_prev_change = zeros(shape(wgt_hid)) # for first epoch
maxepochs = 1000
errors = zeros((maxepochs,1))
N = 0.05 # learning rate parameter
M = 0.10 # momentum parameter

# we are going to plot the network's performance over the course of learning
# inputs will be a regular grid of [inp1,inp2] points
n_grid = 20
g_grid = linspace(-1.0, 2.0, n_grid)
g1,g2 = meshgrid(g_grid, g_grid)
figure()

for i in range(maxepochs):            						# iterate over epochs
	net_out = zeros(shape(xor_out))
	for j in range(shape(xor_in)[0]): 						# iterate over training examples
		# forward pass
		act_inp = xor_in[j,:]					   # select the first training example
		act_hid = layer_forward(act_inp, wgt_hid)  # hidden unit activations
		act_out = layer_forward(act_hid, wgt_out)  # output unit activations
		net_out[j,:] = act_out[0,:]

		# compute error gradients for each layer,
		# starting from the output layer and working backwards
		err_out = xor_out[j,:] - act_out 
		deltas_out = layer_deltas(err_out, act_out)
		err_hid = layer_errors(deltas_out, wgt_out)
		deltas_hid = layer_deltas(err_hid, act_hid)

		# update the weights !
		# output weights
		wgt_out_change = layer_update_weights(wgt_out, deltas_out, act_hid, wgt_out_prev_change)
		wgt_out = wgt_out + (N * wgt_out_change) + (M * wgt_out_prev_change)
		wgt_out_prev_change = wgt_out_change
		# hidden weights
		wgt_hid_change = layer_update_weights(wgt_hid, deltas_hid, act_inp, wgt_hid_prev_change)
		wgt_hid = wgt_hid + (N * wgt_hid_change) + (M * wgt_hid_prev_change)
		wgt_hid_prev_change = wgt_hid_change

	# compute errors across all targets
	errors[i] = 0.5*sum(square(net_out - xor_out))
	if ((i % 1)==0):
		print "*** EPOCH %4d/%4d : SSE = %6.5f" % (i,maxepochs,errors[i])
		print net_out
		# now do our plotting
		net_perf = zeros(shape(g1))
		for i1 in range(n_grid):
			for i2 in range(n_grid):
				act_inp = matrix([g1[i1,i2],g2[i1,i2]])
				act_hid = layer_forward(act_inp, wgt_hid)
				o_grid = layer_forward(act_hid, wgt_out)
				o_grid = int(o_grid >= 0.50) # hardlim
				net_perf[i1,i2] = o_grid
		cla()
		imshow(net_perf, extent=[-1,2,-1,2])
		plot((0,0,1,1),(0,1,0,1),'ws',markersize=10)
		axis([-1, 2, -1, 2])
		draw()

figure()
subplot(2,1,1)
plot(errors)
subplot(2,1,2)
plot(log(errors))













