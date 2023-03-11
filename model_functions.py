import numpy as np
from itertools import product
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split


def train_model(params, profits, random_state=42):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(params, profits, test_size=0.2, random_state=random_state)

    # Train a random forest regressor on the training data
    model = RandomForestRegressor(n_estimators=100, random_state=random_state)
    model.fit(X_train, y_train)

    # Evaluate the model on the testing data
    score = model.score(X_test, y_test)
    print("Model score:", score)

    return model


def predict_profit_ranges(model, range_data, means):
    # Use the model to predict the RealizedProfits values for the parameter combinations within the recommended Min/Max ranges
    predicted_profits = []
    for i in range(len(range_data)):
        param_range = range_data[i]
        param_values = []
        for j in range(len(means)):
            if params.columns[j] == param_range['Parameter']:
                param_values.append(np.arange(param_range['Min'], param_range['Max'] + param_range.get('Step', 0.01), param_range.get('Step', 0.01)))
            else:
                param_values.append([means[j]])
        X_new = pd.DataFrame(list(product(*param_values)), columns=params.columns)
        predicted_profit = model.predict(X_new)
        predicted_profits.append(predicted_profit)

    # Calculate the predicted profit ranges
    predicted_min = np.min(np.concatenate(predicted_profits, axis=0), axis=0)
    predicted_max = np.max(np.concatenate(predicted_profits), axis=1)

    return predicted_min, predicted_max
