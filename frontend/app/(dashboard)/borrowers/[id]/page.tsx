'use client'
export const runtime = 'edge'
import { useEffect, useState } from 'react'
import { useParams } from 'next/navigation'
import Link from 'next/link'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'
import { ArrowLeft } from 'lucide-react'

export default function BorrowerDetail() {
  const { id } = useParams()
  const [borrower, setBorrower] = useState<any>(null)
  const toast = useToast()

  useEffect(() => {
    api.borrowers.getById(id as string).then(setBorrower).catch(err => toast(err.message, 'error'))
  }, [id, toast])

  if (!borrower) return <div>Loading...</div>

  return (
    <div className="space-y-6">
      <Link href="/borrowers" className="text-blue-600 hover:underline flex items-center gap-2 text-sm font-medium">
        <ArrowLeft className="h-4 w-4" /> Back to Borrowers
      </Link>
      <h1 className="text-3xl font-bold">Borrower Details</h1>
      <Card>
        <CardHeader><CardTitle>{borrower.name}</CardTitle></CardHeader>
        <CardContent className="space-y-2">
          <p className="text-sm text-slate-500">Email: <span className="font-medium text-slate-900">{borrower.email}</span></p>
          <p className="text-sm text-slate-500">Phone: <span className="font-medium text-slate-900">{borrower.phone || '-'}</span></p>
        </CardContent>
      </Card>
    </div>
  )
}