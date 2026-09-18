export default function MobileBar({ onOpen }) {
  return (
    <div className="lg:hidden sticky top-0 z-20 flex items-center gap-3 border-b border-hairline bg-canvas/90 backdrop-blur px-4 py-3">
      <button
        onClick={onOpen}
        aria-label="Open navigation"
        className="h-9 w-9 rounded-md border border-hairline flex items-center justify-center text-muted"
      >
        <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round">
          <path d="M4 7h16M4 12h16M4 17h16" />
        </svg>
      </button>
      <div className="h-7 w-7 rounded bg-gradient-to-br from-india to-malaysia flex items-center justify-center font-display font-bold text-canvas text-xs">
        SB
      </div>
      <span className="font-display font-semibold text-sm">SkillBridge</span>
    </div>
  )
}
