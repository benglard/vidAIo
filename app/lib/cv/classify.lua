require 'torch'
require 'image'
require 'imgraph'
require 'nn'
require 'paths'

function inTable(t, elem)
    for i = 1, #t do
        if t[i] == elem then return true end
    end
    return false
end

classes = {'airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 'truck'}
model = torch.load('app/lib/cv/data2/cifar23.net')

-- use opencv to loop through video
-- always name: frame.jpg
-- segment, extract segments around 32x32
-- classify each

img = image.load('app/lib/cv/frame.jpg')
graph = imgraph.graph(img)
segm = imgraph.segmentmst(graph)
components = imgraph.extractcomponents(segm, img, 'bbox', 32)

labels = {}
for i, p in pairs(components.patch) do
    w = p:size()[2]
    h = p:size()[3]

    if w < 40 and w > 20 and h < 40 and h > 20 then 
        segment = image.scale(p, 32, 32)
        prob, idx = model:forward(segment):max(1)
        prob = prob:squeeze()
        idx = idx:squeeze()
        output = classes[idx]
        if not inTable(labels, classes[idx]) then
            table.insert(labels, output)
        end
    end
end

for i = 1, #labels do print(labels[i]) end --print to stdout, collect by python subprocess