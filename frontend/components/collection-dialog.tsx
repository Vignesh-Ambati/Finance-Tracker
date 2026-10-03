'use client'
import { useState } from 'react'
import { Dialog } from '@/components/ui/dialog'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export function CollectionDialog({ loanId, open, onClose, onSuccess }: { loanId: string, open: boolean, onClose: () => void, onSuccess: () => void }) {
  const [amount, setAmount] = useState('')
  const [date, setDate] = useState('')
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.loans.collectInterest(loanId, { amount: parseFloat(amount), date })
      toast('Interest collected successfully', 'success')
      onSuccess()
      onClose()
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <Dialog open={open} onClose={onClose} title="Record Interest Collection">
      <form onSubmit={handleSubmit} className="space-y-4">
        <Input label="Amount" type="number" step="0.01" value={amount} onChange={e => setAmount(e.target.value)} required />
        <Input label="Collection Date" type="date" value={date} onChange={e => setDate(e.target.value)} required />
        <div className="flex justify-end gap-2 mt-4">
          <Button type="button" variant="outline" onClick={onClose}>Cancel</Button>
          <Button type="submit">Save Collection</Button>
        </div>
      </form>
    </Dialog>
  )
}