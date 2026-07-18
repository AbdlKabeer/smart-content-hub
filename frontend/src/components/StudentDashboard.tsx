// import React, { useEffect, useState } from 'react';
// import { Video, BookOpen } from 'lucide-react';
// import { Link, useNavigate } from 'react-router-dom';
// import { useAuth } from '../context/authContext';

// // Define TypeScript interfaces
// interface Student {
//   name: string;
//   course: string;
//   year: string;
// }

// interface VideoRecommendation {
//   id: number;
//   title: string;
//   thumbnail: string;
//   duration: string;
//   instructor: string;
//   views: string;
// }

// interface ArticleRecommendation {
//   id: number;
//   title: string;
//   top_image: string;
//   author: string;
//   readTime: string;
//   date: string;
// }

// const StudentDashboard: React.FC = () => {



//   const [student] = useState<Student>({
//     name: "Olanrewaju AbdulKabeer",
//     course: "Computer Science",
//     year: "Finalist"
//   });

//   const navigate = useNavigate()

//   const { fetchWithAuth } = useAuth();

//   const [isVideoLoading, setIsVideoLoading] = useState(true);
//   const [isArticleLoading, setIsArticleLoading] = useState(true);

//   const [recommendedVideos, setRecommendedVideos] = useState<VideoRecommendation[]>([
  
//   ]);

//   const [recommendedArticles, setRecommendedArticles] = useState<ArticleRecommendation[]>([
  
//   ]);


//   async function fetchVideos() {
//     try {
//       setIsVideoLoading(true);
      
//       const data = await fetchWithAuth({
//         method: 'GET',
//         path: `/admin/videos/recommendation`,
//       });
      
//       setRecommendedVideos(data?.data)
//     } catch (error) {
//       console.error('Error fetching videos:', error);
//     } finally {
//       setIsVideoLoading(false);
//     }
//   }

//   async function fetchArticles() {
//     try {
//       setIsArticleLoading(true);
      
//       const data = await fetchWithAuth({
//         method: 'GET',
//         path: `/admin/articles/recommendation`,
//       });
      
//       setRecommendedArticles(data?.data)
//     } catch (error) {
//       console.error('Error fetching videos:', error);
//     } finally {
//       setIsArticleLoading(false);
//     }
//   }

//   useEffect(() => {
//     fetchVideos();
//     fetchArticles();
//   }, []);


//   // Get current time of day for greeting
//   const getGreeting = (): string => {
//     const hour = new Date().getHours();
//     if (hour < 12) return "Good morning";
//     if (hour < 18) return "Good afternoon";
//     return "Good evening";
//   };

//   return (
//     <div className="bg-gray-100 p-6 min-h-screen">
//       {/* Welcome Section */}
//       <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-8 mb-8 text-white">
//         <h2 className="text-3xl font-bold mb-2">{getGreeting()}, {student.name}!</h2>
//         <p className="opacity-90 mb-4">{student.year} • {student.course}</p>
//         <p className="text-lg">Your weekly progress is on track. You've completed 80% of this week's assignments.</p>
//       </div>

//       {/* Content Sections */}
//       <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
//         {/* Video Recommendations */}
//         <div className="bg-white rounded-xl shadow p-6">
//           <h2 className="text-xl font-bold mb-4 flex items-center">
//             <Video size={20} className="mr-2 text-indigo-600" />
//             Top Pick Videos for You
//           </h2>
//           <div className="space-y-4">
//             {isVideoLoading ? (
//               <div className="flex justify-center items-center h-64">
//                 <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
//               </div>
//             ): (
//               <>
//               {recommendedVideos?.map((video) => (
//               <Link to={`/videos/${video.id}`} key={video.id} className="flex space-x-4 hover:bg-gray-50 p-2 rounded-lg transition-colors cursor-pointer">
//                 <div className="relative flex-shrink-0">
//                   <img src={video.thumbnail} alt={video.title} className="w-32 h-20 object-cover rounded-md" />
//                   {/* <div className="absolute bottom-1 right-1 bg-black bg-opacity-75 text-white text-xs px-1 py-0.5 rounded">
//                     {video.duration}
//                   </div> */}
//                 </div>
//                 <div className="flex-1">
//                   <h3 className="font-medium text-gray-900">{video.title}</h3>
//                   <p className="text-gray-600 text-sm">{video.instructor}</p>
//                   <p className="text-gray-500 text-xs">{video.views} views</p>
//                 </div>
//               </Link >
//             ))}
//              <button 
//               onClick={()=> navigate('/videos')}
//               className="w-full mt-4 text-indigo-600 font-medium py-2 hover:bg-indigo-50 rounded-lg transition-colors">
//               View All Recommended Videos
//             </button>
//               </>
//             )}
            
//           </div>
         
//         </div>

