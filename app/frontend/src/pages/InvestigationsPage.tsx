import React, { useState, useEffect } from 'react';
import {
  Briefcase,
  UserCheck,
  Search,
  Filter,
  CheckCircle2,
  Clock,
  AlertTriangle,
  User,
  ArrowRight,
  ShieldAlert,
  ChevronLeft,
  ChevronRight,
  Edit3,
} from 'lucide-react';
import { Investigation, Investigator, InvestigationStatus, InvestigationOutcome } from '../types';
import { api } from '../api/client';
import { StatusBadge, SeverityBadge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

interface InvestigationsPageProps {
  onRefreshTrigger?: () => void;
}

export const InvestigationsPage: React.FC<InvestigationsPageProps> = ({ onRefreshTrigger }) => {
  const [investigations, setInvestigations] = useState<Investigation[]>([]);
  const [investigators, setInvestigators] = useState<Investigator[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [pageSize] = useState<number>(10);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Filters
  const [statusFilter, setStatusFilter] = useState<string>('');
  const [outcomeFilter, setOutcomeFilter] = useState<string>('');
  const [search, setSearch] = useState<string>('');

  // Modals
  const [assignModalCase, setAssignModalCase] = useState<Investigation | null>(null);
  const [selectedInvestigatorId, setSelectedInvestigatorId] = useState<number>(301);
  const [isAssigning, setIsAssigning] = useState<boolean>(false);
  const [assignError, setAssignError] = useState<string | null>(null);

  const [statusModalCase, setStatusModalCase] = useState<Investigation | null>(null);
  const [newStatus, setNewStatus] = useState<string>('UNDER REVIEW');
  const [newOutcome, setNewOutcome] = useState<string>('CONFIRMED_FRAUD');
  const [statusNotes, setStatusNotes] = useState<string>('');
  const [isUpdatingStatus, setIsUpdatingStatus] = useState<boolean>(false);
  const [statusError, setStatusError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setIsLoading(true);
      const [invRes, invrRes] = await Promise.all([
        api.getInvestigations({
          page,
          page_size: pageSize,
          status: statusFilter || undefined,
          outcome: outcomeFilter || undefined,
          search: search || undefined,
        }),
        api.getInvestigators(true),
      ]);
      setInvestigations(invRes.items);
      setTotalCount(invRes.total);
      setTotalPages(invRes.total_pages);
      setInvestigators(invrRes);
    } catch (err) {
      console.error('Failed to load investigation data:', err);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [page, statusFilter, outcomeFilter]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadData();
  };

  const handleAssignSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!assignModalCase) return;
    setAssignError(null);
    try {
      setIsAssigning(true);
      await api.assignInvestigator(assignModalCase.investigation_id, Number(selectedInvestigatorId));
      setAssignModalCase(null);
      loadData();
      if (onRefreshTrigger) onRefreshTrigger();
    } catch (err: any) {
      setAssignError(err.message || 'Assignment failed');
    } finally {
      setIsAssigning(false);
    }
  };

  const handleStatusSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!statusModalCase) return;
    setStatusError(null);

    if (newStatus === 'CLOSED' && (!newOutcome || newOutcome === 'PENDING')) {
      setStatusError('Closing an investigation requires a confirmed outcome (CONFIRMED_FRAUD, FALSE_POSITIVE, or INCONCLUSIVE).');
      return;
    }

    try {
      setIsUpdatingStatus(true);
      await api.updateInvestigationStatus(statusModalCase.investigation_id, {
        new_status: newStatus,
        outcome: newStatus === 'CLOSED' ? newOutcome : undefined,
        notes: statusNotes || undefined,
      });
      setStatusModalCase(null);
      loadData();
      if (onRefreshTrigger) onRefreshTrigger();
    } catch (err: any) {
      setStatusError(err.message || 'Status transition failed');
    } finally {
      setIsUpdatingStatus(false);
    }
  };

  const formatINR = (val?: number) => {
    if (!val) return '₹0.00';
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 0,
    }).format(val);
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight">Investigation Case Management</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Operational dockets managed via SP_ASSIGN_INVESTIGATOR and SP_UPDATE_INVESTIGATION_STATUS
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
        <form onSubmit={handleSearchSubmit} className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by Case ID, Notes, Investigator, or Alert ID..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition-colors"
          />
        </form>

        <div className="flex items-center gap-2">
          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All Case Statuses</option>
            <option value="OPEN">Open (Triage)</option>
            <option value="UNDER REVIEW">Under Review</option>
            <option value="CLOSED">Closed (Resolved)</option>
          </select>

          {/* Outcome Filter */}
          <select
            value={outcomeFilter}
            onChange={(e) => {
              setOutcomeFilter(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All Outcomes</option>
            <option value="CONFIRMED_FRAUD">Confirmed Fraud</option>
            <option value="FALSE_POSITIVE">False Positive</option>
            <option value="INCONCLUSIVE">Inconclusive</option>
            <option value="PENDING">Pending</option>
          </select>
        </div>
      </div>

      {/* Investigations Table */}
      <div className="rounded-xl bg-slate-900 border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/50 text-slate-400 font-mono">
                <th className="py-3 px-4 font-semibold">Case ID</th>
                <th className="py-3 px-4 font-semibold">Alert Reference</th>
                <th className="py-3 px-4 font-semibold">Assigned Investigator</th>
                <th className="py-3 px-4 font-semibold">Customer & Volume</th>
                <th className="py-3 px-4 font-semibold">Case Status</th>
                <th className="py-3 px-4 font-semibold">Outcome</th>
                <th className="py-3 px-4 font-semibold">Opened Date</th>
                <th className="py-3 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {isLoading ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-400 font-mono text-xs">
                    Querying Oracle INVESTIGATION table...
                  </td>
                </tr>
              ) : investigations.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-12 text-center text-slate-400">
                    No investigation cases match the selected filters.
                  </td>
                </tr>
              ) : (
                investigations.map((inv) => (
                  <tr key={inv.investigation_id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-mono font-bold text-cyan-400">
                      #{inv.investigation_id}
                    </td>
                    <td className="py-3 px-4 max-w-xs">
                      <div className="font-semibold text-slate-200">Alert #{inv.alert_id}</div>
                      <div className="text-[10px] text-slate-400 truncate">{inv.rule_triggered}</div>
                    </td>
                    <td className="py-3 px-4">
                      {inv.investigator_name && inv.investigator_name !== 'UNASSIGNED' ? (
                        <div className="flex items-center gap-2">
                          <div className="w-6 h-6 rounded-full bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold text-[10px] border border-cyan-500/20">
                            {inv.investigator_name.slice(0, 2).toUpperCase()}
                          </div>
                          <div>
                            <div className="font-medium text-slate-200">{inv.investigator_name}</div>
                            <div className="text-[10px] font-mono text-slate-500">ID #{inv.investigator_id}</div>
                          </div>
                        </div>
                      ) : (
                        <span className="text-amber-400 font-mono text-[11px] bg-amber-500/10 px-2 py-0.5 rounded border border-amber-500/20">
                          Unassigned
                        </span>
                      )}
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-medium text-slate-200">{inv.customer_name || 'N/A'}</div>
                      <div className="text-[11px] font-mono text-cyan-400 font-semibold">
                        {formatINR(inv.amount)}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <StatusBadge status={inv.status} />
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`font-mono text-[11px] font-semibold ${
                          inv.outcome === 'CONFIRMED_FRAUD'
                            ? 'text-rose-400'
                            : inv.outcome === 'FALSE_POSITIVE'
                            ? 'text-emerald-400'
                            : 'text-slate-400'
                        }`}
                      >
                        {inv.outcome}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono text-[11px] text-slate-400 whitespace-nowrap">
                      {inv.start_date}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="flex items-center justify-end gap-1.5">
                        {/* Assign Button */}
                        <button
                          onClick={() => {
                            setAssignError(null);
                            setSelectedInvestigatorId(inv.investigator_id || 301);
                            setAssignModalCase(inv);
                          }}
                          className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-[11px] font-medium transition-colors border border-slate-700/60"
                          title="Assign or reassign investigator via SP_ASSIGN_INVESTIGATOR"
                        >
                          Assign
                        </button>

                        {/* Status Update Button */}
                        <button
                          onClick={() => {
                            setStatusError(null);
                            setNewStatus(inv.status === 'OPEN' ? 'UNDER REVIEW' : 'CLOSED');
                            setNewOutcome('CONFIRMED_FRAUD');
                            setStatusNotes(inv.notes || '');
                            setStatusModalCase(inv);
                          }}
                          className="px-2.5 py-1 rounded-lg bg-cyan-500/10 hover:bg-cyan-500/20 text-cyan-400 border border-cyan-500/30 text-[11px] font-medium transition-colors"
                          title="Progress status via SP_UPDATE_INVESTIGATION_STATUS"
                        >
                          Status
                        </button>
                      </div>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
        <div className="p-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div>
            Page <span className="font-bold text-white font-mono">{page}</span> of{' '}
            <span className="font-bold text-white font-mono">{totalPages}</span> (Total{' '}
            <span className="font-bold text-white font-mono">{totalCount}</span> cases)
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page <= 1}
              className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-mono font-medium px-2 text-white">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page >= totalPages}
              className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Assign Investigator Modal */}
      <Modal
        isOpen={assignModalCase !== null}
        onClose={() => setAssignModalCase(null)}
        title={`Assign Investigator to Case #${assignModalCase?.investigation_id}`}
        subtitle="Executes Oracle stored procedure SP_ASSIGN_INVESTIGATOR"
        maxWidth="md"
      >
        <form onSubmit={handleAssignSubmit} className="space-y-4 text-xs">
          {assignError && (
            <div className="p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-400">
              {assignError}
            </div>
          )}

          <div>
            <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
              Certified Investigator (Oracle INVESTIGATOR Table)
            </label>
            <select
              value={selectedInvestigatorId}
              onChange={(e) => setSelectedInvestigatorId(Number(e.target.value))}
              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500"
            >
              {investigators.map((inv) => (
                <option key={inv.investigator_id} value={inv.investigator_id}>
                  {inv.full_name} ({inv.department}, {inv.experience_years} yrs exp) — ID #{inv.investigator_id}
                </option>
              ))}
            </select>
            <p className="mt-1 text-[11px] text-slate-500">
              Stored procedure enforces active credential verification and auto-transitions case from OPEN to UNDER REVIEW.
            </p>
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={isAssigning}
              className="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs tracking-wide shadow-md shadow-cyan-500/20 transition-all"
            >
              {isAssigning ? 'Calling SP_ASSIGN_INVESTIGATOR...' : 'Confirm Assignment in Oracle'}
            </button>
          </div>
        </form>
      </Modal>

      {/* Update Investigation Status Modal */}
      <Modal
        isOpen={statusModalCase !== null}
        onClose={() => setStatusModalCase(null)}
        title={`Update Status: Case #${statusModalCase?.investigation_id}`}
        subtitle="Executes SP_UPDATE_INVESTIGATION_STATUS & fires TRG_INVESTIGATION_STATUS_AUDIT"
        maxWidth="md"
      >
        <form onSubmit={handleStatusSubmit} className="space-y-4 text-xs">
          {statusError && (
            <div className="p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-400">
              {statusError}
            </div>
          )}

          {/* New Status */}
          <div>
            <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
              Target Investigation Status
            </label>
            <select
              value={newStatus}
              onChange={(e) => setNewStatus(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500"
            >
              <option value="UNDER REVIEW">UNDER REVIEW</option>
              <option value="CLOSED">CLOSED (Final Case Docket Resolution)</option>
              <option value="OPEN">OPEN (Return to Triage)</option>
            </select>
          </div>

          {/* Mandatory Outcome if Closed */}
          {newStatus === 'CLOSED' && (
            <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-2">
              <label className="block text-slate-300 font-bold font-mono text-[11px]">
                Definitive Resolution Outcome (Mandatory)
              </label>
              <select
                value={newOutcome}
                onChange={(e) => setNewOutcome(e.target.value)}
                className="w-full px-3 py-2 rounded-lg bg-slate-900 border border-slate-700 text-white text-xs focus:outline-none focus:border-cyan-500 font-semibold"
              >
                <option value="CONFIRMED_FRAUD">CONFIRMED_FRAUD (Card/Account Locked)</option>
                <option value="FALSE_POSITIVE">FALSE_POSITIVE (Customer Authorized)</option>
                <option value="INCONCLUSIVE">INCONCLUSIVE (Customer Unreachable)</option>
              </select>
              <p className="text-[10px] text-amber-400">
                Business rule: Database stored procedure requires valid resolution outcome upon closure.
              </p>
            </div>
          )}

          {/* Case Notes */}
          <div>
            <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
              Investigator Findings Memo / Forensic Notes
            </label>
            <textarea
              rows={3}
              placeholder="Enter forensic remarks, counterparty inquiry results, or customer statement..."
              value={statusNotes}
              onChange={(e) => setStatusNotes(e.target.value)}
              className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div className="p-3 rounded-lg bg-cyan-500/10 border border-cyan-500/20 text-[11px] text-cyan-300">
            Database trigger <span className="font-mono font-bold">TRG_INVESTIGATION_STATUS_AUDIT</span> will automatically log this state change with session user and timestamp to <span className="font-mono font-bold">INVESTIGATION_AUDIT</span>.
          </div>

          <div className="pt-2">
            <button
              type="submit"
              disabled={isUpdatingStatus}
              className="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs tracking-wide shadow-md shadow-cyan-500/20 transition-all"
            >
              {isUpdatingStatus ? 'Executing Procedure & Trigger...' : 'Commit Status Update'}
            </button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
