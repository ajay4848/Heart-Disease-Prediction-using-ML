from flask import Flask, render_template, request, send_file
import io
import base64
import pickle
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


data = pd.DataFrame({'Models': ['LR', 'SVM', 'KNN', 'DT', 'RF', 'GB'], 'ACC': [78.688525, 80.327869, 83.770492, 70.491803, 85.245902, 80.327869]})
acc_array = data.values


warnings.filterwarnings("ignore")

model = pickle.load(
    open('C:\\Users\\ACER\Documents\\flask\\model.pkl', 'rb'))

app = Flask(__name__)



@app.route('/')
def landing():
    return render_template('landing.html',  methods=['GET', 'POST'])


@app.route('/home', methods=['GET', 'POST'])


    
def home():
    r = ' '
    if request.method == 'POST':
        input_text = []
        for i in range(1, 14):
            it = 'input_text' + str(i)
            print("requst : ",it," : ",request.form[it])
            input_text.append(int(request.form[it]))


        my_dataframe = pd.DataFrame({
            'age': input_text[0],
            'sex':  input_text[1],
            'cp':  input_text[2],
            'trestbps':  input_text[3],
            'chol': input_text[4],
            'fbs':  input_text[5],
            'restecg':  input_text[6],
            'thalach':  input_text[7],
            'exang':  input_text[8],
            'oldpeak':  input_text[9],
            'slope':  input_text[10],
            'ca':  input_text[11],
            'thal': input_text[12],
        }, index=[0])

        result = model.predict(my_dataframe)
        
        print("result is : ",result[0])

        print(result)
        if result[0]:
            r = 'You have risk of Heart Disease'
        else:
            r='You do not have risk of Heart Disease'

        fig, ax = plt.subplots()
        sns.barplot(x='Models', y='ACC', data=data, ax=ax)

        # encode plot image in base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()
        graphic = base64.b64encode(image_png)

        # render template with plot image

        return render_template('home.html', output=r, acc = acc_array , graphic=graphic.decode('utf-8'))

    return render_template('home.html')







if __name__ == '__main__':
    app.run()
