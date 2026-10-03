'use client'
import { Bell, UserCircle } from 'lucide-react'
import { useAuth } from '@/hooks/use-auth'

export function Topbar() {
  const { user } = useAuth();
  return (
    <header className="h-16 border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-950 flex items-center justify-between px-6 shrink-0">
      <h2 className="text-lg font-semibold text-slate-800 dark:text-slate-100">Finance Tracker</h2>
      <div className="flex items-center gap-4">
        <button className="relative p-2 text-slate-600 hover:bg-slate-100 rounded-full dark:text-slate-300 dark:hover:bg-slate-800">
          <Bell className="h-5 w-5" />
          <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-red-500"></span>
        </button>
        <div className="flex items-center gap-2">
          <UserCircle className="h-8 w-8 text-slate-400" />
          <span className="text-sm font-medium">{user?.username || 'User'}</span>
        </div>
      </div>
    </header>
  )
}