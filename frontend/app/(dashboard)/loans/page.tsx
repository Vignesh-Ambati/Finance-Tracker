'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { LoanCard } from '@/components/loan-card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export default function Loans() {
  const [loans, setLoans] = useState<any[]>([])
  const toast = useToast()

  useEffect(() => {
    api.loans.getAll().then(setLoans).catch(err => toast(err.message, 'error'))
  }, [toast])

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Loans</h1>
        <Link href="/loans/new">
          <Button>Add New Loan</Button>
        </Link>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {loans.map(loan => (
          <LoanCard key={loan.id} loan={loan} />
        ))}
        {loans.length === 0 && <p className="text-slate-500 col-span-full">No loans found. Create one to get started.</p>}
      </div>
    </div>
  )
}