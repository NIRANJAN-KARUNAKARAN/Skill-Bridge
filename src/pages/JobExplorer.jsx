import { useMemo, useState } from 'react'
import { skillbridgeData } from '../data/skillbridgeData'
import PageHeader from '../components/PageHeader'
import { Card, CountryPill, EmptyState, SkillChip } from '../components/ui'
import { IconSearch, IconMapPin, IconBriefcase } from '../components/icons'

function formatSalary(job) {
  if (!job.minSalary || !job.maxSalary) return 'Not disclosed'
  const fmt = (n) =>
    job.currency === 'INR'
      ? `₹${(n / 100000).toFixed(1)}L`
      : `${job.currency} ${Math.round(n).toLocaleString()}`
  return `${fmt(job.minSalary)} – ${fmt(job.maxSalary)}`
}

export default function JobExplorer() {
  const { jobs, topRoles } = skillbridgeData
  const [query, setQuery] = useState('')
  const [country, setCountry] = useState('All')
  const [role, setRole] = useState('All')

  const roles = useMemo(() => ['All', ...topRoles.map((r) => r.role)], [topRoles])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return jobs.filter((j) => {
      if (country !== 'All' && j.country !== country) return false
      if (role !== 'All' && j.role !== role) return false
      if (q) {
        const hay = `${j.title} ${j.company} ${j.location} ${j.skills.join(' ')}`.toLowerCase()
        if (!hay.includes(q)) return false
      }
      return true
    })
  }, [jobs, query, country, role])

  return (
    <div>
      <PageHeader
        eyebrow="Job explorer"
        title="Browse live listings across both markets"
        description="Filter by country and role, or search a title, company, skill or city. Sampled from the unified India–Malaysia dataset."
      />

      <Card className="p-4 mb-5">
        <div className="flex flex-col lg:flex-row gap-3">
          <div className="flex-1 flex items-center gap-2 rounded-md border border-hairline bg-elevated px-3 py-2.5">
            <IconSearch className="h-4 w-4 text-faint shrink-0" />
            <input
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search title, company, skill, or city…"
              className="w-full bg-transparent text-sm text-ink placeholder:text-faint outline-none"
            />
          </div>

          <div className="flex gap-3">
            <select
              value={country}
              onChange={(e) => setCountry(e.target.value)}
              className="rounded-md border border-hairline bg-elevated px-3 py-2.5 text-sm text-ink outline-none"
            >
              <option value="All">Both countries</option>
              <option value="India">India</option>
              <option value="Malaysia">Malaysia</option>
            </select>

            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="rounded-md border border-hairline bg-elevated px-3 py-2.5 text-sm text-ink outline-none"
            >
              {roles.map((r) => (
                <option key={r} value={r}>
                  {r === 'All' ? 'All roles' : r}
                </option>
              ))}
            </select>
          </div>
        </div>
      </Card>

      <div className="text-xs text-faint mb-3">
        {filtered.length} of {jobs.length} sampled listings
      </div>

      {filtered.length === 0 ? (
        <Card>
          <EmptyState
            icon={IconSearch}
            title="No listings match those filters"
            description="Try a broader search term, or reset the country and role filters."
          />
        </Card>
      ) : (
        <div className="space-y-3">
          {filtered.map((job, i) => (
            <Card key={i} className="p-5">
              <div className="flex flex-col lg:flex-row lg:items-start lg:justify-between gap-3">
                <div className="min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <h3 className="font-medium text-ink">{job.title}</h3>
                    <CountryPill country={job.country} size="sm" />
                  </div>
                  <div className="mt-1 flex items-center gap-3 text-sm text-muted">
                    <span className="flex items-center gap-1.5">
                      <IconBriefcase className="h-3.5 w-3.5 text-faint" />
                      {job.company}
                    </span>
                    <span className="flex items-center gap-1.5">
                      <IconMapPin className="h-3.5 w-3.5 text-faint" />
                      {job.location}
                    </span>
                  </div>
                  {job.skills.length > 0 && (
                    <div className="mt-3 flex flex-wrap gap-1.5">
                      {job.skills.map((s) => (
                        <SkillChip key={s}>{s}</SkillChip>
                      ))}
                    </div>
                  )}
                </div>

                <div className="shrink-0 text-left lg:text-right">
                  <div className="text-sm font-medium text-ink tabular">{formatSalary(job)}</div>
                  <div className="text-xs text-faint mt-0.5">{job.experience || 'Experience unspecified'}</div>
                  <div className="text-xs text-faint mt-0.5">{job.role}</div>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
