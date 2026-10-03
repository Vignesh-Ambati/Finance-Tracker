'use client'
import { useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export default function ForgotPassword() {
  const [email, setEmail] = useState('')
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.auth.forgotPassword(email)
      toast('Reset instructions sent to your email', 'success')
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">Reset Password</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent>
          <Input label="Email Address" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full">Send Instructions</Button>
          <div className="text-center text-sm text-slate-500">
            <Link href="/login" className="text-blue-600 hover:underline">Back to Login</Link>
          </div>
        </CardFooter>
      </form>
    </Card>
  )
}