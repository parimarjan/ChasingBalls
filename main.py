import random
import time
import numpy as np
import os
import json

from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn import preprocessing

SCALE = 500
# size = 2
colour = (0,0,255)
STEP_SIZE = 0.1
CONVERGE_THRESHOLD = 0.5
MAX_CONVERGE_ITER = 500000

NUM_POINTS = 5    # number of balls in a simulation

NETWORK_SIZE = (200,200,50)
# NETWORK_SIZE = (50,50,50)
TRAIN_SAMPLES = 100000
TEST_SAMPLES = 10000

DIM = 2
ERROR_MARGIN = 3

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
       return v
    return v / norm

class Point():
    def __init__(self, dim=DIM, coord=None):
        self.pos = []
        if coord is None:
            for i in range(dim):
                self.pos.append(SCALE*random.random())
        else:
            for i in range(len(coord)):
                self.pos.append(coord[i])
        
        self.pos = np.array(self.pos)
        self.new_pos = np.copy(self.pos)
        self.following = None

def init(n=4, coords=None):
    '''
    returns n points.
    '''
    points = []
    for i in range(n):
        if coords:
            points.append(Point(coord=coords[i]))
        else:
            points.append(Point())

    # adding the following code.
    for i in range(n):
        idx = (i+1) % n
        points[i].following = points[idx]

    return points

def update(points):
    '''
    '''
    for i, p in enumerate(points):
        # TODO: Normalize this??
        dif = normalize(p.following.pos - p.pos)
        p.new_pos += dif*STEP_SIZE 

    # now that all points positions have been updated, correct pos variable to
    # the new pos.
    for i, p in enumerate(points):
        p.pos = np.copy(p.new_pos)

def total_dist(points):
    cur_dist = 0
    for p in points:
        cur_dist += np.linalg.norm(p.pos - p.following.pos)
    return cur_dist

## TODO: add converging if the distance between the points stop changing.

def run(points):
    if DIM == 1:
        point_pos = [p.pos for p in points]
        return (max(point_pos) + min(point_pos)) / 2
    else:
        # point_posx = [p.pos[0] for p in points]
        # point_posy = [p.pos[1] for p in points]
        # x = (max(point_posx) + min(point_posy)) / 2
        # y = (max(point_posx) + min(point_posy)) / 2
        # return np.array([x,y])

        i = 0
        while True:
            tdist = total_dist(points)
            if (tdist <= CONVERGE_THRESHOLD):
                break
            update(points)
            i += 1
            if i % 1000 == 0:
                print(i)
            if i > MAX_CONVERGE_ITER:
                break
        # TODO: return central point
        return points[0].pos
    

def extract_feature_naive(points):
    '''
    Feature list:
        1. p.x
        2. p.y
    '''
    # TODO: arrange feature order BETTER.
    features = []
    for p in points:
        for i, coord in enumerate(p.pos):
            features.append(p.pos[i])
            # features.append(p.following.pos[i])
            # features.append(abs(p.pos[i] + p.following.pos[i]))
    
    if DIM == 1:
        point_pos = [p.pos for p in points]
        features.append(max(point_pos))
        features.append(min(point_pos))
    elif DIM == 2:
        point_posx = [p.pos[0] for p in points]
        point_posy = [p.pos[1] for p in points]
        features.append(max(point_posx))
        features.append(min(point_posx))
        features.append(max(point_posy))
        features.append(min(point_posy))
        features.append(np.mean(np.array(point_posx)))
        features.append(np.mean(np.array(point_posy)))

    for i, f in enumerate(features):
        features[i] = float(f)
    # Other features we can add: total distance between the points etc. etc.
    return features

def gen_data(num_samples, num_points):
    all_features = []
    all_Y = []
    for i in range(num_samples):
        print('generating point ', i)
        points = init(n=num_points)
        sample_features = extract_feature_naive(points)
        all_features.append(sample_features)

        # generate initial features
        sample_result = run(points)
        if DIM == 1:
            all_Y.append(float(sample_result[0]))
        elif DIM == 2:
            all_Y.append(sample_result[0] + sample_result[1])

    return all_features, all_Y
    # return np.array(all_features), np.array(all_Y)
    # return preprocessing.scale(all_features), preprocessing.scale(all_Y)
    # NOT scale Y
    # return preprocessing.scale(all_features), all_Y


def train_network(train_features, train_labels):
    '''
    simple, naive version.
    '''
    # clf = SVR(C=1000, epsilon=0.0001)
    clf = MLPRegressor(hidden_layer_sizes=(NETWORK_SIZE), max_iter=2000000)
    print('.... starting training ....')
    clf.fit(train_features, train_labels) 
    return clf

def test_network(clf, X):
    print('... starting to test ... ')
    Y = clf.predict(X)
    return Y

if __name__ == "__main__":
    if os.path.isfile('train_features.json'):
        with open('train_features.json', 'r') as outfile:
            train_features = json.load(outfile)
        with open('train_labels.json', 'r') as outfile:
            train_labels = json.load(outfile)
        with open('test_features.json', 'r') as outfile:
            test_features = json.load(outfile)
        with open('test_labels.json', 'r') as outfile:
            test_labels = json.load(outfile)
        print('loaded training data!')
    else:
        train_features, train_labels = gen_data(TRAIN_SAMPLES, NUM_POINTS)
        print('training done!')
        # save train data to json

        with open('train_features.json', 'w') as outfile:
            json.dump(train_features, outfile)
        with open('train_labels.json', 'w') as outfile:
            json.dump(train_labels, outfile)
    
    
        test_features, test_labels = gen_data(TEST_SAMPLES, NUM_POINTS)
        with open('test_features.json', 'w') as outfile:
            json.dump(test_features, outfile)
        with open('test_labels.json', 'w') as outfile:
            json.dump(test_labels, outfile)

    clf = train_network(train_features, train_labels)
    Y_preds = test_network(clf, test_features)

    mistakes = 0
    for i, y in enumerate(Y_preds):
        print(Y_preds[i])
        if abs(Y_preds[i] - test_labels[i]) > ERROR_MARGIN:
            mistakes += 1

    print('% mistakes: ', mistakes/float(len(Y_preds)))
