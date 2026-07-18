import pickle

# Load the model
with open("recommender_model.pkl", "rb") as f:
    recommender_data = pickle.load(f)

df = recommender_data["df"]
tfidf_vectorizer = recommender_data["tfidf_vectorizer"]
content_matrix = recommender_data["content_matrix"]
content_similarity = recommender_data["content_similarity"]
indices = recommender_data["indices"]
algo = recommender_data["svd_model"]
trainset = recommender_data["trainset"]

# Load functions
def get_content_based_recommendations(title, top_n=5):
    if title not in indices:
        return []
    idx = indices[title]
    similarity_scores = list(enumerate(content_similarity[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
    similarity_scores = similarity_scores[1:top_n + 1]
    recommended_indices = [i[0] for i in similarity_scores]
    return df['Title'].iloc[recommended_indices].tolist()

def get_collaborative_filtering_recommendations(title, top_n=5):
    testset = trainset.build_anti_testset()
    testset = [x for x in testset if x[0] == title]
    predictions = algo.test(testset)
    predictions.sort(key=lambda x: x.est, reverse=True)
    recommended_ids = [pred.iid for pred in predictions[:top_n]]
    recommended_titles = df[df['information'].isin(recommended_ids)]['Title'].tolist()
    return recommended_titles

def get_hybrid_recommendations(title, top_n=5):
    content_based = get_content_based_recommendations(title, top_n)
    collaborative_based = get_collaborative_filtering_recommendations(title, top_n)
    hybrid_recommendations = list(set(content_based + collaborative_based))
    return hybrid_recommendations[:top_n]

# Example Usage
title_to_search = "Sample Video Title 58010e69"
recommendations = get_hybrid_recommendations(title_to_search, top_n=5)
print(recommendations)
