import './App.css';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
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

function App() {
  return (
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
          </Routes>
        </BrowserRouter>
        <Toaster position="top-right" richColors />
      </LanguageProvider>
    </div>
  );
}

export default App;
