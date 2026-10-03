'use client'
import { useEffect, useState } from 'react'
import { StatsCards } from '@/components/stats-cards'
import { LoanCard } from '@/components/loan-card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null)
  const [loans, setLoans] = useState<any[]>([])
  const toast = useToast()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.loans.getAll()
        const loanList = Array.isArray(res) ? res : []
        setLoans(loanList.slice(0, 5))
        setStats({
          totalOutstanding: loanList.reduce((acc: number, l: any) => acc + (l.status === 'active' ? (l.principal || l.principal_amount || 0) : 0), 0),
          activeLoans: loanList.filter((l: any) => l.status === 'active').length,
          interestEarned: 0,
          pendingCollections: 0
        })
      } catch (err: any) {
        toast(err.message, 'error')
      }
    }
    fetchData()
  }, [toast])

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      <StatsCards stats={stats} />
      <div>
        <h2 className="text-xl font-semibold mb-4">Recent Loans</h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {loans.map(loan => (
            <LoanCard key={loan.id} loan={loan} />
          ))}
          {loans.length === 0 && <p className="text-slate-500">No active loans found.</p>}
        </div>
      </div>
    </div>
  )
}