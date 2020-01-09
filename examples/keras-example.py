from FeatureSelection import FeatureSelection

from preprocessing.Normalize import Normalize
import helper.SeriesHelper as series_helper
n = Normalize()
normal_matrix = n.get_normalized_data()
del Normalize
del n
f = FeatureSelection()

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from keras.wrappers.scikit_learn import KerasClassifier
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# larger model
def create_larger():
	# create model
	model = Sequential()
	model.add(Dense(22215, input_dim=22215, activation='relu'))
	model.add(Dense(1000, activation='relu'))
	model.add(Dense(1, activation='sigmoid'))
	# Compile model
	model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model
estimators = []
estimators.append(('standardize', StandardScaler()))
estimators.append(('mlp', KerasClassifier(build_fn=create_larger, epochs=100, batch_size=5, verbose=0)))
pipeline = Pipeline(estimators)
kfold = StratifiedKFold(n_splits=10, shuffle=True)
X,Y = normal_matrix.to_numpy(),series_helper.get_relapse_value_from_series_matrix(normal_matrix)
results = cross_val_score(pipeline, X, Y, cv=kfold)
print("Larger: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))
# f.rfe(model,normal_matrix.to_numpy(),series_helper.get_relapse_value_from_series_matrix(normal_matrix),1000)
