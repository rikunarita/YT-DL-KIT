import { LucideIcon } from 'lucide-react'
import { useTranslation } from '../i18n'

interface NavItem {
  label: string
  icon: LucideIcon
  page: string
}

interface SidebarProps {
  items: NavItem[]
  currentPage: string
  onPageChange: (page: string) => void
}

export default function Sidebar({ items, currentPage, onPageChange }: SidebarProps) {
  const { t } = useTranslation()

  return (
    <aside className="relative w-64 bg-slate-900 dark:bg-slate-950 text-white border-r border-slate-800">
      <div className="p-6">
        <h1 className="text-2xl font-bold tracking-tight">yt-dlp GUI</h1>
        <p className="text-sm text-slate-400 mt-1">{t('app.version', { version: '1.0.0' })}</p>
      </div>

      <nav className="mt-6 px-3 space-y-2">
        {items.map((item) => {
          const Icon = item.icon
          const isActive = currentPage === item.page

          return (
            <button
              key={item.page}
              onClick={() => onPageChange(item.page)}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-colors text-left ${
                isActive
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <Icon size={20} />
              <span>{item.label}</span>
            </button>
          )
        })}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-6 border-t border-slate-800">
        <p className="text-xs text-slate-500">{t('footer.copyright')}</p>
      </div>
    </aside>
  )
}
