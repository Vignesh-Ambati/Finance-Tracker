'use client'
import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'

export default function Setup2FA() {
  const [setupData, setSetupData] = useState<any>(null)
  const [code, setCode] = useState('')
  const router = useRouter()
  const toast = useToast()

  useEffect(() => {
    api.auth.setup2FA().then(setSetupData).catch(err => toast(err.message, 'error'))
  }, [toast])

  const handleVerify = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await api.auth.enable2FA(code)
      toast('2FA Enabled successfully', 'success')
      router.push('/dashboard')
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center">Setup Two-Factor Authentication</CardTitle>
      </CardHeader>
      {setupData ? (
        <form onSubmit={handleVerify}>
          <CardContent className="space-y-6 flex flex-col items-center">
            <div className="bg-white p-2 rounded-lg border border-slate-200">
              <img src={`data:image/png;base64,${setupData.qr_code}`} alt="2FA QR Code" className="w-48 h-48" />
            </div>
            <p className="text-sm font-mono bg-slate-100 p-2 rounded w-full text-center">{setupData.secret}</p>
            <Input label="Verification Code" value={code} onChange={e => setCode(e.target.value)} maxLength={6} required className="text-center text-lg tracking-[0.5em] h-12" />
          </CardContent>
          <CardFooter>
            <Button type="submit" className="w-full">Verify & Enable</Button>
          </CardFooter>
        </form>
      ) : (
        <CardContent className="text-center py-8">Loading setup data...</CardContent>
      )}
    </Card>
  )
}