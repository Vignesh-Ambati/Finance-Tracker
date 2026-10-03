'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export default function NewLoan() {
  const router = useRouter()
  const toast = useToast()
  const [formData, setFormData] = useState({ borrower_id: '', principal: '', interest_rate: '', date_given: '' })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const loan = await api.loans.create({
        borrower_id: parseInt(formData.borrower_id),
        principal: parseFloat(formData.principal),
        interest_rate: parseFloat(formData.interest_rate),
        date_given: formData.date_given
      })
      toast('Loan created successfully', 'success')
      router.push(`/loans/${loan.id}`)
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Create New Loan</h1>
      <Card>
        <CardContent className="pt-6">
          <form onSubmit={handleSubmit} className="space-y-4">
            <Input label="Borrower ID" type="number" value={formData.borrower_id} onChange={e => setFormData({...formData, borrower_id: e.target.value})} required />
            <Input label="Principal Amount" type="number" step="0.01" value={formData.principal} onChange={e => setFormData({...formData, principal: e.target.value})} required />
            <Input label="Interest Rate (%)" type="number" step="0.01" value={formData.interest_rate} onChange={e => setFormData({...formData, interest_rate: e.target.value})} required />
            <Input label="Date Given" type="date" value={formData.date_given} onChange={e => setFormData({...formData, date_given: e.target.value})} required />
            <Button type="submit" className="w-full">Create Loan</Button>
          </form>
        </CardContent>
      </Card>
    </div>
  )
}