# imports
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from data import get_data, clean_data
from encoders import TimeFeaturesEncoder
from encoders import DistanceTransformer
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from utils import compute_rmse

class Trainer():
    def __init__(self, X, y):
        """
            X: pandas DataFrame
            y: pandas Series
        """
        self.pipeline = None
        self.X = X
        self.y = y

    def set_pipeline(self):
        """defines the pipeline as a class attribute"""
        dist_pipe = Pipeline([('dist_trans', DistanceTransformer()),
                              ('stdscaler', StandardScaler())])

        time_pipe = Pipeline([('time_enc', TimeFeaturesEncoder('pickup_datetime')),
                          ('ohe', OneHotEncoder(handle_unknown='ignore'))])
        preproc_pipe = ColumnTransformer([('distance', dist_pipe, [
            "pickup_latitude", "pickup_longitude", 'dropoff_latitude',
            'dropoff_longitude'
        ]), ('time', time_pipe, ['pickup_datetime'])],
                                     remainder="drop")
        self.pipeline = Pipeline([('preproc', preproc_pipe),
                     ('linear_model', LinearRegression())])
        return self.pipeline

    def run(self):
        """set and train the pipeline"""
        self.set_pipeline()
        self.pipeline.fit(X_train, y_train)
        return self.pipeline

    def evaluate(self, X_test, y_test):
        """evaluates the pipeline on df_test and return the RMSE"""
        y_pred = self.pipeline.predict(X_test)
        rmse = compute_rmse(y_pred, y_test)
        return rmse


if __name__ == "__main__":
    data = get_data()
    #print(data)

    cleaned_data = clean_data(data)
    #print(cleaned_data)

    y = cleaned_data["fare_amount"]
    #print(y)
    X = cleaned_data.drop("fare_amount", axis=1)
    #print(X)

    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.15)
    train = Trainer(X_train, y_train)

    train.run()

    eval = train.evaluate(X_val, y_val)
    print(eval)
