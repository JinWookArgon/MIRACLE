import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def train_model(Input_file,Ratio):
	data = pd.read_csv(Input_file, delimiter='\t')
	msi_h = data[data['Type'] == 'MSI-H']
	mss = data[data['Type'] == 'MSS']
	train_msi_h = msi_h.sample(frac=Ratio, random_state=54)
	train_mss = mss.sample(n=len(train_msi_h), random_state=54)
	train_data = pd.concat([train_msi_h, train_mss])
	X_train = train_data[['Counts']]
	y_train = train_data['Type']

	forest_clf = RandomForestClassifier(random_state=42, n_estimators=100)
	param_grid = {
			    'max_features': range(1, X_train.shape[1] + 1) if X_train.shape[1] > 1 else [1]
				}

	grid_search = GridSearchCV(forest_clf, param_grid, cv=10, scoring='accuracy', refit=True)
	grid_search.fit(X_train, y_train)

	final_model = grid_search.best_estimator_

	return final_model

def test_new_samples(paras):
	test_file = "Unstable_loci_count_" + paras.output + ".txt"
	new_samples = pd.read_csv(test_file, delimiter='\t')
	X_new_samples = new_samples[['Counts']]
	training_data = paras.Model
	output = paras.output
	Ratio = paras.Random
	model = train_model(training_data,Ratio)
	y_prob_new_samples = model.predict_proba(X_new_samples)
	probabilities_new_samples = pd.DataFrame(y_prob_new_samples, columns=model.classes_)
	probabilities_new_samples['Name'] = new_samples['Case']
	probabilities_new_samples['Counts'] = new_samples['Counts']
	final_output = probabilities_new_samples[['Name', 'Counts', 'MSI-H', 'MSS']]
	filename = f"Final_result_{output}.txt"
	final_output.to_csv(filename,index=False, sep='\t')
	print(f"[step: 3] Calculating the possibility is finished")