//         {/* Article Recommendations */}
//         <div className="bg-white rounded-xl shadow p-6">
//           <h2 className="text-xl font-bold mb-4 flex items-center">
//             <BookOpen size={20} className="mr-2 text-indigo-600" />
//             Top Pick Articles for You
//           </h2>
//           <div className="space-y-4">
//             {isArticleLoading ? (
//               <div className="flex justify-center items-center h-64">
//                 <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-indigo-500"></div>
//               </div>
//             ): (
//               <>
//               {recommendedArticles.map((article) => (
//               <Link to={`/articles/${article.id}`} key={article.id} className="flex space-x-4 hover:bg-gray-50 p-2 rounded-lg transition-colors cursor-pointer">
//                 <img src={article.top_image} alt={article.title} className="w-32 h-20 object-cover rounded-md flex-shrink-0" />
//                 <div className="flex-1">
//                   <h3 className="font-medium text-gray-900">{article.title}</h3>
//                   <p className="text-gray-600 text-sm">{article.author}</p>
//                   {/* <p className="text-gray-500 text-xs">{article.readTime} • {article.date}</p> */}
//                 </div>
//               </Link>
//               ))}
//              <button onClick={()=> navigate('/articles')} className="w-full mt-4 text-indigo-600 font-medium py-2 hover:bg-indigo-50 rounded-lg transition-colors">
//               View All Recommended Articles
//             </button>
//               </>
//             )}
            
//           </div>
         
//         </div>
//       </div>
//     </div>
//   );
// };

// export default StudentDashboard;


import React, { useEffect, useState } from 'react';
import { BookOpen, PlayCircle } from 'lucide-react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/authContext';

interface ContentRecommendation {
  id: number;
  title: string;
  thumbnail: string;
  type: 'video' | 'article';
  creator: string;
  views?: string;
  duration?: string;
  readTime?: string;
}

const StudentDashboard: React.FC = () => {
  const [student] = useState({
    name: "Olanrewaju AbdulKabeer",
    course: "Computer Science",
    year: "Finalist"
  });

  const { fetchWithAuth, user } = useAuth();

  const [isLoading, setIsLoading] = useState(true);
  const [recommendations, setRecommendations] = useState<ContentRecommendation[]>([]);

  async function fetchRecommendations() {
    try {
      setIsLoading(true);
      
      const [videoData, articleData] = await Promise.all([
        fetchWithAuth({
          method: 'GET',
          path: `/admin/videos/recommendation`,
        }),
        fetchWithAuth({
          method: 'GET',
          path: `/admin/articles/recommendation`,
        })
      ]);
      
      
      const combinedRecommendations = [
        ...(videoData?.data || []).map((video: { instructor: any; thumbnail: any; }) => ({
          ...video,
          type: 'video' as const,
          creator: video.instructor,
          thumbnail: video.thumbnail
        })),
        ...(articleData?.data || []).map((article: { author: any; top_image: any; }) => ({
          ...article,
          type: 'article' as const,
          creator: article.author,
          thumbnail: article.top_image
        }))
      ].sort(() => 0.5 - Math.random()) 
       .slice(0, 10); 

      setRecommendations(combinedRecommendations);
    } catch (error) {
      console.error('Error fetching recommendations:', error);
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    fetchRecommendations();
  }, []);

  const getGreeting = (): string => {
    const hour = new Date().getHours();
    if (hour < 12) return "Good morning";
    if (hour < 18) return "Good afternoon";
    return "Good evening";
  };

  return (
    <div className="bg-gray-50 min-h-screen p-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl p-6 mb-6 text-white">
        <h2 className="text-2xl font-bold mb-2">{getGreeting()}, {student.name}!</h2>
        <p className="opacity-90">{student.year} • {student.course}</p>
        <p className="mt-2 text-sm">Your weekly learning progress is on track. {user?.role}</p>
      </div>

      {/* Mixed Recommendations Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {isLoading 
          ? Array(8).fill(0).map((_, index) => (
              <div key={index} className="bg-white rounded-lg shadow-md animate-pulse">
                <div className="h-44 bg-gray-200 rounded-t-lg"></div>
                <div className="p-3">
                  <div className="h-4 bg-gray-200 mb-2 w-3/4"></div>
                  <div className="h-3 bg-gray-200 w-1/2"></div>
                </div>
              </div>
            ))
          : recommendations.map((item) => (
              <Link 
                to={`/${item.type}s/${item.id}`} 
                key={item.id} 
                className="bg-white rounded-lg shadow-md hover:shadow-lg transition-all group"
              >
                <div className="relative">
                  <img 
                    src={item.thumbnail} 
                    alt={item.title} 
                    className="w-full h-44 object-cover rounded-t-lg group-hover:opacity-90 transition-opacity"
                  />
                  <div className="absolute top-2 left-2 bg-black/60 text-white text-xs px-2 py-1 rounded flex items-center">
                    {item.type === 'video' 
                      ? <><PlayCircle size={12} className="mr-1" /> Video</> 
                      : <><BookOpen size={12} className="mr-1" /> Article</>}
                  </div>
                  {item.type === 'video' && item.duration && (
                    <div className="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-2 py-1 rounded">
                      {item.duration}
                    </div>
                  )}
                </div>
                <div className="p-3">
                  <h3 className="font-semibold text-gray-800 line-clamp-2 mb-1 text-sm">
                    {item.title}
                  </h3>
                  <p className="text-gray-600 text-xs">{item.creator}</p>
                  {item.type === 'video' && item.views && (
                    <p className="text-gray-500 text-xs mt-1">{item.views} views</p>
                  )}
                  {item.type === 'article' && item.readTime && (
                    <p className="text-gray-500 text-xs mt-1">{item.readTime} read</p>
                  )}
                </div>
              </Link>
            ))
        }
      </div>
    </div>
  );
};

export default StudentDashboard;