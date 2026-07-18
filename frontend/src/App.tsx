
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom'; // Correct import
import { ToastContainer } from 'react-toastify';
import PrivateRoute from './components/PrivateRoute';
import RoleBasedRoute from './components/RoleBasedRoute';
import UnauthenticatedRoute from './components/UnauthenticatedRoute';
import { useAuth } from './context/authContext'; // Import useAuth
import './index.css';
import AddQuizQuestionFormPage from './pages/AddQuizQuestionFormPage';
import Login from './pages/Login';
import Register from './pages/Register';
import Unauthorized from './pages/Unauthorized';
import Loader from './components/Loader';
import AllVideosPage from './pages/videos/AllVideosPage';
import VideoPlayerPage from './pages/videos/VideoPlayerPage';
import ArticleReadingPage from './pages/articles/ArticleReadingPage';
import ArticlesList from './pages/articles/ArticleDetail';
import RecommendedQuizzes from './pages/quiz/RecommendedQuizzes';
import QuizTakingPage from './pages/quiz/QuizTakingPage';
import ProfileManagementPage from './pages/ProfileManagementPage';
import AdminQuizUploadPage from './pages/quiz/admin/AdminQuizUploadPage';
import QuizListingPage from './pages/quiz/admin/QuizListingPage';
import AdminQuizEditPage from './pages/quiz/admin/AdminQuizEditPage';
import VideoUploadPage from './pages/videos/admin/VideoUploadPage';
import VideoListingPage from './pages/quiz/admin/VideoListingPage';
import StudentListingPage from './pages/admin/students/StudentListingPage';
import AdminDashboard from './pages/admin/AdminDashboard';
import Home from './pages/Home';
import AdminArticlesList from './pages/admin/articles/AdminArticlesList';
import ArticleCreator from './pages/admin/articles/ArticleCreator';
import ArticleEditor from './pages/admin/articles/ArticleEditor';

function App() {

  const {globalLoading, globalLoadingText} = useAuth();
  return (
    <>
      <ToastContainer />
      {globalLoading && <Loader text={globalLoadingText}/>}
      <Router>
        <Routes>
          {/* Define all your routes within the <Routes> component */}

          {/* Public route for login with a check for unauthenticated users */}
          <Route path="/login" element={<UnauthenticatedRoute element={<Login />} />} />
          <Route path="/register" element={<UnauthenticatedRoute element={<Register />} />} />
          
          {/* Private Route for Home */}
          <Route path="/quiz/new/*" element={<PrivateRoute element={<AddQuizQuestionFormPage />} />} />
          <Route path="/home/*" element={<PrivateRoute element={<Home />} />} />
          <Route path="/videos/" element={<PrivateRoute element={<AllVideosPage />} />} />
          <Route path="/videos/:videoId" element={<PrivateRoute element={<VideoPlayerPage />} />} />
          <Route path="/account/*" element={<PrivateRoute element={<ProfileManagementPage />} />} />
          <Route path="/articles" element={<PrivateRoute element={<ArticlesList />} />} />
          <Route path="/articles/:id" element={<PrivateRoute element={<ArticleReadingPage />} />} />
          <Route path="/quizzes" element={<PrivateRoute element={<RecommendedQuizzes />} />} />
          <Route path="/quizzes/:id" element={<PrivateRoute element={<QuizTakingPage />} />} />
          
          

          <Route path="/admin/home" element={<RoleBasedRoute element={<AdminDashboard />} requiredRole="admin" />} />
          <Route path="/admin/quiz-list" element={<RoleBasedRoute element={<QuizListingPage />} requiredRole="admin" />} />
          <Route path="/admin/quiz-create" element={<RoleBasedRoute element={<AdminQuizUploadPage />} requiredRole="admin" />} />
          <Route path="/admin/quiz-edit/:id" element={<RoleBasedRoute element={<AdminQuizEditPage />} requiredRole="admin"/>} />
          <Route path="/admin/quiz-results" element={<RoleBasedRoute element={<AdminQuizUploadPage />} requiredRole="admin" />} />
          <Route path="/admin/video-list" element={<RoleBasedRoute element={<VideoListingPage />} requiredRole="admin" />} />
          <Route path="/admin/video-upload" element={<RoleBasedRoute element={<VideoUploadPage />} requiredRole="admin" />} />
          <Route path="/admin/article-list" element={<RoleBasedRoute element={<AdminArticlesList />} requiredRole="admin" />} />
          <Route path="/admin/article-create" element={<RoleBasedRoute element={<ArticleCreator />} requiredRole="admin" />} />
          <Route path="/admin/article-edit/:id" element={<RoleBasedRoute element={<ArticleEditor />} requiredRole="admin" />} />

          <Route path="/admin/students" element={<RoleBasedRoute element={<StudentListingPage />} requiredRole="admin" />} />
          
          {/* Unauthorized route */}
          <Route path="/unauthorized" element={<Unauthorized />} />
          
          {/* Redirect to home */}
          <Route path="/" element={<Navigate to="/home" />} />

        </Routes>
      </Router>
    </>
  );
}

export default App;
