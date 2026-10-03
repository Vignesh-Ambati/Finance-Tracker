'use client'
import { useEffect, useState } from 'react'
import { Card, CardContent } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { api } from '@/lib/api'
import { useToast } from '@/components/ui/toast'
import { Bell, Check } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function Notifications() {
  const [notifs, setNotifs] = useState<any[]>([])
  const toast = useToast()

  const fetchNotifs = () => api.notifications.getAll().then(setNotifs).catch(err => toast(err.message, 'error'))

  useEffect(() => { fetchNotifs() }, [])

  const markAll = async () => {
    try {
      await api.notifications.markAllRead()
      fetchNotifs()
    } catch (err: any) { toast(err.message, 'error') }
  }

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold">Notifications</h1>
        {notifs.some(n => !n.is_read) && (
          <Button onClick={markAll} variant="outline" size="sm">Mark all as read</Button>
        )}
      </div>
      <div className="space-y-3">
        {notifs.map(n => (
          <Card key={n.id} className={cn("transition-all", n.is_read ? 'opacity-60 bg-slate-50' : 'border-blue-200')}>
            <CardContent className="p-4 flex items-start gap-4">
              <div className="p-2 bg-blue-100 text-blue-600 rounded-full shrink-0"><Bell className="h-4 w-4" /></div>
              <div className="flex-1">
                <p className="font-semibold text-sm">{n.title}</p>
                <p className="text-sm text-slate-600 mt-1">{n.message}</p>
              </div>
              {!n.is_read && (
                <Button size="icon" variant="ghost" className="shrink-0 hover:bg-emerald-50 hover:text-emerald-600" onClick={() => api.notifications.markRead(n.id).then(fetchNotifs)}>
                  <Check className="h-4 w-4" />
                </Button>
              )}
            </CardContent>
          </Card>
        ))}
        {notifs.length === 0 && <p className="text-center text-slate-500 mt-10 p-8 border border-dashed rounded-lg">No notifications yet.</p>}
      </div>
    </div>
  )
}