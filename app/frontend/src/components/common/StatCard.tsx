import React from 'react';
import { LucideIcon } from 'lucide-react';

interface StatCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  icon: LucideIcon;
  variant?: 'cyan' | 'blue' | 'rose' | 'amber' | 'emerald' | 'violet';
  trend?: {
    value: string;
    isPositive?: boolean;
  };
  onClick?: () => void;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  subtitle,
  icon: Icon,
  variant = 'cyan',
  trend,
  onClick,
}) => {
  const variantStyles = {
    cyan: {
      bg: 'bg-cyan-500/10',
      border: 'hover:border-cyan-500/40',
      iconColor: 'text-cyan-400',
      glow: 'group-hover:shadow-[0_0_20px_-5px_rgba(6,182,212,0.3)]',
    },
    blue: {
      bg: 'bg-blue-500/10',
      border: 'hover:border-blue-500/40',
      iconColor: 'text-blue-400',
      glow: 'group-hover:shadow-[0_0_20px_-5px_rgba(59,130,246,0.3)]',
    },
    rose: {
      bg: 'bg-rose-500/10',
      border: 'hover:border-rose-500/40',
      iconColor: 'text-rose-400',
      glow: 'group-hover:shadow-[0_0_20px_-5px_rgba(244,63,94,0.3)]',
    },
    amber: {
      bg: 'bg-amber-500/10',
      border: 'hover:border-amber-500/40',
      iconColor: 'text-amber-400',
      glow: 'group-hover:shadow-[0_0_20px_-5px_rgba(245,158,11,0.3)]',
    },
    emerald: {
      bg: 'bg-emerald-500/10',
      border: 'hover:border-emerald-500/40',
      iconColor: 'text-emerald-400',
      glow: 'group-hover:shadow-[0_0_20px_-5px_rgba(16,185,129,0.3)]',
    },
    violet: {
      bg: 'bg-violet-500/10',
      border: 'hover:border-violet-500/40',
      iconColor: 'text-violet-400',
      glow: 'group-hover:shadow-[0_0_20px_-5px_rgba(139,92,246,0.3)]',
    },
  };

  const style = variantStyles[variant];

  // Dynamic font sizing and truncation to prevent overlapping on long numbers
  const valueStr = typeof value === 'string' ? value : String(value);
  const isExtraLong = valueStr.length > 15;
  const isLong = valueStr.length > 11;

  const fontSizeClass = isExtraLong
    ? 'text-base sm:text-lg lg:text-xl'
    : isLong
    ? 'text-lg sm:text-xl lg:text-2xl'
    : 'text-2xl';

  return (
    <div
      onClick={onClick}
      className={`group relative p-5 rounded-xl bg-slate-900/90 border border-slate-800 transition-all duration-300 overflow-hidden ${style.border} ${style.glow} ${
        onClick ? 'cursor-pointer hover:-translate-y-0.5' : ''
      }`}
    >
      <div className="flex items-start justify-between gap-3 min-w-0">
        <div className="min-w-0 flex-1 overflow-hidden">
          <p className="text-xs font-medium uppercase tracking-wider text-slate-400 truncate">{title}</p>
          <h3
            className={`mt-2 font-bold tracking-tight text-white font-mono truncate ${fontSizeClass}`}
            title={valueStr}
          >
            {value}
          </h3>
          {subtitle && (
            <p className="mt-1 text-xs text-slate-500 truncate" title={subtitle}>
              {subtitle}
            </p>
          )}
          {trend && (
            <p className="mt-2 flex items-center gap-1 text-xs font-medium truncate">
              <span className={trend.isPositive ? 'text-emerald-400' : 'text-rose-400'}>
                {trend.value}
              </span>
              <span className="text-slate-500 truncate">vs historical baseline</span>
            </p>
          )}
        </div>
        <div className={`p-3 rounded-lg ${style.bg} border border-white/5 flex-shrink-0`}>
          <Icon className={`w-5 h-5 ${style.iconColor}`} />
        </div>
      </div>
    </div>
  );
};
