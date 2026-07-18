import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
// Define types for the props in Card component
interface CardProps {
    id: string;
    title: string;
    summary: string;
    hyper_link: string;
    image: string;
}

// Card Component
const Card: React.FC<CardProps> = ({ id, title, summary, hyper_link, image }) => {
    console.log(hyper_link)
    return (
        <Link
            to={`/article/${id}`}
            className="block max-w-sm p-6 bg-white border border-gray-200 rounded-lg shadow hover:bg-gray-100 dark:bg-gray-800 dark:border-gray-700 dark:hover:bg-gray-700"
        >
            <img
                src={image || 'https://via.placeholder.com/150'}
                alt={title}
                className="rounded-t-lg w-full h-40 object-cover mb-4"
            />
            <h5 className="mb-2 text-2xl font-bold tracking-tight text-gray-900 dark:text-white">
                {title}
            </h5>
            <p className="font-normal text-gray-700 dark:text-gray-400">{summary}</p>
        </Link>
    );
}

// Define types for the article data
interface Article {
    id: string;
    title: string;
    summary: string;
    source_url: string;
    top_image: string;
    meta_description: string;
}

// ArticlesTopPick Component
const ArticlesTopPick: React.FC = () => {
    const [articles, setArticles] = useState<Article[]>([]);  // State to hold articles
    const [loading, setLoading] = useState<boolean>(true);  // State to handle loading state

    useEffect(() => {
        // Fetching the data from the API
        const fetchArticles = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/v1/articles?page_size=5');
                const data = await response.json();

                if (data.status) {
                    setArticles(data.data);  // Set the articles data from the API response
                } else {
                    console.error('Failed to fetch articles');
                }
            } catch (error) {
                console.error('Error fetching articles:', error);
            } finally {
                setLoading(false);  // Stop loading when the request completes
            }
        };

        fetchArticles();
    }, []);  // Empty dependency array ensures the effect runs only once

    return (
        <>
            <div className="py-4">
                <h3 className="text-xl font-medium pb-2">Top pick for you on articles</h3>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 md:grid-cols-3">
                    {loading ? (
                        <p>Loading articles...</p>
                    ) : articles.length > 0 ? (
                        articles.map((article) => (
                            <Card
                                key={article.id}
                                id={article.id}
                                title={article.title}
                                summary={article.summary || article.meta_description || 'No summary available.'}
                                hyper_link={article.source_url}
                                image={article.top_image}
                            />
                        ))
                    ) : (
                        <p>No articles available at the moment.</p>
                    )}
                </div>
            </div>
        </>
    );
}

export default ArticlesTopPick;
