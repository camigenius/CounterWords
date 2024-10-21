import streamlit as st
import pandas as pd
import re
import matplotlib.pyplot as plt
import spacy
from collections import Counter
from io import StringIO


st.title("Word Counter SENA  🧮")


# df = pd.read_excel("EspaciosParticipacion.xlsx",sheet_name="comentarios")

#print("Hola Mundo")

df = pd.read_excel("EspaciosParticipacion.xlsx",sheet_name="comentarios")

df = df.rename(columns={'¿Qué otros temas o actividades le gustaría que se desarrollaran en próximos espacios?\n': 'Sugerencias'})

df['Sugerencias'] = df['Sugerencias'].str.lower().apply(lambda x: re.sub(r'\W+', ' ', str(x)))




option = st.selectbox(
    "Elija una Regional",
    df['Regional'].unique(),
)

st.write("Ha seleccionado la Regional:", option)

df = df[df['Regional']== option]

st.dataframe(df.head(5))


# numeroregionales = len(options)


def extractwords(df):
  all_suggestions = ' '.join(df['Sugerencias'].dropna())
  words = all_suggestions.split()
  word_freq = Counter(words)
  nlp = spacy.blank("es")
  stop_words = nlp.Defaults.stop_words
  doc =nlp(all_suggestions)
  l = [token.text for token in doc if not token.is_stop and not token.is_punct]
  word_freq = Counter(l)
  word_freq_df = pd.DataFrame(word_freq.items(), columns=['Palabra', 'Frecuencia']).sort_values(by='Frecuencia', ascending=False)

  return word_freq_df


dfcountwords = extractwords(df)

st.dataframe(dfcountwords)


def ChartWordFrequency(df,topN,NombreRegional,NumPalabrasDestacadas):


  topN = topN  # Número de palabras a Visualizar
  df = df[df['Palabra'].str.strip() != '']
  df = df.head(topN)

# Resaltar las 5 palabras más frecuentes
  colors = ['green' if i < NumPalabrasDestacadas else 'grey' for i in range(len(df))]
  #regional = df.columns[2]
  # Gráfica de barras


  plt.figure(figsize=(10, 6))
  plt.barh(df['Palabra'], df['Frecuencia'], color=colors)
  plt.xlabel('Frecuencia')
  plt.ylabel('Palabras')
  plt.title('Palabras más frecuentes en las sugerencias' + " "+ NombreRegional)
  plt.gca().invert_yaxis()  # Invertir el eje y para que la palabra más frecuente aparezca en la parte superior
  # plt.show()
  st.pyplot(plt)  


NumPalabrasDestacadas = st.slider('Cantidad Palabras destacadas:', 1,20, 5)
topN = st.slider('Selecciona el número de palabras a mostrar:', 1, len(df), 20)



ChartWordFrequency(dfcountwords,topN,option,NumPalabrasDestacadas)









