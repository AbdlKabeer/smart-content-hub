// @ts-nocheck
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';

// TypeScript interface for the Article data
interface Article {
  id: string;
  title: string;
  authors: string;
  publish_date: string;
  source_url: string;
  text: string; // Ensure the backend is sending formatted HTML here
  keywords: string;
  top_image: string;
  meta_description: string;
  summary: string;
}

interface Feedback {
  helpful: 'yes' | 'no' | null;
  moreContent: 'yes' | 'no' | null;
}

const ArticleDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>(); // { id: string } defines the shape of the params

  // State to hold the article data
  const [article, setArticle] = useState<Article | null>(null);

  // State for feedback modal visibility and feedback data
  const [modalVisible, setModalVisible] = useState(false);
  const [feedback, setFeedback] = useState<Feedback>({ helpful: null, moreContent: null });

  // Fetch the article from the backend
  useEffect(() => {
    const fetchArticle = async () => {
      try {
        if (id) {
          const response = await axios.get<Article>(`http://127.0.0.1:8000/api/v1/article/${id}/`);
          setArticle(response?.data?.data);
        }
      } catch (error) {
        console.error("Error fetching article:", error);
      }
    };

    fetchArticle();
  }, [id]);

  // Automatically trigger the feedback modal after 1 minute (60000ms)
  useEffect(() => {
    const timer = setTimeout(() => {
      setModalVisible(true);
    }, 30000); // 30 seconds

    // Cleanup timeout if the component is unmounted or user navigates away
    return () => clearTimeout(timer);
  }, []);

  if (!article) {
    return <div className="text-center text-xl text-gray-500">Loading...</div>;
  }

  // Handle newlines in plain text and convert them to <br /> tags
  const formattedText = article.text ? article.text.split('\n').map((line, index) => (
    <span key={index}>
      {line}
      <br />
    </span>
  )) : '';

  // Handle the feedback submission
  const handleFeedbackSubmit = () => {
    console.log('Feedback submitted:', feedback);
    // Here, you can send the feedback data to your backend.
    setModalVisible(false); // Close the modal after submitting
  };

  return (
    <div className="container mx-auto p-6 md:px-12 lg:px-24">
      <div className="bg-white p-6 rounded-lg shadow-xl max-w-3xl mx-auto">
        {/* Title */}
        <h1 className="text-4xl font-semibold text-gray-900 leading-tight mb-4">{article.title}</h1>
        
        {/* Author & Date */}
        <div className="text-gray-600 mb-6">
          <p className="text-lg">By <span className="font-semibold">{article.authors}</span></p>
          <p className="text-sm text-gray-400">{new Date(article.publish_date).toLocaleDateString()}</p>
        </div>
        
        {/* Top Image */}
        {article.top_image && (
          <img 
            src={article.top_image} 
            alt={article.title} 
            className="w-full mb-6 rounded-xl shadow-md object-cover h-80"
          />
        )}

        {/* Article Content */}
        <div className="prose prose-lg text-gray-800 mb-8">
          {article.text.includes('<') ? (
            // If the article text is already HTML-formatted, render it safely using dangerouslySetInnerHTML
            <div dangerouslySetInnerHTML={{ __html: article.text }} />
          ) : (
            // If it's plain text with newlines, render it with <br /> tags
            formattedText
          )}
        </div>

        {/* Read More Link */}
        <div className="flex justify-start">
          <a 
            href={article.source_url} 
            className="text-blue-600 hover:underline font-medium text-lg" 
            target="_blank" 
            rel="noopener noreferrer"
          >
            Continue reading on the source
          </a>
        </div>
      </div>

      {/* Feedback Modal */}
      {modalVisible && (
        <div className="fixed inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50">
          <div className="bg-white p-6 rounded-lg shadow-md w-96">
            <h3 className="text-xl font-semibold mb-4">Feedback</h3>

            {/* Was this article helpful? */}
            <div className="mb-4">
              <p className="font-medium">Was this article helpful?</p>
              <div className="flex gap-4 mt-2">
                <button
                  className={`px-4 py-2 border rounded-md ${feedback.helpful === 'yes' ? 'bg-blue-500 text-white' : ''}`}
                  onClick={() => setFeedback({ ...feedback, helpful: 'yes' })}
                >
                  Yes
                </button>
                <button
                  className={`px-4 py-2 border rounded-md ${feedback.helpful === 'no' ? 'bg-red-500 text-white' : ''}`}
                  onClick={() => setFeedback({ ...feedback, helpful: 'no' })}
                >
                  No
                </button>
              </div>
            </div>

            {/* Would you like more content like this? */}
            <div className="mb-4">
              <p className="font-medium">Would you like more content like this?</p>
              <div className="flex gap-4 mt-2">
                <button
                  className={`px-4 py-2 border rounded-md ${feedback.moreContent === 'yes' ? 'bg-blue-500 text-white' : ''}`}
                  onClick={() => setFeedback({ ...feedback, moreContent: 'yes' })}
                >
                  Yes
                </button>
                <button
                  className={`px-4 py-2 border rounded-md ${feedback.moreContent === 'no' ? 'bg-red-500 text-white' : ''}`}
                  onClick={() => setFeedback({ ...feedback, moreContent: 'no' })}
                >
                  No
                </button>
              </div>
            </div>

            {/* Modal Actions */}
            <div className="flex justify-between">
              <button
                className="px-4 py-2 bg-gray-300 rounded-md"
                onClick={() => setModalVisible(false)}
              >
                Close
              </button>
              <button
                className="px-4 py-2 bg-blue-500 text-white rounded-md"
                onClick={handleFeedbackSubmit}
              >
                Submit
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ArticleDetail;
