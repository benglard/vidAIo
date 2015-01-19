from sklearn.cross_validation import train_test_split
from sklearn.datasets import fetch_lfw_people
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.decomposition import RandomizedPCA
from sklearn.svm import SVC

class FaceRecognize(object):

    """Use scikit-learn PCA and SVM to build a
    facial recognition system for the labeled faces
    in the wild dataset."""

    def __init__(self):
        lfw_people = fetch_lfw_people(min_faces_per_person=70, resize=0.4)
        n_samples, h, w = lfw_people.images.shape
        X = lfw_people.data

        # the label to predict is the id of the person
        y = lfw_people.target
        self.target_names = lfw_people.target_names

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25)

        n_components = 150
        pca = RandomizedPCA(n_components=n_components, whiten=True).fit(X_train)

        X_train_pca = pca.transform(X_train)
        X_test_pca = pca.transform(X_test)

        param_grid = {'C': [1e3, 5e3, 1e4, 5e4, 1e5], 'gamma': [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.1]}
        clf = GridSearchCV(SVC(kernel='rbf', class_weight='auto'), param_grid)
        clf = clf.fit(X_train_pca, y_train)

        self.pca = pca
        self.clf = clf

    def test(self, frame):
        frame_pca = self.pca.transform(frame)
        prediction = self.clf.predict(frame_pca)
        return self.target_names[prediction[0]]