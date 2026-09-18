import { useMemo, useState } from 'react'
import { RadialBarChart, RadialBar, PolarAngleAxis } from 'recharts'
import { skillbridgeData } from '../data/skillbridgeData'
import PageHeader from '../components/PageHeader'
import { Card, CountryPill, SkillChip } from '../components/ui'
import { IconTarget, IconCheck } from '../components/icons'

function normalize(s) {
  return s.trim().toLowerCase()
}

function MatchGauge({ pct, color }) {
  const data = [{ value: pct, fill: color }]
  return (
    <div className="relative h-40 w-40 mx-auto">
      <RadialBarChart
        width={160}
        height={160}
        cx="50%"
        cy="50%"
        innerRadius={58}
        outerRadius={76}
        barSize={12}
        data={data}
        startAngle={90}
        endAngle={-270}
      >
        <PolarAngleAxis type="number" domain={[0, 100]} angleAxisId={0} tick={false} />
        <RadialBar background={{ fill: '#1B2740' }} dataKey="value" cornerRadius={8} angleAxisId={0} />
      </RadialBarChart>
      <div className="absolute inset-0 flex flex-col items-center justify-center">
        <div className="font-display text-2xl font-semibold text-ink tabular">{pct}%</div>
        <div className="text-[11px] text-faint">match</div>
      </div>
    </div>
  )
}

export default function SkillGap() {
  const { roleDetails, topRoles } = skillbridgeData
  const roleNames = topRoles.map((r) => r.role)

  const [role, setRole] = useState(roleNames[0])
  const [country, setCountry] = useState('India')
  const [skillsInput, setSkillsInput] = useState('')
  const [submitted, setSubmitted] = useState(false)

  const required = roleDetails[role]?.requiredSkills ?? []

  const userSkills = useMemo(
    () =>
      skillsInput
        .split(',')
        .map((s) => s.trim())
        .filter(Boolean),
    [skillsInput],
  )
  const userSkillsNorm = useMemo(() => new Set(userSkills.map(normalize)), [userSkills])

  const have = required.filter((s) => userSkillsNorm.has(normalize(s)))
  const missing = required.filter((s) => !userSkillsNorm.has(normalize(s)))
  const pct = required.length ? Math.round((have.length / required.length) * 100) : 0

  const detail = roleDetails[role]
  const avgSalary =
    country === 'India'
      ? detail?.avgSalaryIndia
        ? `₹${(detail.avgSalaryIndia / 100000).toFixed(1)}L / yr avg.`
        : 'Not enough salary data'
      : detail?.avgSalaryMalaysia
      ? `MYR ${Math.round(detail.avgSalaryMalaysia).toLocaleString()} / mo avg.`
      : 'Not enough salary data'

  const openings = country === 'India' ? detail?.indiaJobs ?? 0 : detail?.malaysiaJobs ?? 0
  const gaugeColor = country === 'India' ? '#EE9B3A' : '#2FBF9F'

  return (
    <div>
      <PageHeader
        eyebrow="Skill-gap checker"
        title="How close are you to a target role?"
        description="Pick a role and market, list what you already know, and see the gap against skills pulled from real listings — with what to prioritize learning next."
      />

      <div className="grid grid-cols-1 lg:grid-cols-5 gap-4">
        <Card className="lg:col-span-2 p-6 h-fit">
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-muted mb-1.5">Target role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full rounded-md border border-hairline bg-elevated px-3 py-2.5 text-sm text-ink outline-none"
              >
                {roleNames.map((r) => (
                  <option key={r} value={r}>
                    {r}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm text-muted mb-1.5">Target market</label>
              <div className="flex gap-2">
                {['India', 'Malaysia'].map((c) => (
                  <button
                    key={c}
                    onClick={() => setCountry(c)}
                    className={`flex-1 rounded-md border px-3 py-2.5 text-sm transition-colors ${
                      country === c
                        ? c === 'India'
                          ? 'border-india-line bg-india-soft text-india'
                          : 'border-malaysia-line bg-malaysia-soft text-malaysia'
                        : 'border-hairline bg-elevated text-muted hover:text-ink'
                    }`}
                  >
                    {c}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm text-muted mb-1.5">Your skills</label>
              <textarea
                value={skillsInput}
                onChange={(e) => setSkillsInput(e.target.value)}
                placeholder="e.g. Python, SQL, AWS, Docker"
                rows={4}
                className="w-full rounded-md border border-hairline bg-elevated px-3 py-2.5 text-sm text-ink placeholder:text-faint outline-none resize-none"
              />
              <div className="mt-1.5 text-[11px] text-faint">Comma-separated. Matching isn't case-sensitive.</div>
            </div>

            <button
              onClick={() => setSubmitted(true)}
              className="w-full rounded-md bg-signal px-4 py-2.5 text-sm font-medium text-canvas hover:opacity-90 transition-opacity"
            >
              View match score
            </button>
          </div>
        </Card>

        <div className="lg:col-span-3 space-y-4">
          <Card className="p-6">
            <div className="flex flex-col sm:flex-row items-center gap-6">
              <MatchGauge pct={submitted ? pct : 0} color={gaugeColor} />
              <div className="flex-1 w-full">
                <div className="flex items-center gap-2 mb-1">
                  <h2 className="font-display font-semibold text-ink">{role}</h2>
                  <CountryPill country={country} size="sm" />
                </div>
                <p className="text-sm text-muted mb-4">
                  {submitted
                    ? `You match ${have.length} of ${required.length} skills most commonly listed for this role in ${country}.`
                    : 'Enter your skills and view your match score to see the breakdown here.'}
                </p>
                <div className="grid grid-cols-2 gap-3">
                  <div className="rounded-md border border-hairline bg-elevated px-3 py-2.5">
                    <div className="text-[11px] text-faint">Open listings</div>
                    <div className="text-ink font-medium tabular">{openings.toLocaleString()}</div>
                  </div>
                  <div className="rounded-md border border-hairline bg-elevated px-3 py-2.5">
                    <div className="text-[11px] text-faint">Avg. advertised pay</div>
                    <div className="text-ink font-medium tabular">{avgSalary}</div>
                  </div>
                </div>
              </div>
            </div>
          </Card>

          {submitted && (
            <>
              <Card className="p-6">
                <div className="flex items-center gap-2 mb-4">
                  <IconCheck className="h-4 w-4 text-malaysia" />
                  <h3 className="font-medium text-ink">Skills you already have</h3>
                </div>
                {have.length ? (
                  <div className="flex flex-wrap gap-2">
                    {have.map((s) => (
                      <SkillChip key={s} tone="have">
                        {s}
                      </SkillChip>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted">None of your listed skills matched yet — try adding more, or check the spelling against common naming (e.g. "React.Js").</p>
                )}
              </Card>

              <Card className="p-6">
                <div className="flex items-center gap-2 mb-1">
                  <IconTarget className="h-4 w-4 text-india" />
                  <h3 className="font-medium text-ink">Recommended learning priorities</h3>
                </div>
                <p className="text-sm text-muted mb-4">Ordered by how often each skill appears in {role} listings.</p>
                {missing.length ? (
                  <div className="flex flex-wrap gap-2">
                    {missing.map((s) => (
                      <SkillChip key={s} tone="missing">
                        {s}
                      </SkillChip>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-muted">You cover every commonly listed skill for this role — nice place to be.</p>
                )}
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
