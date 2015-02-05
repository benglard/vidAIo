# vidAIo

vidAIo is video search engine made by combining natural language processing/computer vision to analyze the audio/frames.

I wanted to combine as many AI technologies as I could think of. Videos offer a powerful opportunity as they offer up both audio, which can be transcribed to text, and analyzed and indexed by natural language processing (NLP) algorithms, and frames, which often contain a myriad of objects, and can be analyzed and indexed by computer vision (CV) algorithms. On the NLP side, there are algorithms for keyword extraction (graphical model), named entity extraction (nltk chunking), topic modeling (LDA with gensim), and summarization (lexrank). On the CV side, there is a neural network (built on Torch7) trained on the Cifar10 dataset, achieving 57% accuracy (not bad for about an hour of training on a laptop), and a facial recognition system (PCA+SVM, built on scikit-learn). The NLP systems tend to work much better than the CV systems. The data is stored in MongoDB and there's a simple web interface built with Flask.

Note: this is hackathon level code with a lot of dependencies. Enjoy!
