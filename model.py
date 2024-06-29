import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import tensorflow as tf
from tensorflow.keras.losses import BinaryCrossentropy
from tensorflow.keras.layers import Dense,Input
from tensorflow.keras import Sequential
from tensorflow.keras.activations import relu,sigmoid
from tensorflow.keras.optimizers import Adam

data = pd.read_csv("TARP.csv")

soil_moisture = data["Soil Moisture"]
temp = data["Temperature"]
soil_humidity = data[" Soil Humidity"]
status = data["Status"]
x = [[soil_moisture[i], temp[i], soil_humidity[i]] for i in range(len(soil_moisture))]
X = np.array(x)
y=[]
for i in range(len(status)):
    if(status[i] == "ON"):
        y.append(1)
    else:
        y.append(0)
y = np.array(y)
X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_norm = scaler.fit_transform(X_train)
X_test = scaler.fit_transform(X_test)
model = Sequential()
model.add(Dense(units = 100,activation = "relu"))
model.add(Dense(units = 50,activation ="relu"))
model.add(Dense(units =1,activation ="sigmoid"))
model.compile(loss = BinaryCrossentropy(), optimizer = Adam())
model.fit(X_norm,y_train,epochs = 100)
y_hat = model.predict(X_test)
y_pred_discrete = (y_hat > 0.5).astype(int)
model.save('my_model.h5')  # Save the model
accuracy = accuracy_score(y_test, y_pred_discrete)
print(accuracy)
