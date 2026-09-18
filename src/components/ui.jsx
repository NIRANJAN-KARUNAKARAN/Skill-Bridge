export function Card({ className = '', children }) {
  return (
    <div className={`rounded-lg border border-hairline bg-surface ${className}`}>
      {children}
    </div>
  )
}

export function StatCard({ label, value, sub, accent }) {
  return (
    <Card className="p-5">
      <div className="text-[13px] text-muted">{label}</div>
      <div className="mt-2 font-display text-[26px] font-semibold text-ink tabular leading-none">
        {value}
      </div>
      {sub && (
        <div className={`mt-2 text-xs ${accent ? '' : 'text-faint'}`} style={accent ? { color: accent } : undefined}>
          {sub}
        </div>
      )}
    </Card>
  )
}

export function CountryPill({ country, size = 'md' }) {
  const isIndia = country === 'India'
  const color = isIndia ? 'text-india' : 'text-malaysia'
  const bg = isIndia ? 'bg-india-soft' : 'bg-malaysia-soft'
  const border = isIndia ? 'border-india-line' : 'border-malaysia-line'
  const pad = size === 'sm' ? 'px-2 py-0.5 text-[11px]' : 'px-2.5 py-1 text-xs'
  return (
    <span className={`inline-flex items-center gap-1.5 rounded-full border ${border} ${bg} ${color} ${pad} font-medium`}>
      <span className={`h-1.5 w-1.5 rounded-full ${isIndia ? 'bg-india' : 'bg-malaysia'}`} />
      {country}
    </span>
  )
}

// A horizontal split bar: India value on the left (warm), Malaysia on the right (teal),
// proportional to their share of the total. Used to make every comparison read as one
// shape rather than two separate charts.
export function SplitBar({ india, malaysia, labelIndia = 'India', labelMalaysia = 'Malaysia', height = 'h-2.5' }) {
  const total = india + malaysia || 1
  const indiaPct = (india / total) * 100
  const malaysiaPct = 100 - indiaPct
  return (
    <div>
      <div className={`flex w-full overflow-hidden rounded-full ${height} bg-elevated`}>
        <div className="bg-india" style={{ width: `${indiaPct}%` }} />
        <div className="bg-malaysia" style={{ width: `${malaysiaPct}%` }} />
      </div>
      <div className="mt-1.5 flex justify-between text-[11px] text-faint tabular">
        <span>{labelIndia} · {india.toLocaleString()}</span>
        <span>{labelMalaysia} · {malaysia.toLocaleString()}</span>
      </div>
    </div>
  )
}

export function EmptyState({ icon: Icon, title, description }) {
  return (
    <div className="flex flex-col items-center justify-center text-center py-16 px-6">
      {Icon && (
        <div className="h-11 w-11 rounded-full border border-hairline flex items-center justify-center text-faint mb-4">
          <Icon className="h-5 w-5" />
        </div>
      )}
      <div className="text-ink font-medium">{title}</div>
      {description && <div className="mt-1.5 text-sm text-muted max-w-sm">{description}</div>}
    </div>
  )
}

export function SkillChip({ children, tone = 'neutral' }) {
  const tones = {
    neutral: 'border-hairline bg-elevated text-muted',
    have: 'border-malaysia-line bg-malaysia-soft text-malaysia',
    missing: 'border-india-line bg-india-soft text-india',
  }
  return (
    <span className={`inline-flex items-center gap-1 rounded-full border px-2.5 py-1 text-xs ${tones[tone]}`}>
      {children}
    </span>
  )
}
