import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Surprise imports for collaborative filtering
from surprise import SVD, Dataset, Reader

def get_hybrid_recommendations(articles, quizzes, videos, search_title, top_n=5):
    """
    Combines articles, quizzes, and videos data into a single DataFrame,
    computes recommendations using both content-based (TF-IDF & cosine similarity)
    and collaborative filtering (Surprise SVD), and returns a hybrid recommendation
    dictionary where the keys are Titles and the values are their content types.
    
    Parameters:
      articles (list of dict): Each dictionary includes keys like "title", "content", etc.
      quizzes (list of list): Each inner list represents a quiz record.
      videos (list of list): Each inner list represents a video record.
      search_title (str): The title to base the recommendations on.
      top_n (int): Number of recommendations to return (default is 5).
      
    Returns:
      dict: A dictionary where keys are recommended Titles and values are content types.
    """
    
    # -------------------------------
    # 1. Convert each data source into a DataFrame with appropriate column names.
    # -------------------------------
    # Articles: assume keys match (e.g., title, content, tags, author, references)
    df_articles = pd.DataFrame(articles)
    # Quizzes: define column names (adjust if needed)
    quiz_columns = ['ID', 'Title', 'Description', 'Category', 'Level', 'Estimated Time', 
                    'Tags', 'Extra', 'Created At', 'Updated At']
    df_quizzes = pd.DataFrame(quizzes, columns=quiz_columns)
    # Videos: define column names (adjust if needed)
    video_columns = ['ID', 'Title', 'Slug', 'Description', 'Category', 'Tags', 'Video File', 
                     'Thumbnail', 'Views', 'Created At', 'Updated At', 'Rating', 'Extra']
    df_videos = pd.DataFrame(videos, columns=video_columns)
    
    # -------------------------------
    # 2. Add a 'content_type' column to each DataFrame.
    # -------------------------------
    df_articles['content_type'] = 'article'
    df_quizzes['content_type'] = 'quiz'
    df_videos['content_type'] = 'video'
    
    # -------------------------------
    # 3. Create a combined text column ("information") from relevant columns.
    # -------------------------------
    def combine_article(row):
        # For articles, combine title, content, tags, author, and references (titles only)
        tags = ' '.join(row.get('tags', [])) if isinstance(row.get('tags', []), list) else str(row.get('tags', ''))
        references = ' '.join([f"{ref.get('title', '')}" for ref in row.get('references', [])]) if row.get('references') else ""
        return f"{row.get('title', '')} {row.get('content', '')} {tags} {row.get('author', '')} {references}"
    
    def combine_quiz(row):
        # For quizzes, combine Title, Description, Category, Level, and Tags.
        return f"{row.get('Title', '')} {row.get('Description', '')} {row.get('Category', '')} {row.get('Level', '')} {row.get('Tags', '')}"
    
    def combine_video(row):
        # For videos, combine Title, Description, Category, and Tags.
        return f"{row.get('Title', '')} {row.get('Description', '')} {row.get('Category', '')} {row.get('Tags', '')}"
    
    df_articles['information'] = df_articles.apply(combine_article, axis=1)
    df_quizzes['information'] = df_quizzes.apply(combine_quiz, axis=1)
    df_videos['information'] = df_videos.apply(combine_video, axis=1)
    
    # -------------------------------
    # 4. Combine all data into a single DataFrame.
    # -------------------------------
    df_all = pd.concat([df_articles, df_quizzes, df_videos], ignore_index=True)
    df_all['information'] = df_all['information'].astype(str)
    
    # For collaborative filtering, we need a rating column.
    # If the data source does not have ratings, add a dummy rating (e.g., 3).
    if 'rating' not in df_all.columns:
        df_all['rating'] = 3
    else:
        df_all['rating'] = df_all['rating'].fillna(3)
    
    # -------------------------------
    # 5. Build content-based recommendations using TF-IDF and cosine similarity.
    # -------------------------------
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(df_all['information'])
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
    
    # Create a mapping from Title to DataFrame index (assuming titles are unique)
    indices = pd.Series(df_all.index, index=df_all['Title']).drop_duplicates()
    
    def get_content_based_recommendations(title, top_n=top_n):
        if title not in indices:
            return []
        idx = indices[title]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:top_n+1]  # exclude the item itself
        rec_indices = [i[0] for i in sim_scores]
        return df_all.iloc[rec_indices]['Title'].tolist()
    
    # -------------------------------
    # 6. Build collaborative filtering recommendations using Surprise SVD.
    # -------------------------------
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(df_all[['Title', 'information', 'rating']], reader)
    trainset = data.build_full_trainset()
    algo = SVD()
    algo.fit(trainset)
    
    def get_collaborative_filtering_recommendations(title, top_n=top_n):
        """
        Get top_n recommendations for a given Title using collaborative filtering.
        Note: In this demonstration, Title is used as the user identifier.
        """
        testset = trainset.build_anti_testset()
        testset = [x for x in testset if x[0] == title]
        predictions = algo.test(testset)
        predictions.sort(key=lambda x: x.est, reverse=True)
        recommended_ids = [pred.iid for pred in predictions[:top_n]]
        # Mapping back to titles based on unique 'information'
        recommended_titles = df_all[df_all['information'].isin(recommended_ids)]['Title'].tolist()
        return recommended_titles
    
    # -------------------------------
    # 7. Combine both recommendations into a hybrid list.
    # -------------------------------
    content_recs = get_content_based_recommendations(search_title, top_n)
    collab_recs = get_collaborative_filtering_recommendations(search_title, top_n)
    
    # Combine recommendations and remove duplicates
    hybrid_titles = list(set(content_recs + collab_recs))
    hybrid_titles = hybrid_titles[:top_n]
    
    # Build the output dictionary: key = Title, value = content_type
    rec_dict = {}
    for title in hybrid_titles:
        # Find the row in the DataFrame matching this title
        row = df_all[df_all['Title'] == title]
        if not row.empty:
            rec_dict[title] = row.iloc[0]['content_type']
    
    return rec_dict

