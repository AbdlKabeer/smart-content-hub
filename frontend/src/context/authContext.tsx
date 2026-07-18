import React, { createContext, useContext, useState, useEffect } from 'react';
import { toast } from 'react-toastify';

interface AuthContextType {
  user: any;
  authToken: any;
  globalLoading: any;
  setGlobalLoading: React.Dispatch<React.SetStateAction<any>>;
  globalLoadingText: string;
  setGlobalLoadingText: React.Dispatch<React.SetStateAction<any>>;
  login: (email: string, password: string) => void;
  logout: () => void;
  checkRole: (requiredRole: string) => boolean;
  fetchWithAuth: (params: any) => Promise<any>;
  displayNotification: (type: string, text: any) => void;
  setUser: React.Dispatch<React.SetStateAction<any>>;
  BACKEND_URL:string;
  setAuthToken:React.Dispatch<React.SetStateAction<any>>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  // const BACKEND_URL = 'http://127.0.0.1:8000/api/v1';

  const BACKEND_URL = 'https://ayo-recommendation-backend.onrender.com/api/v1';

  const [user, setUser] = useState<any>(() => JSON.parse(localStorage.getItem('user') || 'null'));
  const [authToken, setAuthToken] = useState<any>(() => JSON.parse(localStorage.getItem('tokens') || 'null'));
  const [loading, setLoading] = useState(true);
  const [globalLoading, setGlobalLoading] = useState<any>(false);
  const [globalLoadingText, setGlobalLoadingText] = useState<any>('Loading....');

  // Fetch user profile after the token is available or on token update
  const fetchUserProfile = async () => {
    if (!authToken?.access) return;

    try {
      setGlobalLoadingText("Setting up profile...")
      setGlobalLoading(true);
      

      const data = await fetchWithAuth({
        method: 'GET',
        path: `/account/`,
      });
      console.log(data);
      setUser(data?.data);
    } catch (error) {
      console.error('Error fetching user profile:', error);
    }finally{
      setGlobalLoading(false);
    }
  };

  useEffect(() => {
    // Check if there's an auth token in localStorage and set the user on page load
    const token = localStorage.getItem('tokens');
    if (token) {
      fetchUserProfile();
    }
    setLoading(false);
  }, []); // This runs once on page load to check the token

  // Mimicking the login API call to check username and assign role
  const login = async (email: string, password: string) => {
    const request_data = {
      email: email,
      password: password,
    };

    try {
      const data = await fetchWithAuth({
        method: 'POST',
        path: `/auth/login`,
        body: request_data,
      });
      setAuthToken(data?.data?.tokens);
      localStorage.setItem('tokens', JSON.stringify(data?.data?.tokens));
      localStorage.setItem('user', JSON.stringify(data?.data?.user));
      setUser(data?.data?.user);
      return data?.data?.user;
    } catch (error) {
      console.error('Error fetching user profile:', error);
      return null
    }
  };

  function displayNotification(type: string, text: any) {
    if (type === 'info') {
      toast.info(`${text}`, {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: 'colored',
      });
    } else if (type === 'success') {
      toast.success(`${text}`, {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: 'colored',
      });
    } else if (type === 'error') {
      toast.error(`${text}`, {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: 'colored',
      });
    } else {
      toast(`${text}`, {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
        theme: 'colored',
      });
    }
  }

  const deleteUserFromLocalStorage = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('tokens');
    window.location.href = '/login';
  };

  async function fetchWithAuth({
    method = 'GET',
    path,
    queryParams = {},
    body = null,
    isFormData = false,
  }: {
    method?: string;
    path: string;
    queryParams?: Record<string, any>;
    body?: any;
    isFormData?: boolean;
  }) {
    const accessToken = authToken?.access;
    const refreshToken = authToken?.refresh;
    const REFRESH_TOKEN_URL = `${BACKEND_URL}/auth/token/refresh/`;

    // Build the full URL with query parameters if provided
    let url = `${BACKEND_URL}${path}`;
    if (Object.keys(queryParams).length > 0) {
      const query = new URLSearchParams(queryParams).toString();
      url = `${url}?${query}`;
    }

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    // Include the access token in the Authorization header if available
    if (accessToken) {
      headers['Authorization'] = `Bearer ${accessToken}`;
    }

    let response;
    if (isFormData) {
      const headers: Record<string, string> = {
        // 'Content-Type': 'application/json',
      };
      response = await fetch(url, { method, headers, body: body });
    } else {
      response = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : null });
    }

    // Check if the response is a 401 (Unauthorized) error (token might be expired)
    if (response.status === 401 && refreshToken) {
      try {
        // Attempt to refresh the token using the refresh token
        const refreshResponse = await fetch(REFRESH_TOKEN_URL, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ refresh: refreshToken }),
        });

        if (!refreshResponse.ok) {
          throw new Error('Unable to refresh token');
        }

        // Parse the new tokens from the response
        const refreshData = await refreshResponse.json();
        // Store the new tokens in localStorage
        localStorage.setItem('tokens', JSON.stringify(refreshData));
        setAuthToken(refreshData);
        // Retry the original request with the new access token
        headers['Authorization'] = `Bearer ${refreshData?.access}`;
        response = await fetch(url, { method, headers, body: body ? JSON.stringify(body) : null });

        if (!response.ok) {
          handleErrorResponse(response);
        }

        return response.json();
      } catch (error) {
        console.error('Token refresh failed:', error);
        deleteUserFromLocalStorage();
        throw new Error('Authentication error. Please log in again.');
      }
    }

    if (!response.ok) {
      handleErrorResponse(response);
    }

    return response.json();
  }

  const handleErrorResponse = (response: Response) => {
    if (response.status === 400) {
      response.json().then((errorData) => {
        displayNotification('error', errorData?.message);
      });
    }
    if (response.status === 401) {
      deleteUserFromLocalStorage();
    }
    if (response.status === 500) {
      response.json().then((errorData) => {
        displayNotification('error', errorData?.message);
      });
    }
    throw new Error(`Error fetching data: ${response.statusText}`);
  };

  // Logout function
  const logout = () => {
    localStorage.removeItem('tokens');
    localStorage.removeItem('user');
    setUser(null);
    setAuthToken(null)
    displayNotification('success', 'Logged out successfully');
    window.location.pathname = '/'
  };

  // Check if user has required role
  const checkRole = (requiredRole: string) => {
    if (user && user.role) {
      return user.role === requiredRole;
    }
    return false;
  };

  const value: AuthContextType = {
    user,
    authToken,
    login,
    logout,
    checkRole,
    fetchWithAuth,
    displayNotification,
    setUser,
    globalLoading,
    setGlobalLoading,
    globalLoadingText,
    setGlobalLoadingText,
    BACKEND_URL,
    setAuthToken
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};
