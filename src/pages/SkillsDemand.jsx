import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { skillbridgeData } from '../data/skillbridgeData'
import PageHeader from '../components/PageHeader'
import { Card, CountryPill } from '../components/ui'

function SkillTooltip({ active, payload }) {
  if (!active || !payload?.length) return null
  const p = payload[0]
  return (
    <div className="rounded-md border border-hairline bg-elevated px-3 py-2 text-xs shadow-lg">
      <span className="text-ink">{p.payload.skill}</span>
      <span className="text-muted"> · {p.value.toLocaleString()} listings</span>
    </div>
  )
}

function SkillsChart({ data, color }) {
  const rows = [...data].reverse()
  return (
    <div style={{ height: Math.max(280, rows.length * 30) }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart data={rows} layout="vertical" margin={{ top: 4, right: 24, left: 0, bottom: 4 }}>
          <CartesianGrid stroke="#1B2740" horizontal={false} />
          <XAxis type="number" tick={{ fill: '#8C9AB8', fontSize: 11 }} tickLine={false} axisLine={{ stroke: '#22314F' }} />
          <YAxis
            type="category"
            dataKey="skill"
            tick={{ fill: '#EEF2FA', fontSize: 12.5 }}
            tickLine={false}
            axisLine={false}
            width={150}
          />
          <Tooltip content={<SkillTooltip />} cursor={{ fill: 'rgba(255,255,255,0.03)' }} />
          <Bar dataKey="count" fill={color} radius={[0, 4, 4, 0]} maxBarSize={16} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}

export default function SkillsDemand() {
  const { topSkillsIndia, topSkillsMalaysia } = skillbridgeData

  return (
    <div>
      <PageHeader
        eyebrow="Skills demand"
        title="What each market is actually hiring for"
        description="Skill and keyword frequency extracted from listing text and tags — the raw signal behind every role and recommendation in SkillBridge."
      />

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        <Card className="p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display font-semibold text-ink">India</h2>
            <CountryPill country="India" size="sm" />
          </div>
          <SkillsChart data={topSkillsIndia} color="#EE9B3A" />
        </Card>

        <Card className="p-6">
          <div className="flex items-center justify-between mb-5">
            <h2 className="font-display font-semibold text-ink">Malaysia</h2>
            <CountryPill country="Malaysia" size="sm" />
          </div>
          <SkillsChart data={topSkillsMalaysia} color="#2FBF9F" />
        </Card>
      </div>

      <Card className="p-6 mt-4">
        <h2 className="font-display font-semibold text-ink mb-2">Reading the two lists</h2>
        <p className="text-sm text-muted leading-relaxed max-w-2xl">
          India's postings skew toward named engineering stacks — Java, Spring Boot, React,
          microservices — reflecting a software-development-heavy listing pool. Malaysia's
          postings carry more category and employment-type tags alongside named skills, which is
          why broader labels sit higher in that list. Both are shown as extracted, so the gap
          between them is itself a data point about how each market's postings are written.
        </p>
      </Card>
    </div>
  )
}
