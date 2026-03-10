import React, { useContext, useState, useEffect } from 'react';
import { AuthProvider, AuthContext } from './AuthContext'; 
import Login from './components/Login';
import Signup from './components/Signup';
import ForgotPassword from './components/ForgotPassword';
import ResetPassword from './components/ResetPassword';
import Dashboard from './components/Dashboard';
import SharedAgreementView from './components/SharedAgreementView';

const MainContent = () => {
  const { token } = useContext(AuthContext); 
  const [authView, setAuthView] = useState('login'); // 'login', 'signup', 'forgot', 'reset'
  const [isSharedView, setIsSharedView] = useState(false);

  useEffect(() => {
    // Check if URL has reset token
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('token')) {
      setAuthView('reset');
    }
    
    // Check if this is a shared agreement URL
    if (window.location.pathname.startsWith('/shared-agreement/')) {
      setIsSharedView(true);
    }
  }, []);

  // If it's a shared agreement view, show only the agreement
  if (isSharedView) {
    return <SharedAgreementView />;
  }

  // If user is logged in, show dashboard
  if (token) {
    return <Dashboard />;
  }

  // Otherwise show auth screens
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