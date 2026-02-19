import React, { useContext, useState, useEffect } from 'react';
import { AuthProvider, AuthContext } from './AuthContext'; 
import Login from './components/Login';
import Signup from './components/Signup';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import Dashboard from './components/Dashboard';

const MainContent = () => {
  const { token } = useContext(AuthContext); 
  const [authView, setAuthView] = useState('login'); // 'login', 'signup', 'forgot', 'reset'

  useEffect(() => {
    // Check if URL has reset token
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('token')) {
      setAuthView('reset');
    }
  }, []);

  if (token) {
    return <Dashboard />;
  }

  return (
    <div className="App">
      {authView === 'signup' && (
        <Signup switchToLogin={() => setAuthView('login')} />
      )}
      {authView === 'forgot' && (
        <ForgotPassword 
          switchToLogin={() => setAuthView('login')} 
        />
      )}
      {authView === 'reset' && (
        <ResetPassword 
          switchToLogin={() => setAuthView('login')} 
        />
      )}
      {authView === 'login' && (
        <Login 
          switchToSignup={() => setAuthView('signup')}
          switchToForgotPassword={() => setAuthView('forgot')}
        />
      )}
    </div> 
  );
};

function App() {
  return (
    <AuthProvider>
      <MainContent />
    </AuthProvider>
  );
}

export default App;