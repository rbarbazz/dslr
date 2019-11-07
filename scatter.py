import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    colors = {
        'Gryffindor': '#7f0909',
        'Ravenclaw': '#0e1a40',
        'Slytherin': '#1a472a',
        'Hufflepuff': '#ecb939',
    }
    df = pd.read_csv('dataset_train.csv')
    df.plot.scatter(x='Astronomy', y='Defense Against the Dark Arts', c=df['Hogwarts House'].apply(lambda x: colors[x]))
    plt.show()