# # -------------------------------
# # Example Usage:
# # -------------------------------
# if __name__ == "__main__":
#     import datetime
#     import zoneinfo

#     # Sample articles (list of dicts)
#     articles = [
#         {
#             "title": "Understanding Data Structures in Python",
#             "author": "Jane Doe",
#             "published_date": "2025-03-28",
#             "content": "In this article, we explore common data structures in Python, such as lists, tuples, sets, and dictionaries...",
#             "tags": ["Python", "Programming", "Data Structures"],
#             "references": [
#                 {"author": "John Smith", "title": "Python Basics", "year": 2022},
#                 {"author": "Emily Taylor", "title": "Advanced Python", "year": 2024}
#             ]
#         },
#         {
#             "title": "A Beginner's Guide to Machine Learning",
#             "author": "Michael Johnson",
#             "published_date": "2025-02-15",
#             "content": "This article covers the fundamentals of machine learning, from supervised to unsupervised learning, with practical examples...",
#             "tags": ["Machine Learning", "AI", "Data Science"],
#             "references": [
#                 {"author": "Alice Williams", "title": "Introduction to Machine Learning", "year": 2023},
#                 {"author": "Bob Lee", "title": "AI Fundamentals", "year": 2024}
#             ]
#         },
#         {
#             "title": "Web Development in 2025: What to Expect",
#             "author": "Sarah Brown",
#             "published_date": "2025-03-01",
#             "content": "This article discusses emerging trends in web development, including the latest frameworks, tools, and best practices for modern developers...",
#             "tags": ["Web Development", "JavaScript", "Tech Trends"],
#             "references": [
#                 {"author": "David Clark", "title": "The Future of Web Development", "year": 2024},
#                 {"author": "Sophie Green", "title": "Building Scalable Web Apps", "year": 2023}
#             ]
#         }
#     ]
    
#     # Sample quizzes (list of lists)
#     quizzes = [
#         ['6ffdc0a1-3fb4-48dd-baf6-d5b21b8ee9b8', 'Quiz: Web Dev Basics', 'An introductory quiz on web development concepts.', 'Web Development', 'Medium', 29, 'Express, React, Web Development', '', datetime.datetime(2025, 3, 12, 1, 27, 42, 948534, tzinfo=datetime.timezone.utc), datetime.datetime(2025, 3, 12, 1, 27, 42, 948555, tzinfo=datetime.timezone.utc)],
#         ['0f4f3555-3ce5-40f1-8636-e469f1332ae2', 'Quiz: Advanced Web Dev', 'A quiz testing advanced web development skills.', 'Web Development', 'Medium', 23, 'UI Design, TypeScript, JavaScript', '', datetime.datetime(2025, 3, 12, 1, 27, 42, 968915, tzinfo=datetime.timezone.utc), datetime.datetime(2025, 3, 12, 1, 27, 42, 968934, tzinfo=datetime.timezone.utc)]
#     ]
    
#     # Sample videos (list of lists)
#     videos = [
#         ['61dc051b-155a-46c3-a802-04a55adedca0', 'Sample Video Title 7ed1bd3c', 'sample-video-title-7ed1bd3c-e284a209', 'This is a sample description for the video Sample Video Title 7ed1bd3c.', 'UI Design', 'Frontend, MongoDB, React Hooks', '/media/videos/sample1.mp4', '/media/thumbnails/sample1.jpg', 0, datetime.datetime(2025, 3, 11, 22, 46, 30, 31793, tzinfo=zoneinfo.ZoneInfo("UTC")), datetime.datetime(2025, 3, 11, 22, 46, 30, 31820, tzinfo=zoneinfo.ZoneInfo("UTC")), None, 0],
#         ['a29a90ff-15de-4871-8482-9a5f08ac40a9', 'Sample Video Title 58010e69', 'sample-video-title-58010e69-3579d687', 'This is a sample description for the video Sample Video Title 58010e69.', 'Web Development', 'Frontend, TypeScript', '/media/videos/sample2.mp4', '/media/thumbnails/sample2.jpg', 0, datetime.datetime(2025, 3, 11, 22, 46, 29, 907636, tzinfo=zoneinfo.ZoneInfo("UTC")), datetime.datetime(2025, 3, 11, 22, 46, 29, 907663, tzinfo=zoneinfo.ZoneInfo("UTC")), None, 0]
#     ]
    
#     # Use a title from one of the sources for recommendations.
#     search_title = "Quiz: Web Dev Basics"
#     recommendations = get_hybrid_recommendations(articles, quizzes, videos, search_title, top_n=5)
    
#     print("Hybrid Recommendations (as dictionary):")
#     for title, content_type in recommendations.items():
#         print(f"{title}: {content_type}")
