'use client'
import { useEffect, useState } from 'react'
import { useParams, useRouter } from 'next/navigation'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { CollectionDialog } from '@/components/collection-dialog'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'
import { formatCurrency, formatDate } from '@/lib/utils'
import { ArrowLeft } from 'lucide-react'
import Link from 'next/link'

export default function LoanDetail() {
  const { id } = useParams()
  const router = useRouter()
  const [loan, setLoan] = useState<any>(null)
  const [showCollect, setShowCollect] = useState(false)
  const toast = useToast()

  const fetchLoan = async () => {
    try {
      const data = await api.loans.getById(id as string)
      setLoan(data)
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  useEffect(() => { fetchLoan() }, [id])

  if (!loan) return <div>Loading...</div>

  const borrowerName = loan.borrower?.name || loan.borrower_name || 'Unknown Borrower'
  const principalAmount = loan.principal ?? loan.principal_amount ?? 0

  return (
    <div className="space-y-6">
      <Link href="/loans" className="text-blue-600 hover:underline flex items-center gap-2 text-sm font-medium">
        <ArrowLeft className="h-4 w-4" /> Back to Loans
      </Link>
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold flex items-center gap-3">
          Loan Details
          <Badge variant={loan.status === 'active' ? 'success' : loan.status === 'closed' ? 'secondary' : 'destructive'} className="text-sm">
            {loan.status}
          </Badge>
        </h1>
        <div className="flex gap-2">
          {loan.status === 'active' && <Button onClick={() => setShowCollect(true)}>Collect Interest</Button>}
          {loan.status === 'active' && (
            <Button variant="outline" className="text-red-600 hover:text-red-700 hover:bg-red-50 border-red-200" onClick={() => api.loans.close(id as string).then(() => { toast('Loan closed', 'success'); fetchLoan(); })}>
              Close Loan
            </Button>
          )}
        </div>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Overview</CardTitle>
        </CardHeader>
        <CardContent className="grid grid-cols-2 md:grid-cols-4 gap-6">
          <div><p className="text-sm text-slate-500 mb-1">Borrower</p><p className="font-semibold text-lg">{borrowerName}</p></div>
          <div><p className="text-sm text-slate-500 mb-1">Principal</p><p className="font-semibold text-lg text-blue-600">{formatCurrency(principalAmount)}</p></div>
          <div><p className="text-sm text-slate-500 mb-1">Interest Rate</p><p className="font-semibold text-lg">{loan.interest_rate}%</p></div>
          <div><p className="text-sm text-slate-500 mb-1">Date Given</p><p className="font-semibold text-lg">{loan.date_given ? formatDate(loan.date_given) : '-'}</p></div>
        </CardContent>
      </Card>
      <CollectionDialog open={showCollect} onClose={() => setShowCollect(false)} loanId={id as string} onSuccess={fetchLoan} />
    </div>
  )
}