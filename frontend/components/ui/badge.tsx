import * as React from "react"
import { cn } from "@/lib/utils"

export interface BadgeProps extends React.HTMLAttributes<HTMLDivElement> {
  variant?: 'default' | 'success' | 'warning' | 'destructive' | 'secondary';
}

export function Badge({ className, variant = "default", ...props }: BadgeProps) {
  return (
    <div className={cn(
      "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none",
      {
        'border-transparent bg-blue-100 text-blue-900': variant === 'default',
        'border-transparent bg-emerald-100 text-emerald-900': variant === 'success',
        'border-transparent bg-amber-100 text-amber-900': variant === 'warning',
        'border-transparent bg-red-100 text-red-900': variant === 'destructive',
        'border-slate-200 text-slate-950': variant === 'secondary',
      },
      className
    )} {...props} />
  )
}