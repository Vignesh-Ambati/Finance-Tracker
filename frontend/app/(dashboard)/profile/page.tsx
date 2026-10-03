'use client'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { useAuth } from '@/hooks/use-auth'

export default function Profile() {
  const { user } = useAuth()
  const router = useRouter()
  
  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <h1 className="text-3xl font-bold">Profile</h1>
      <Card>
        <CardHeader><CardTitle>Account Details</CardTitle></CardHeader>
        <CardContent className="space-y-4">
          <Input label="Username" value={user?.username || ''} disabled />
          <Input label="Email" value={user?.email || ''} disabled />
        </CardContent>
      </Card>
      <Card>
        <CardHeader><CardTitle>Security</CardTitle></CardHeader>
        <CardContent className="space-y-6">
          <div>
            <p className="text-sm font-medium mb-2">Two-Factor Authentication</p>
            {user?.has_2fa ? (
              <Button variant="destructive">Disable 2FA</Button>
            ) : (
              <Button onClick={() => router.push('/setup-2fa')}>Enable 2FA</Button>
            )}
          </div>
          <div className="pt-4 border-t border-slate-100">
            <p className="text-sm font-medium mb-2">Password</p>
            <Button variant="outline">Change Password (Coming Soon)</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}