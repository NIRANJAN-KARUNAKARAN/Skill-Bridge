import { Link } from 'react-router-dom'
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
} from 'recharts'
import { skillbridgeData } from '../data/skillbridgeData'
import PageHeader from '../components/PageHeader'
import { Card, StatCard, SplitBar, CountryPill } from '../components/ui'
import { IconArrowUpRight, IconMapPin } from '../components/icons'

function ChartTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-md border border-hairline bg-elevated px-3 py-2 text-xs shadow-lg">
      <div className="text-ink font-medium mb-1">{label}</div>
      {payload.map((p) => (
        <div key={p.dataKey} className="flex items-center gap-2 text-muted">
          <span className="h-1.5 w-1.5 rounded-full" style={{ background: p.fill }} />
          {p.name}: <span className="text-ink tabular">{p.value.toLocaleString()}</span>
        </div>
      ))}
    </div>
  )
}

export default function Dashboard() {
  const { summary, topRoles, topLocationsIndia, topLocationsMalaysia } = skillbridgeData

  const chartData = topRoles.map((r) => ({ role: r.role, India: r.india, Malaysia: r.malaysia }))

  return (
    <div>
      <PageHeader
        eyebrow="Internship briefing · SkillBridge"
        title="One dataset, two tech job markets"
        description="India and Malaysia's software, data and security hiring, unified from live postings into a single schema — so a role, a skill or a salary band can be compared across both markets directly."
      >
        <Link
          to="/skill-gap"
          className="inline-flex items-center gap-1.5 rounded-md bg-signal px-4 py-2.5 text-sm font-medium text-canvas hover:opacity-90 transition-opacity"
        >
          Check your skill gap
          <IconArrowUpRight className="h-4 w-4" />
        </Link>
      </PageHeader>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard label="Unified listings" value={summary.totalJobs.toLocaleString()} sub="India + Malaysia, deduplicated" />
        <StatCard label="India listings" value={summary.indiaJobs.toLocaleString()} sub="Software-heavy market" accent="#EE9B3A" />
        <StatCard label="Malaysia listings" value={summary.malaysiaJobs.toLocaleString()} sub="Analyst & security-heavy" accent="#2FBF9F" />
        <StatCard label="Roles tracked" value={topRoles.length} sub="Classified by suggested role" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-4 mb-6">
        <Card className="lg:col-span-3 p-6">
          <div className="flex items-center justify-between mb-1">
            <h2 className="font-display font-semibold text-ink">Where the roles are</h2>
          </div>
          <p className="text-sm text-muted mb-5">Listings per role, split by country.</p>
          <div className="h-[280px] -ml-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} barGap={4} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
                <CartesianGrid stroke="#1B2740" vertical={false} />
                <XAxis
                  dataKey="role"
                  tick={{ fill: '#8C9AB8', fontSize: 11 }}
                  tickLine={false}
                  axisLine={{ stroke: '#22314F' }}
                  interval={0}
                  angle={-18}
                  textAnchor="end"
                  height={54}
                />
                <YAxis tick={{ fill: '#8C9AB8', fontSize: 11 }} tickLine={false} axisLine={false} width={40} />
                <Tooltip content={<ChartTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
                <Bar dataKey="India" fill="#EE9B3A" radius={[4, 4, 0, 0]} maxBarSize={22} />
                <Bar dataKey="Malaysia" fill="#2FBF9F" radius={[4, 4, 0, 0]} maxBarSize={22} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="lg:col-span-2 p-6">
          <h2 className="font-display font-semibold text-ink mb-1">Market balance</h2>
          <p className="text-sm text-muted mb-5">Share of tracked listings by country, for each role.</p>
          <div className="space-y-4">
            {topRoles.map((r) => (
              <div key={r.role}>
                <div className="text-sm text-ink mb-1.5">{r.role}</div>
                <SplitBar india={r.india} malaysia={r.malaysia} />
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-semibold text-ink">Top India hiring hubs</h2>
            <CountryPill country="India" size="sm" />
          </div>
          <ul className="space-y-3">
            {topLocationsIndia.map((l) => (
              <li key={l.location} className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2 text-muted">
                  <IconMapPin className="h-4 w-4 text-faint" />
                  {l.location}
                </span>
                <span className="text-ink tabular">{l.count.toLocaleString()}</span>
              </li>
            ))}
          </ul>
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2 className="font-display font-semibold text-ink">Top Malaysia hiring hubs</h2>
            <CountryPill country="Malaysia" size="sm" />
          </div>
          <ul className="space-y-3">
            {topLocationsMalaysia.map((l) => (
              <li key={l.location} className="flex items-center justify-between text-sm">
                <span className="flex items-center gap-2 text-muted">
                  <IconMapPin className="h-4 w-4 text-faint" />
                  {l.location}
                </span>
                <span className="text-ink tabular">{l.count.toLocaleString()}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>
    </div>
  )
}
