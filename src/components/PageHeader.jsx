export default function PageHeader({ eyebrow, title, description, children }) {
  return (
    <div className="flex flex-col gap-4 lg:flex-row lg:items-end lg:justify-between mb-8">
      <div className="max-w-2xl">
        {eyebrow && <div className="text-sm text-signal mb-1.5">{eyebrow}</div>}
        <h1 className="text-2xl lg:text-[28px] font-semibold text-ink">{title}</h1>
        {description && <p className="mt-2 text-[15px] leading-relaxed text-muted">{description}</p>}
      </div>
      {children && <div className="shrink-0">{children}</div>}
    </div>
  )
}
