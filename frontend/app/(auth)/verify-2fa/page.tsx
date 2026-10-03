'use client'
import { Suspense, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/use-auth'
import { useToast } from '@/components/ui/toast'

function Verify2FAForm() {
  const [code, setCode] = useState('')
  const searchParams = useSearchParams()
  const tempToken = searchParams.get('token')
  const { login } = useAuth()
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!tempToken) return toast('Missing temporary token', 'error')
    try {
      const res = await api.auth.verify2FA({ temp_token: tempToken, totp_code: code })
      login(res.token)
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">Two-Factor Authentication</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent>
          <p className="text-sm text-slate-500 mb-4 text-center">Enter the 6-digit code from your authenticator app.</p>
          <Input type="text" value={code} onChange={e => setCode(e.target.value)} maxLength={6} required className="text-center text-2xl tracking-[0.5em] h-14" />
        </CardContent>
        <CardFooter>
          <Button type="submit" className="w-full">Verify</Button>
        </CardFooter>
      </form>
    </Card>
  )
}

export default function Verify2FA() {
  return (
    <Suspense fallback={<div className="text-center p-4">Loading verification...</div>}>
      <Verify2FAForm />
    </Suspense>
  )
}