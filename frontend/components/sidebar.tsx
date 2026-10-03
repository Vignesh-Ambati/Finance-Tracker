'use client'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { LayoutDashboard, Banknote, Users, Bell, UserCircle, LogOut } from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'
import { cn } from '@/lib/utils'

export function Sidebar() {
  const pathname = usePathname();
  const { logout } = useAuth();
  
  const links = [
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/loans', label: 'Loans', icon: Banknote },
    { href: '/borrowers', label: 'Borrowers', icon: Users },
    { href: '/notifications', label: 'Notifications', icon: Bell },
    { href: '/profile', label: 'Profile', icon: UserCircle },
  ];

  return (
    <aside className="w-64 h-full border-r border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950 flex flex-col shrink-0">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-blue-600">FinanceTracker</h1>
      </div>
      <nav className="flex-1 px-4 space-y-2">
        {links.map((link) => {
          const Icon = link.icon;
          const isActive = pathname === link.href || pathname.startsWith(link.href + '/');
          return (
            <Link key={link.href} href={link.href} className={cn(
              "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
              isActive ? "bg-blue-50 text-blue-700 dark:bg-blue-900/50 dark:text-blue-300" : "text-slate-600 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-800"
            )}>
              <Icon className="h-5 w-5" />
              {link.label}
            </Link>
          )
        })}
      </nav>
      <div className="p-4 border-t border-slate-200 dark:border-slate-800">
        <button onClick={logout} className="flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm font-medium text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20">
          <LogOut className="h-5 w-5" />
          Logout
        </button>
      </div>
    </aside>
  )
}