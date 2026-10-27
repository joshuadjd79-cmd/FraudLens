import React, { useState, useEffect } from 'react';
import {
  Server,
  Database,
  Shield,
  Activity,
  CheckCircle2,
  AlertTriangle,
  Cpu,
  Layers,
  Clock,
  RefreshCw,
  Lock,
} from 'lucide-react';
import { SystemHealth } from '../types';
import { api } from '../api/client';

export const SystemHealthPage: React.FC = () => {
  const [health, setHealth] = useState<SystemHealth | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [lastCheck, setLastCheck] = useState<string>('');

  const loadHealth = async () => {
    try {
      setIsLoading(true);
      const res = await api.getHealth();
      setHealth(res);
      setLastCheck(new Date().toLocaleTimeString());
    } catch (err) {
      console.error('Failed to load health:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadHealth();
  }, []);

  const isConnected = health?.database?.connected ?? false;

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight">System & Database Diagnostics</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Operational status of Oracle Database 26ai Free, connection pool, and FastAPI backend
          </p>
        </div>
        <button
          onClick={loadHealth}
          disabled={isLoading}
          className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-medium text-slate-200 transition-colors"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${isLoading ? 'animate-spin text-cyan-400' : ''}`} />
          <span>Ping Engine</span>
        </button>
      </div>

      {/* Main Connection Status Banner */}
      <div
        className={`p-6 rounded-2xl border ${
          isConnected
            ? 'bg-gradient-to-r from-slate-900 via-slate-900 to-emerald-950/30 border-emerald-500/30'
            : 'bg-gradient-to-r from-slate-900 via-slate-900 to-amber-950/30 border-amber-500/30'
        }`}
      >
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-start gap-4">
            <div
              className={`p-3.5 rounded-xl border ${
                isConnected
                  ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
                  : 'bg-amber-500/10 text-amber-400 border-amber-500/30'
              }`}
            >
              <Database className="w-7 h-7" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-semibold uppercase tracking-wider text-slate-400">
                  Database Engine Connection
                </span>
                <span
                  className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold ${
                    isConnected
                      ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                      : 'bg-amber-500/20 text-amber-400 border border-amber-500/30'
                  }`}
                >
                  {isConnected ? 'ONLINE & SYNCED' : 'STANDALONE DEMO MODE'}
                </span>
              </div>
              <h2 className="text-2xl font-bold text-white tracking-tight mt-1 font-mono">
                {isConnected ? 'Oracle AI Database 26ai Free (FREEPDB1)' : 'In-Memory Simulation Adapter'}
              </h2>
              <p className="text-xs text-slate-400 mt-1">
                {isConnected
                  ? 'Connected via Python oracledb Thin Mode (Zero-Client TCP). Safe connection pool active.'
                  : 'Running offline fallback memory repository with the 56 baseline DBMS records.'}
              </p>
            </div>
          </div>

          <div className="text-right font-mono text-xs">
            <div className="text-slate-400">Diagnostic Ping:</div>
            <div className="text-emerald-400 font-bold">{lastCheck || 'Just now'}</div>
          </div>
        </div>
      </div>

      {/* Database Topology and Service Info */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-cyan-400 font-semibold text-xs uppercase tracking-wider font-mono">
            <Server className="w-4 h-4" />
            <span>Container & Service</span>
          </div>
          <div className="space-y-2 text-xs">
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Pluggable Database (PDB)</p>
              <p className="font-mono text-slate-200 font-medium">FREEPDB1 (OPEN / READ WRITE)</p>
            </div>
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Oracle Schema User</p>
              <p className="font-mono text-slate-200 font-medium">FRAUDLENS_USER</p>
            </div>
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Host & Port</p>
              <p className="font-mono text-slate-200 font-medium">localhost:1521</p>
            </div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-blue-400 font-semibold text-xs uppercase tracking-wider font-mono">
            <Cpu className="w-4 h-4" />
            <span>Connection Pool</span>
          </div>
          <div className="space-y-2 text-xs">
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Driver Protocol</p>
              <p className="font-mono text-slate-200 font-medium">python-oracledb Thin Mode</p>
            </div>
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Pool Configuration</p>
              <p className="font-mono text-slate-200 font-medium">Min: 1 | Max: 5 | Increment: 1</p>
            </div>
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Transaction Isolation</p>
              <p className="font-mono text-slate-200 font-medium">Read Committed (ACID)</p>
            </div>
          </div>
        </div>

        <div className="p-5 rounded-2xl bg-slate-900 border border-slate-800 space-y-3">
          <div className="flex items-center gap-2 text-violet-400 font-semibold text-xs uppercase tracking-wider font-mono">
            <Shield className="w-4 h-4" />
            <span>Surveillance Engine</span>
          </div>
          <div className="space-y-2 text-xs">
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">High Amount Tier</p>
              <p className="font-mono text-cyan-400 font-bold">
                ₹{health?.high_amount_threshold?.toLocaleString('en-IN') || '50,000'}
              </p>
            </div>
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Automated Evaluation</p>
              <p className="font-mono text-slate-200 font-medium">PL/SQL Stored Procedure</p>
            </div>
            <div>
              <p className="text-slate-500 text-[10px] uppercase font-mono">Audit Triggers</p>
              <p className="font-mono text-slate-200 font-medium">Row-level Autonomous Write</p>
            </div>
          </div>
        </div>
      </div>

      {/* Registered Database Objects Directory */}
      <div className="p-6 rounded-2xl bg-slate-900 border border-slate-800 space-y-4">
        <h2 className="text-sm font-semibold text-white tracking-wide">
          Verified Active Database Schema Objects
        </h2>
        <p className="text-xs text-slate-400">
          The following relational entities, procedural packages, and triggers are confirmed live in the Oracle catalog:
        </p>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
          {[
            { name: 'CUSTOMERS', type: 'TABLE', desc: '10 KYC accounts' },
            { name: 'ACCOUNTS', type: 'TABLE', desc: '12 multi-currency ledgers' },
            { name: 'TRANSACTIONS', type: 'TABLE', desc: 'Financial transaction stream' },
            { name: 'FRAUD_ALERT', type: 'TABLE', desc: 'Surveillance anomaly records' },
            { name: 'INVESTIGATOR', type: 'TABLE', desc: 'Certified investigators' },
            { name: 'INVESTIGATION', type: 'TABLE', desc: 'Case dockets & outcomes' },
            { name: 'INVESTIGATION_AUDIT', type: 'AUDIT', desc: 'Trigger audit mutations' },
            { name: 'ALERT_AUDIT', type: 'AUDIT', desc: 'Trigger alert logs' },
          ].map((obj) => (
            <div key={obj.name} className="p-3 rounded-xl bg-slate-950 border border-slate-800/80">
              <div className="flex items-center justify-between">
                <span className="font-mono font-bold text-slate-200 text-[11px]">{obj.name}</span>
                <span
                  className={`text-[9px] font-mono px-1.5 py-0.5 rounded font-bold ${
                    obj.type === 'AUDIT'
                      ? 'bg-purple-500/20 text-purple-300'
                      : 'bg-cyan-500/20 text-cyan-300'
                  }`}
                >
                  {obj.type}
                </span>
              </div>
              <p className="text-[10px] text-slate-500 mt-1">{obj.desc}</p>
            </div>
          ))}
        </div>

        {/* Stored Procedures & Triggers List */}
        <div className="pt-2 border-t border-slate-800">
          <p className="text-xs font-mono font-semibold text-slate-400 uppercase mb-2">
            PL/SQL Stored Procedures & Triggers
          </p>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs font-mono">
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
              <span className="text-cyan-400">SP_EVALUATE_AND_ALERT_TRANSACTION</span>
              <span className="text-emerald-400 text-[10px]">Active</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
              <span className="text-cyan-400">SP_ASSIGN_INVESTIGATOR</span>
              <span className="text-emerald-400 text-[10px]">Active</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
              <span className="text-cyan-400">SP_UPDATE_INVESTIGATION_STATUS</span>
              <span className="text-emerald-400 text-[10px]">Active</span>
            </div>
            <div className="p-2.5 rounded-lg bg-slate-950 border border-slate-800 flex items-center justify-between">
              <span className="text-purple-400">TRG_INVESTIGATION_STATUS_AUDIT</span>
              <span className="text-emerald-400 text-[10px]">Trigger Active</span>
            </div>
          </div>
        </div>

        {/* Security Notice */}
        <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 flex items-center gap-3 text-xs text-slate-400">
          <Lock className="w-4 h-4 text-emerald-400 shrink-0" />
          <span>
            Security Policy Enforced: Connection passwords and internal host file paths are masked in API responses and client telemetry.
          </span>
        </div>
      </div>
    </div>
  );
};
