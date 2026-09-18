import { NavLink } from 'react-router-dom'
import { skillbridgeData } from '../data/skillbridgeData'
import { IconGrid, IconBriefcase, IconBars, IconScale, IconTarget } from './icons'

const NAV = [
  { to: '/', label: 'Overview', icon: IconGrid, end: true },
  { to: '/jobs', label: 'Job explorer', icon: IconBriefcase },
  { to: '/skills', label: 'Skills demand', icon: IconBars },
  { to: '/comparison', label: 'India vs Malaysia', icon: IconScale },
  { to: '/skill-gap', label: 'Skill-gap checker', icon: IconTarget },
]

export default function Sidebar({ open, onClose }) {
  const { summary } = skillbridgeData

  return (
    <>
      {open && (
        <button
          aria-label="Close navigation"
          onClick={onClose}
          className="fixed inset-0 z-30 bg-black/50 lg:hidden"
        />
      )}
      <aside
        className={`fixed z-40 inset-y-0 left-0 w-72 shrink-0 border-r border-hairline bg-surface
        flex flex-col transition-transform duration-200 lg:static lg:translate-x-0
        ${open ? 'translate-x-0' : '-translate-x-full'}`}
      >
        <div className="flex items-center gap-3 px-6 pt-7 pb-6">
          <div className="h-9 w-9 rounded-md bg-gradient-to-br from-india to-malaysia flex items-center justify-center font-display font-bold text-canvas text-sm">
            SB
          </div>
          <div>
            <div className="font-display font-semibold text-ink leading-none">SkillBridge</div>
            <div className="text-[11px] text-faint mt-1 leading-none">Job market &amp; skill-gap intelligence</div>
          </div>
        </div>

        <nav className="flex-1 px-3 space-y-1">
          {NAV.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={onClose}
              className={({ isActive }) =>
                `group flex items-center gap-3 rounded-md px-3 py-2.5 text-sm transition-colors ${
                  isActive
                    ? 'bg-elevated text-ink'
                    : 'text-muted hover:text-ink hover:bg-elevated/60'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <Icon className={`h-[18px] w-[18px] ${isActive ? 'text-signal' : 'text-faint group-hover:text-muted'}`} />
                  <span>{label}</span>
                </>
              )}
            </NavLink>
          ))}
        </nav>

        <div className="px-6 py-5 border-t border-hairline">
          <div className="text-[11px] uppercase tracking-wide text-faint mb-2" style={{ letterSpacing: '0.04em' }}>
            Dataset
          </div>
          <div className="flex items-baseline gap-1.5 text-ink font-display font-semibold text-lg tabular">
            {summary.totalJobs.toLocaleString()}
            <span className="text-xs font-body font-normal text-muted">live listings</span>
          </div>
          <div className="mt-2 flex gap-3 text-xs text-muted">
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-india" />
              India {summary.indiaJobs.toLocaleString()}
            </span>
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-malaysia" />
              Malaysia {summary.malaysiaJobs.toLocaleString()}
            </span>
          </div>
        </div>
      </aside>
    </>
  )
}
