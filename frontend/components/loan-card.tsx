import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { formatCurrency, formatDate } from '@/lib/utils'

export function LoanCard({ loan }: { loan: any }) {
  return (
    <Link href={`/loans/${loan.id}`}>
      <Card className="hover:border-blue-500 transition-colors cursor-pointer h-full">
        <CardHeader className="pb-2">
          <div className="flex justify-between items-start">
            <CardTitle className="text-lg">{loan.borrower?.name || 'Unknown'}</CardTitle>
            <Badge variant={loan.status === 'active' ? 'success' : loan.status === 'closed' ? 'secondary' : 'destructive'}>
              {loan.status}
            </Badge>
          </div>
        </CardHeader>
        <CardContent className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Principal</span>
            <span className="font-semibold">{formatCurrency(loan.principal)}</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Rate</span>
            <span className="font-semibold">{loan.interest_rate}%</span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-slate-500">Given on</span>
            <span>{loan.date_given ? formatDate(loan.date_given) : '-'}</span>
          </div>
        </CardContent>
      </Card>
    </Link>
  )
}