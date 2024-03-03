import pandas as pd
import numpy as np

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline

from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
from keras.layers.core import Dropout
from keras import callbacks


class Neural:
    def __init__(self, file):
        self.names = None
        self.scaler1 = None
        self.scaler2 = None
        self.grid = None
        self.y_test = None
        self.y_train = None
        self.x_test = None
        self.x_train = None
        self.data = None
        self.model = None
        self.file = file

    def set_file(self, file):
        self.file = file

    def calculateNeural(self):
        data = pd.read_csv(self.file)
        y = data['class']
        x = data.drop(['rerun_ID', 'obj_ID', 'run_ID', 'cam_col', 'field_ID', 'class', 'fiber_ID'], axis=1)
        self.names = x.columns
        self.scaler1 = MinMaxScaler()
        norm_x = pd.DataFrame(self.scaler1.fit_transform(x), columns=self.names)
        x_train, x_test, y_train, y_test = train_test_split(norm_x, y, stratify=y, test_size=0.3,
                                                            random_state=1111)

        y_train = y_train.map({"GALAXY": 0, "STAR": 1, "QSO": 2})
        y_test = y_test.map({"GALAXY": 0, "STAR": 1, "QSO": 2})
        y_trainOHE = to_categorical(y_train, num_classes=3, dtype='int')
        y_testOHE = to_categorical(y_test, num_classes=3, dtype='int')

        self.model = Sequential()

        self.model.add(Dense(11, input_dim=11, activation='relu'))
        self.model.add(Dropout(0.20))
        self.model.add(Dense(3, input_dim=11, activation='softmax'))

        self.model.compile(optimizer=Adam(learning_rate=0.001), loss='categorical_crossentropy', metrics=['accuracy'])

        earlystopping = callbacks.EarlyStopping(monitor="val_accuracy",
                                                mode="max", patience=3,
                                                restore_best_weights=True)
        self.model.fit(x_train, y_trainOHE,
                       epochs=100,
                       validation_data=(x_test, y_testOHE),
                       callbacks=[earlystopping])

    def calculateKNN(self):
        data = pd.read_csv(self.file)
        y = data['class']
        x = data.drop(['rerun_ID', 'obj_ID', 'run_ID', 'cam_col', 'field_ID', 'class', 'fiber_ID'], axis=1)
        self.scaler2 = MinMaxScaler()
        x_train, x_test, y_train, y_test = train_test_split(x, y, stratify=y, test_size=0.3, random_state=1234)
        knn = KNeighborsClassifier(n_neighbors=3)
        estimator = Pipeline([('scale', self.scaler2), ('knn', knn)])
        hyperparam_space = {
            'knn__n_neighbors': [1, 2, 3, 4, 5],
            'knn__weights': ['uniform', 'distance']
        }

        self.grid = GridSearchCV(
            estimator,
            param_grid=hyperparam_space,
            cv=StratifiedKFold(n_splits=5),
            scoring='accuracy',
            n_jobs=-1)
        self.grid.fit(x_train, y_train)
        self.grid.best_estimator_.fit(x_train, y_train)

    def classificateNeural(self, newdata):
        dictionary = {0: "GALAXY", 1: "STAR", 2: "QSO"}
        tab = pd.DataFrame(data=newdata)
        norm_x = pd.DataFrame(self.scaler1.transform(tab), columns=self.names)
        pred = dictionary[np.argmax(self.model.predict(norm_x.iloc[0:1]))]
        return pred

    def classificateKNN(self, newdata):
        tab = pd.DataFrame(data=newdata)
        pred = self.grid.best_estimator_.predict(tab)
        return pred[0]
