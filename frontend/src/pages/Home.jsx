import React from 'react';
import Navbar from '../components/Navbar';
import Footer from '../components/Footer';
import HeroSection from '../components/HeroSection';
import LearnByDoingSection from '../components/LearnByDoingSection';
import StreakSection from '../components/StreakSection';
import ModulesSection from '../components/ModulesSection';
import SpecializedTracksSection from '../components/SpecializedTracksSection';
import JourneyMapSection from '../components/JourneyMapSection';
import LeaderboardSection from '../components/LeaderboardSection';
import { AnywhereSection, CertificateSection, CTASection } from '../components/BottomSections';

export default function Home() {
  return (
    <div className="min-h-screen" style={{ background: 'var(--cf-space)' }}>
      <Navbar />
      <main>
        <HeroSection />
        <LearnByDoingSection />
        <StreakSection />
        <ModulesSection />
        <SpecializedTracksSection />
        <JourneyMapSection />
        <AnywhereSection />
        <LeaderboardSection />
        <CertificateSection />
        <CTASection />
      </main>
      <Footer />
    </div>
  );
}
