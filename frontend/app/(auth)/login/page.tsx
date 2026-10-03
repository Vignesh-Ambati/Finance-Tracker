'use client'
import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/use-auth'
import { useToast } from '@/components/ui/toast'

export default function Login() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()
  const { login } = useAuth()
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const res = await api.auth.login({ email, password })
      if (res.requires_2fa) {
        router.push(`/verify-2fa?token=${res.temp_token}`)
      } else {
        login(res.token)
      }
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center text-2xl text-blue-600">Finance Tracker</CardTitle>
        <p className="text-center text-sm text-slate-500">Sign in to your account</p>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <Input label="Email" type="email" value={email} onChange={e => setEmail(e.target.value)} required />
          <Input label="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} required />
          <div className="text-right">
            <Link href="/forgot-password" className="text-sm text-blue-600 hover:underline">Forgot password?</Link>
          </div>
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full">Sign In</Button>
          <div className="text-center text-sm text-slate-500">
            Don't have an account? <Link href="/register" className="text-blue-600 hover:underline">Register</Link>
          </div>
        </CardFooter>
      </form>
    </Card>
  )
}