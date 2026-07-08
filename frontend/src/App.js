import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { GoogleOAuthProvider } from '@react-oauth/google';
import { LanguageProvider } from './context/LanguageContext';
import { Toaster } from './components/ui/sonner';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Onboard from './pages/Onboard';
import Dashboard from './pages/Dashboard';
import Lesson from './pages/Lesson';
import JourneyPage from './pages/JourneyPage';
import LeaderboardPage from './pages/LeaderboardPage';
import Catalog from './pages/Catalog';
import Profile from './pages/Profile';
import Plans from './pages/Plans';
import PaymentSuccess from './pages/PaymentSuccess';
import Certificates from './pages/Certificates';
import VerifyCertificate from './pages/VerifyCertificate';
import Schools from './pages/Schools';
import ClassDetail from './pages/ClassDetail';
import AdminPanel from './pages/AdminPanel';

function App() {
  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID || ''}>
    <div className="App">
      <LanguageProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/onboard" element={<Onboard />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/licao/:slug" element={<Lesson />} />
            <Route path="/jornada/:slug" element={<JourneyPage />} />
            <Route path="/leaderboard" element={<LeaderboardPage />} />
            <Route path="/catalogo" element={<Catalog />} />
            <Route path="/catalog" element={<Catalog />} />
            <Route path="/perfil" element={<Profile />} />
            <Route path="/configuracoes" element={<Profile />} />
            <Route path="/planos" element={<Plans />} />
            <Route path="/pagamento/sucesso" element={<PaymentSuccess />} />
            <Route path="/certificados" element={<Certificates />} />
            <Route path="/verificar" element={<VerifyCertificate />} />
            <Route path="/verificar/:certId" element={<VerifyCertificate />} />
            <Route path="/escolas" element={<Schools />} />
            <Route path="/escolas/:classId" element={<ClassDetail />} />
            <Route path="/admin" element={<AdminPanel />} />
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" richColors />
      </LanguageProvider>
    </div>
    </GoogleOAuthProvider>
  );
}

export default App;
