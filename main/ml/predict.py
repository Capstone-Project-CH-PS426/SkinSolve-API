# import numpy as np
# import pandas as pd
# import tensorflow as tf
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_similarity
import pickle 


# Load model
# Load list foods (all foods) model
with open('list_products.pkl', 'rb') as f:
    df = pickle.load(f)
# Load similarity results model
with open('similarity_products.pkl', 'rb') as f:
    similarity = pickle.load(f)

def recommend(user_skin_type, similarity_matrix, top=10):
    try:
        # Find the index of the product with the specified skintype
        index = df[df['skintype'] == user_skin_type].index[0]
    except IndexError:
        print(f"No data available for the specified skin type: {user_skin_type}")
        return

    distances = sorted(enumerate(similarity_matrix[index]), reverse=True, key=lambda x: x[1])

    print(f"Top {top} Recommendations for {user_skin_type} skin type:")
    for i in distances[1:top+1]:
        print(f"{df.iloc[i[0]]['name']} ({df.iloc[i[0]]['benefit']})")

# Example Usage:
user_input_skin_type = input("Enter your skin type (e.g., Normal, Dry, Oily, Combination, Sensitive): ")
recommend(user_input_skin_type, similarity, top=10)


