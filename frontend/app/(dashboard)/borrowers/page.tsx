'use client'
import { useEffect, useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export default function Borrowers() {
  const [borrowers, setBorrowers] = useState<any[]>([])
  const toast = useToast()

  useEffect(() => {
    api.borrowers.getAll().then(setBorrowers).catch(err => toast(err.message, 'error'))
  }, [toast])

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Borrowers</h1>
        <Button>Add Borrower</Button>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {borrowers.map(b => (
          <Link key={b.id} href={`/borrowers/${b.id}`}>
            <Card className="hover:border-blue-500 cursor-pointer h-full">
              <CardHeader className="pb-2"><CardTitle className="text-xl">{b.name}</CardTitle></CardHeader>
              <CardContent className="space-y-1 text-sm text-slate-600">
                <p>Email: <span className="font-medium text-slate-900">{b.email}</span></p>
                <p>Phone: <span className="font-medium text-slate-900">{b.phone || '-'}</span></p>
              </CardContent>
            </Card>
          </Link>
        ))}
        {borrowers.length === 0 && <p className="text-slate-500 col-span-full">No borrowers found.</p>}
      </div>
    </div>
  )
}