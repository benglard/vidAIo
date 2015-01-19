require 'torch'
require 'nn'
require 'optim'
require 'image'

torch.manualSeed(1)
torch.setnumthreads(2)

classes = {'airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'}

model = nn.Sequential()
-- stage 1 : mean+std normalization -> filter bank -> squashing -> max pooling
model:add(nn.SpatialConvolutionMap(nn.tables.random(3,16,1), 5, 5))
model:add(nn.Tanh())
model:add(nn.SpatialMaxPooling(2, 2, 2, 2))
-- stage 2 : filter bank -> squashing -> max pooling
model:add(nn.SpatialConvolutionMap(nn.tables.random(16, 256, 4), 5, 5))
model:add(nn.Tanh())
model:add(nn.SpatialMaxPooling(2, 2, 2, 2))
-- stage 3 : standard 2-layer neural network
model:add(nn.Reshape(256*5*5))
model:add(nn.Linear(256*5*5, 128))
model:add(nn.Tanh())
model:add(nn.Linear(128,#classes))

parameters, gradParameters = model:getParameters()

print(model)

model:add(nn.LogSoftMax())
criterion = nn.ClassNLLCriterion()

trsize = 10000
tesize = 1000

trainData = {
   data = torch.Tensor(50000, 3072),
   labels = torch.Tensor(50000),
   size = function() return trsize end
}
for i = 0,4 do
   batch = torch.load('cifar-10-batches-t7/data_batch_' .. (i + 1) .. '.t7', 'ascii')
   trainData.data[{ {i * 10000 + 1, (i + 1) * 10000} }] = batch.data:t()
   trainData.labels[{ {i * 10000 + 1, (i + 1) * 10000} }] = batch.labels
end
trainData.labels = trainData.labels + 1

test = torch.load('cifar-10-batches-t7/test_batch.t7', 'ascii')
testData = {
   data = test.data:t():double(),
   labels = test.labels[1]:double(),
   size = function() return tesize end
}
testData.labels = testData.labels + 1

-- reshape data
trainData.data = trainData.data[{ {1,trsize} }]
trainData.labels = trainData.labels[{ {1,trsize} }]
testData.data = testData.data[{ {1,tesize} }]
testData.labels = testData.labels[{ {1,tesize} }]
trainData.data = trainData.data:reshape(trsize, 3, 32, 32)
testData.data = testData.data:reshape(tesize, 3, 32, 32)

print '<trainer> preprocessing data (color space + normalization)'

-- preprocess trainSet
normalization = nn.SpatialContrastiveNormalization(1, image.gaussian1D(7))
for i = 1, trainData:size() do
   -- rgb -> yuv
   local rgb = trainData.data[i]
   local yuv = image.rgb2yuv(rgb)
   -- normalize y locally:
   yuv[1] = normalization(yuv[{{1}}])
   trainData.data[i] = yuv
end
-- normalize u globally:
mean_u = trainData.data[{ {},2,{},{} }]:mean()
std_u = trainData.data[{ {},2,{},{} }]:std()
trainData.data[{ {},2,{},{} }]:add(-mean_u)
trainData.data[{ {},2,{},{} }]:div(-std_u)
-- normalize v globally:
mean_v = trainData.data[{ {},3,{},{} }]:mean()
std_v = trainData.data[{ {},3,{},{} }]:std()
trainData.data[{ {},3,{},{} }]:add(-mean_v)
trainData.data[{ {},3,{},{} }]:div(-std_v)

-- preprocess testSet
for i = 1,testData:size() do
   -- rgb -> yuv
   local rgb = testData.data[i]
   local yuv = image.rgb2yuv(rgb)
   -- normalize y locally:
   yuv[{1}] = normalization(yuv[{{1}}])
   testData.data[i] = yuv
end
-- normalize u globally:
testData.data[{ {},2,{},{} }]:add(-mean_u)
testData.data[{ {},2,{},{} }]:div(-std_u)
-- normalize v globally:
testData.data[{ {},3,{},{} }]:add(-mean_v)
testData.data[{ {},3,{},{} }]:div(-std_v)

confusion = optim.ConfusionMatrix(classes)

trainLogger = optim.Logger(paths.concat('data3', 'train.log'))
testLogger = optim.Logger(paths.concat('data3', 'test.log'))

config = {
    learningRate = 1e-3,
    learningRateDecay = 5e-7,
    momentum = 0.1
}

function train(data)
    epoch = epoch or 1
    local time = sys.clock()
    print('<trainer> on training set:')
    print("<trainer> online epoch # " .. epoch .. ' [batchSize = ' .. 1 .. ']') 

    for t = 1, data:size() do
        xlua.progress(t, data:size())
        local input = data.data[t]
        local label = data.labels[t]

        -- create closure to evaluate f(X) and df/dX
        local feval = function(x)
            if x ~= parameters then parameters:copy(x) end

            gradParameters:zero() -- zero out gradients
            local output = model:forward(input) -- forward pass
            local err = criterion:forward(output, label) -- calc loss
            local df_do = criterion:backward(output, label) -- calc grad
            model:backward(input, df_do) -- backward pass
            confusion:add(output, label)
            return f, gradParameters
        end

        optim.sgd(feval, parameters, config)
    end

    time = sys.clock() - time
    time = time / data:size()
    print("<trainer> time to learn 1 sample = " .. (time*1000) .. 'ms')

    -- print confusion matrix
    print(confusion)
    trainLogger:add{['% mean class accuracy (train set)'] = confusion.totalValid * 100}
    confusion:zero()

    local filename = paths.concat('data3', 'cifar' .. tostring(epoch) .. '.net')
    print('<trainer> saving network to ' .. filename)
    torch.save(filename, model)

    -- next epoch
    epoch = epoch + 1
end

function test(data)
    local time = sys.clock()
    print('<trainer> on testing Set:')
   for t = 1, data:size() do
      xlua.progress(t, data:size())
      local input = data.data[t]
      local target = data.labels[t]

      local pred = model:forward(input)
      confusion:add(pred, target)
   end

   -- timing
   time = sys.clock() - time
   time = time / data:size()
   print("<trainer> time to test 1 sample = " .. (time*1000) .. 'ms')

   -- print confusion matrix
   print(confusion)
   testLogger:add{['% mean class accuracy (test set)'] = confusion.totalValid * 100}
   confusion:zero()
end

while true do
    train(trainData)
    test(testData)

    trainLogger:style{['% mean class accuracy (train set)'] = '-'}
    testLogger:style{['% mean class accuracy (test set)'] = '-'}
end
