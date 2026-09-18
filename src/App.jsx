import { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import MobileBar from './components/MobileBar'
import Dashboard from './pages/Dashboard'
import JobExplorer from './pages/JobExplorer'
import SkillsDemand from './pages/SkillsDemand'
import Comparison from './pages/Comparison'
import SkillGap from './pages/SkillGap'

export default function App() {
  const [navOpen, setNavOpen] = useState(false)

  return (
    <div className="min-h-screen flex">
      <Sidebar open={navOpen} onClose={() => setNavOpen(false)} />

      <div className="flex-1 min-w-0 flex flex-col">
        <MobileBar onOpen={() => setNavOpen(true)} />

        <main className="flex-1 px-5 py-8 lg:px-10 lg:py-10 max-w-[1180px] w-full mx-auto">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/jobs" element={<JobExplorer />} />
            <Route path="/skills" element={<SkillsDemand />} />
            <Route path="/comparison" element={<Comparison />} />
            <Route path="/skill-gap" element={<SkillGap />} />
          </Routes>
        </main>
      </div>
    </div>
  )
}
