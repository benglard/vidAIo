import subprocess

def classify():
    cmd = 'th app/lib/cv/classify.lua; exit 0'
    print cmd
    classify_labels = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT).split('\n')
    
    labels = []
    for label in classify_labels:
        if label:
            label = label.replace('\x1b[0m', '')
            label = label.replace('\t', '')
            if label:
                labels.append(label)
    
    return set(labels)
