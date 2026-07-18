import React, { useEffect, useState } from 'react';
import { 
  Users, 
  Video, 
  BookOpen, 
  ClipboardList, 
  Star, 
  ThumbsUp, 
  Bookmark, 
  BarChart2, 
  TrendingUp 
} from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { useAuth } from '../../context/authContext';
import { useNavigate } from 'react-router-dom';

// Interfaces for data types
interface AnalyticsSummary {
  students: {
    total: number;
    newThisMonth: number;
    activeUsers: number;
  };
  videos: {
    total: number;
    totalViews: number;
    averageRating: number;
  };
  articles: {
    total: number;
    totalLikes: number;
    totalBookmarks: number;
  };
  quizzes: {
    total: number;
    averageScore: number;
    highestScore: number;
  };
}

interface AnalyticsTimeSeriesData {
  name: string;
  students?: number;
  videos?: number;
  articles?: number;
  quizzes?: number;
}

const AdminDashboard: React.FC = () => {
    const { fetchWithAuth } = useAuth();
    const navigate = useNavigate()
  const [summary, setSummary] = useState<AnalyticsSummary>({
    students: {
      total: 0,
      newThisMonth: 0,
      activeUsers: 0
    },
    videos: {
      total: 0,
      totalViews: 0,
      averageRating: 0
    },
    articles: {
      total: 0,
      totalLikes: 0,
      totalBookmarks: 0
    },
    quizzes: {
      total: 0,
      averageScore: 0,
      highestScore: 0
    }
  });

  const [timeSeriesData,setTimeSeriesData] = useState<AnalyticsTimeSeriesData[]>([
    { name: 'Jan', students: 0, videos: 0, articles: 0, quizzes: 0 },
    { name: 'Feb', students: 0, videos: 0, articles: 0, quizzes: 0 },
    { name: 'Mar', students: 0, videos: 0, articles: 0, quizzes: 0 },
    { name: 'Apr', students: 0, videos: 0, articles: 0, quizzes: 0 }
  ]);

  const StatCard = ({ 
    icon: Icon, 
    title, 
    value, 
    subValue, 
    color 
  }: { 
    icon: React.ElementType, 
    title: string, 
    value: string | number, 
    subValue?: string | number, 
    color: string 
  }) => (
    <div className={`bg-white rounded-lg shadow p-4 ${color} transition-all hover:shadow-md`}>
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-sm text-gray-600 mb-2">{title}</h3>
          <p className="text-2xl font-bold text-gray-800">{value}</p>
          {subValue && (
            <p className="text-xs text-green-600 mt-1">
              +{subValue} this month
            </p>
          )}
        </div>
        <Icon className={`${color} opacity-50`} size={36} />
      </div>
    </div>
  );

  const fetchMainOverview = async () => {
    try {
      const response = await fetchWithAuth({
        method: 'GET',
        path: `/overview`,
      });
      
      setSummary(response?.data);
    } catch (err) {
      console.error('Error fetching article:', err);
    }
  };
  const fetchMainOverviewLastFourMonth = async () => {
    try {
      const response = await fetchWithAuth({
        method: 'GET',
        path: `/overview/last_4_months_overview`,
      });
      
      setTimeSeriesData(response?.data);
    } catch (err) {
      console.error('Error fetching article:', err);
    }
  };

  useEffect(() => {
    fetchMainOverview()
    fetchMainOverviewLastFourMonth()
    }, []);

  return (
    <div className="bg-gray-50 min-h-screen p-6">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Admin Dashboard</h1>

      {/* Overview Grid */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
        <StatCard 
          icon={Users}
          title="Total Students"
          value={summary.students.total}
          subValue={summary.students.newThisMonth}
          color="text-blue-500"
        />
        <StatCard 
          icon={Video}
          title="Video Content"
          value={summary.videos.total}
          subValue={summary.videos.totalViews}
          color="text-purple-500"
        />
        <StatCard 
          icon={BookOpen}
          title="Articles"
          value={summary.articles.total}
          subValue={summary.articles.totalLikes}
          color="text-green-500"
        />
        <StatCard 
          icon={ClipboardList}
          title="Quizzes"
          value={summary.quizzes.total}
          subValue={summary.quizzes.averageScore}
          color="text-red-500"
        />
      </div>

      {/* Detailed Analytics */}
      <div className="grid md:grid-cols-2 gap-6">
        {/* Content Engagement Chart */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <TrendingUp className="mr-2 text-blue-600" size={24} />
            Content Growth
          </h2>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={timeSeriesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="students" stroke="#8884d8" />
              <Line type="monotone" dataKey="videos" stroke="#82ca9d" />
              <Line type="monotone" dataKey="articles" stroke="#ffc658" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Detailed Content Metrics */}
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4 flex items-center">
            <BarChart2 className="mr-2 text-green-600" size={24} />
            Content Metrics
          </h2>
          <div className="space-y-4">
            <div className="flex justify-between items-center border-b pb-2">
              <div className="flex items-center">
                <Star className="text-yellow-500 mr-2" size={20} />
                <span>Video Average Rating</span>
              </div>
              <span className="font-bold">{summary.videos.averageRating}/5</span>
            </div>
            <div className="flex justify-between items-center border-b pb-2">
              <div className="flex items-center">
                <ThumbsUp className="text-blue-500 mr-2" size={20} />
                <span>Article Total Likes</span>
              </div>
              <span className="font-bold">{summary.articles.totalLikes}</span>
            </div>
            <div className="flex justify-between items-center border-b pb-2">
              <div className="flex items-center">
                <Bookmark className="text-green-500 mr-2" size={20} />
                <span>Article Bookmarks</span>
              </div>
              <span className="font-bold">{summary.articles.totalBookmarks}</span>
            </div>
            <div className="flex justify-between items-center">
              <div className="flex items-center">
                <ClipboardList className="text-red-500 mr-2" size={20} />
                <span>Quiz Average Score</span>
              </div>
              <span className="font-bold">{summary.quizzes.averageScore}%</span>
            </div>
          </div>
        </div>
      </div>

      {/* Quick Actions and Recent Activity */}
      <div className="mt-6 grid md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
          <div className="grid grid-cols-2 gap-4">
            <button onClick={()=> navigate('/admin/video-upload')} className="bg-blue-50 text-blue-600 py-2 rounded hover:bg-blue-100">
              Add New Video
            </button>
            {/* <button onClick={()=> navigate('/admin/video-upload')}  className="bg-green-50 text-green-600 py-2 rounded hover:bg-green-100">
              Create Article
            </button> */}
            <button onClick={()=> navigate('/admin/quiz-create')}  className="bg-red-50 text-red-600 py-2 rounded hover:bg-red-100">
              Generate Quiz
            </button>
            <button onClick={()=> navigate('/admin/students')}  className="bg-purple-50 text-purple-600 py-2 rounded hover:bg-purple-100">
              Manage Users
            </button>
          </div>
        </div>
        {/* <div className="bg-white rounded-lg shadow p-4">
          <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
          <ul className="space-y-2">
            <li className="flex justify-between items-center border-b pb-2">
              <span>New video uploaded: React Hooks Masterclass</span>
              <span className="text-sm text-gray-500">2h ago</span>
            </li>
            <li className="flex justify-between items-center border-b pb-2">
              <span>Quiz created: JavaScript Fundamentals</span>
              <span className="text-sm text-gray-500">5h ago</span>
            </li>
            <li className="flex justify-between items-center">
              <span>50 new student registrations</span>
              <span className="text-sm text-gray-500">1d ago</span>
            </li>
          </ul>
        </div> */}
      </div>
    </div>
  );
};

export default AdminDashboard;