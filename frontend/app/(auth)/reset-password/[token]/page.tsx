'use client'
import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export default function ResetPassword({ params }: { params: { token: string } }) {
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const router = useRouter()
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (password !== confirmPassword) return toast("Passwords don't match", 'error')
    try {
      await api.auth.resetPassword(params.token, password)
      toast('Password reset successfully', 'success')
      router.push('/login')
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">Set New Password</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <Input label="New Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          <Input label="Confirm New Password" type="password" value={confirmPassword} onChange={e => setConfirmPassword(e.target.value)} required />
        </CardContent>
        <CardFooter>
          <Button type="submit" className="w-full">Reset Password</Button>
        </CardFooter>
      </form>
    </Card>
  )
}