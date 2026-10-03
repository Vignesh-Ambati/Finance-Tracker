import './globals.css'
import type { Metadata } from 'next'
import { AuthProvider } from '@/providers/auth-provider'
import { ToastProvider } from '@/components/ui/toast'

export const metadata: Metadata = {
  title: 'Finance Tracker',
  description: 'Track your personal finance and loans',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="antialiased min-h-screen text-slate-900 bg-slate-50">
        <ToastProvider>
          <AuthProvider>
            {children}
          </AuthProvider>
        </ToastProvider>
      </body>
    </html>
  )
}