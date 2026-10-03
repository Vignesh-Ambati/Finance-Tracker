'use client'
import { useState } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardHeader, CardTitle, CardContent, CardFooter } from '@/components/ui/card'
import { api } from '@/lib/api'
import { useAuth } from '@/hooks/use-auth'
import { useToast } from '@/components/ui/toast'

export default function Register() {
  const [formData, setFormData] = useState({ username: '', email: '', password: '', confirmPassword: '', phone: '' })
  const { login } = useAuth()
  const toast = useToast()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (formData.password !== formData.confirmPassword) {
      toast("Passwords don't match", 'error')
      return
    }
    try {
      const res = await api.auth.register({
        username: formData.username,
        email: formData.email,
        password: formData.password,
        phone: formData.phone
      })
      login(res.token)
    } catch (err: any) {
      toast(err.message, 'error')
    }
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-center text-2xl">Create Account</CardTitle>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          <Input label="Username" value={formData.username} onChange={e => setFormData({...formData, username: e.target.value})} required />
          <Input label="Email" type="email" value={formData.email} onChange={e => setFormData({...formData, email: e.target.value})} required />
          <Input label="Phone (Optional)" value={formData.phone} onChange={e => setFormData({...formData, phone: e.target.value})} />
          <Input label="Password" type="password" value={formData.password} onChange={e => setFormData({...formData, password: e.target.value})} required />
          <Input label="Confirm Password" type="password" value={formData.confirmPassword} onChange={e => setFormData({...formData, confirmPassword: e.target.value})} required />
        </CardContent>
        <CardFooter className="flex flex-col gap-4">
          <Button type="submit" className="w-full">Register</Button>
          <div className="text-center text-sm text-slate-500">
            Already have an account? <Link href="/login" className="text-blue-600 hover:underline">Sign In</Link>
          </div>
        </CardFooter>
      </form>
    </Card>
  )
}