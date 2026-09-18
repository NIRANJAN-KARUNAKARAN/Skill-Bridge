import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { skillbridgeData } from '../data/skillbridgeData'
import PageHeader from '../components/PageHeader'
import { Card, SplitBar, CountryPill } from '../components/ui'

function SalaryTooltip({ active, payload, label, unit }) {
  if (!active || !payload?.length) return null
  return (
    <div className="rounded-md border border-hairline bg-elevated px-3 py-2 text-xs shadow-lg">
      <div className="text-ink font-medium mb-0.5">{label}</div>
      <div className="text-muted">
        Avg. midpoint · <span className="text-ink tabular">{payload[0].value.toLocaleString()} {unit}</span>
      </div>
    </div>
  )
}

function SalaryChart({ data, color, unit }) {
  return (
    <div className="h-[220px]">
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={data} margin={{ top: 4, right: 8, left: 0, bottom: 0 }}>
          <CartesianGrid stroke="#1B2740" vertical={false} />
          <XAxis dataKey="role" tick={{ fill: '#8C9AB8', fontSize: 10.5 }} tickLine={false} axisLine={{ stroke: '#22314F' }} interval={0} angle={-16} textAnchor="end" height={50} />
          <YAxis tick={{ fill: '#8C9AB8', fontSize: 11 }} tickLine={false} axisLine={false} width={44} />
          <Tooltip content={<SalaryTooltip unit={unit} />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
          <Bar dataKey="value" fill={color} radius={[4, 4, 0, 0]} maxBarSize={26} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function Comparison() {
  const { summary, topRoles, roleDetails } = skillbridgeData

  const indiaSalary = Object.entries(roleDetails)
    .filter(([, d]) => d.avgSalaryIndia)
    .map(([role, d]) => ({ role, value: Math.round(d.avgSalaryIndia / 100000) }))
    .sort((a, b) => b.value - a.value)

  const malaysiaSalary = Object.entries(roleDetails)
    .filter(([, d]) => d.avgSalaryMalaysia)
    .map(([role, d]) => ({ role, value: Math.round(d.avgSalaryMalaysia) }))
    .sort((a, b) => b.value - a.value)

  return (
    <div>
      <PageHeader
        eyebrow="Market comparison"
        title="India and Malaysia, side by side"
        description="Headcount by role, and average advertised salary within each country's own currency — deliberately not converted to one number, since a cross-currency average would flatten real cost-of-living and market differences."
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
        <Card className="p-6">
          <div className="flex items-center gap-2 mb-1">
            <CountryPill country="India" />
            <span className="text-xs text-faint">Software-development-led market</span>
          </div>
          <div className="font-display text-3xl font-semibold text-ink mt-3 tabular">
            {summary.indiaJobs.toLocaleString()}
          </div>
          <div className="text-sm text-muted">listings in the unified dataset</div>
        </Card>
        <Card className="p-6">
          <div className="flex items-center gap-2 mb-1">
            <CountryPill country="Malaysia" />
            <span className="text-xs text-faint">Analyst- and security-led market</span>
          </div>
          <div className="font-display text-3xl font-semibold text-ink mt-3 tabular">
            {summary.malaysiaJobs.toLocaleString()}
          </div>
          <div className="text-sm text-muted">listings in the unified dataset</div>
        </Card>
      </div>

      <Card className="p-6 mb-6">
        <h2 className="font-display font-semibold text-ink mb-1">Headcount by role</h2>
        <p className="text-sm text-muted mb-5">Share of each role's listings coming from India vs Malaysia.</p>
        <div className="space-y-5">
          {topRoles.map((r) => (
            <div key={r.role}>
              <div className="flex items-baseline justify-between mb-1.5">
                <span className="text-sm text-ink">{r.role}</span>
                <span className="text-xs text-faint tabular">{r.total.toLocaleString()} total</span>
              </div>
              <SplitBar india={r.india} malaysia={r.malaysia} height="h-2" />
            </div>
          ))}
        </div>
      </Card>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="p-6">
          <div className="flex items-center justify-between mb-1">
            <h2 className="font-display font-semibold text-ink">India — avg. salary by role</h2>
            <CountryPill country="India" size="sm" />
          </div>
          <p className="text-sm text-muted mb-4">Midpoint of advertised range, in ₹ lakhs per annum.</p>
          <SalaryChart data={indiaSalary} color="#EE9B3A" unit="L / yr" />
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between mb-1">
            <h2 className="font-display font-semibold text-ink">Malaysia — avg. salary by role</h2>
            <CountryPill country="Malaysia" size="sm" />
          </div>
          <p className="text-sm text-muted mb-4">Midpoint of advertised range, in MYR per month.</p>
          <SalaryChart data={malaysiaSalary} color="#2FBF9F" unit="MYR / mo" />
        </Card>
      </div>
    </div>
  )
}
