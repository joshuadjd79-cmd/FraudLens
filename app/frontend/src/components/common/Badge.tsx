import React from 'react';

interface BadgeProps {
  children: React.ReactNode;
  variant?: 'danger' | 'warning' | 'success' | 'info' | 'neutral' | 'purple';
  size?: 'sm' | 'md';
}

export const Badge: React.FC<BadgeProps> = ({ children, variant = 'neutral', size = 'sm' }) => {
  const variantStyles = {
    danger: 'bg-rose-500/15 text-rose-400 border border-rose-500/30',
    warning: 'bg-amber-500/15 text-amber-400 border border-amber-500/30',
    success: 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30',
    info: 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30',
    purple: 'bg-purple-500/15 text-purple-400 border border-purple-500/30',
    neutral: 'bg-slate-700/30 text-slate-300 border border-slate-700/50',
  };

  const sizeStyles = {
    sm: 'text-xs px-2 py-0.5 rounded-full font-medium',
    md: 'text-xs px-2.5 py-1 rounded-full font-semibold',
  };

  return (
    <span className={`inline-flex items-center gap-1 tracking-wide uppercase ${variantStyles[variant]} ${sizeStyles[size]}`}>
      {children}
    </span>
  );
};

export const SeverityBadge: React.FC<{ severity: string }> = ({ severity }) => {
  switch (severity?.toUpperCase()) {
    case 'CRITICAL':
      return <Badge variant="danger">Critical</Badge>;
    case 'HIGH':
      return <Badge variant="warning">High</Badge>;
    case 'MEDIUM':
      return <Badge variant="info">Medium</Badge>;
    case 'LOW':
      return <Badge variant="success">Low</Badge>;
    default:
      return <Badge variant="neutral">{severity}</Badge>;
  }
};

export const StatusBadge: React.FC<{ status: string }> = ({ status }) => {
  switch (status?.toUpperCase()) {
    case 'FLAGGED':
      return <Badge variant="danger">Flagged</Badge>;
    case 'COMPLETED':
      return <Badge variant="success">Completed</Badge>;
    case 'PENDING':
      return <Badge variant="warning">Pending</Badge>;
    case 'FAILED':
      return <Badge variant="neutral">Failed</Badge>;
    case 'OPEN':
      return <Badge variant="warning">Open Case</Badge>;
    case 'UNDER REVIEW':
      return <Badge variant="info">Under Review</Badge>;
    case 'CLOSED':
      return <Badge variant="success">Closed</Badge>;
    case 'ESCALATED':
      return <Badge variant="purple">Escalated</Badge>;
    default:
      return <Badge variant="neutral">{status}</Badge>;
  }
};
