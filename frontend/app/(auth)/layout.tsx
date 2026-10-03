export default function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-br from-slate-100 to-blue-50 p-4 dark:from-slate-900 dark:to-slate-800">
      <div className="w-full max-w-md">
        {children}
      </div>
    </div>
  )
}