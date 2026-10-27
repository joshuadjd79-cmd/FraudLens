import React, { useState, useEffect } from 'react';
import {
  Search,
  Filter,
  Plus,
  Download,
  AlertTriangle,
  ChevronLeft,
  ChevronRight,
  Eye,
  CheckCircle2,
  Clock,
  ArrowUpRight,
  CreditCard,
} from 'lucide-react';
import { Transaction, AccountOption } from '../types';
import { api } from '../api/client';
import { StatusBadge } from '../components/common/Badge';
import { Modal } from '../components/common/Modal';

interface TransactionsPageProps {
  onRefreshTrigger?: () => void;
  openCreateModal?: boolean;
  onCloseCreateModal?: () => void;
}

export const TransactionsPage: React.FC<TransactionsPageProps> = ({
  onRefreshTrigger,
  openCreateModal = false,
  onCloseCreateModal,
}) => {
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [totalCount, setTotalCount] = useState<number>(0);
  const [page, setPage] = useState<number>(1);
  const [pageSize] = useState<number>(10);
  const [totalPages, setTotalPages] = useState<number>(1);
  const [isLoading, setIsLoading] = useState<boolean>(true);

  // Filters
  const [search, setSearch] = useState<string>('');
  const [channelFilter, setChannelFilter] = useState<string>('');
  const [typeFilter, setTypeFilter] = useState<string>('');
  const [statusFilter, setStatusFilter] = useState<string>('');

  // Selected Transaction for Detail Modal
  const [selectedTx, setSelectedTx] = useState<Transaction | null>(null);

  // Create Transaction Form State
  const [isCreateOpen, setIsCreateOpen] = useState<boolean>(openCreateModal);
  const [accounts, setAccounts] = useState<AccountOption[]>([]);
  const [createForm, setCreateForm] = useState({
    account_id: 2001,
    transaction_type: 'TRANSFER',
    amount: 15000,
    channel: 'MOBILE_APP',
    counterparty_account: '',
    description: '',
  });
  const [formError, setFormError] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [createdSuccessTx, setCreatedSuccessTx] = useState<Transaction | null>(null);

  useEffect(() => {
    setIsCreateOpen(openCreateModal);
  }, [openCreateModal]);

  const loadTransactions = async () => {
    try {
      setIsLoading(true);
      const res = await api.getTransactions({
        page,
        page_size: pageSize,
        channel: channelFilter || undefined,
        transaction_type: typeFilter || undefined,
        status: statusFilter || undefined,
        search: search || undefined,
      });
      setTransactions(res.items);
      setTotalCount(res.total);
      setTotalPages(res.total_pages);
    } catch (err: any) {
      console.error('Failed to load transactions:', err);
    } finally {
      setIsLoading(false);
    }
  };

  const loadAccounts = async () => {
    try {
      const accs = await api.getActiveAccounts();
      setAccounts(accs);
      if (accs.length > 0 && !createForm.account_id) {
        setCreateForm((prev) => ({ ...prev, account_id: accs[0].account_id }));
      }
    } catch (err) {
      console.error('Failed to load accounts for dropdown:', err);
    }
  };

  useEffect(() => {
    loadTransactions();
  }, [page, channelFilter, typeFilter, statusFilter]);

  useEffect(() => {
    loadAccounts();
  }, []);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setPage(1);
    loadTransactions();
  };

  const handleCreateSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    if (createForm.amount <= 0) {
      setFormError('Amount must be strictly greater than ₹0.00');
      return;
    }

    try {
      setIsSubmitting(true);
      const newTx = await api.createTransaction({
        account_id: Number(createForm.account_id),
        transaction_type: createForm.transaction_type,
        amount: Number(createForm.amount),
        channel: createForm.channel,
        counterparty_account: createForm.counterparty_account || undefined,
        description: createForm.description || undefined,
      });

      setCreatedSuccessTx(newTx);
      loadTransactions();
      if (onRefreshTrigger) onRefreshTrigger();
    } catch (err: any) {
      setFormError(err.message || 'Transaction submission failed');
    } finally {
      setIsSubmitting(false);
    }
  };

  const formatINR = (val: number) => {
    return new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
      maximumFractionDigits: 2,
    }).format(val);
  };

  return (
    <div className="space-y-6">
      {/* Top Header & Action Controls */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-white tracking-tight">Transaction Explorer</h1>
          <p className="text-xs text-slate-400 mt-0.5">
            Real-time Oracle TRANSACTIONS stream with parameterized search and procedural alert triggers
          </p>
        </div>

        <div className="flex items-center gap-2.5">
          <a
            href={api.exportTransactionsCsvUrl()}
            download="fraudlens_transactions.csv"
            className="flex items-center gap-2 px-3.5 py-2 rounded-xl bg-slate-900 hover:bg-slate-800 border border-slate-700 text-xs font-medium text-slate-200 transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-cyan-400" />
            <span>Export CSV</span>
          </a>

          <button
            onClick={() => {
              setCreatedSuccessTx(null);
              setFormError(null);
              setIsCreateOpen(true);
            }}
            className="flex items-center gap-2 px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs shadow-md shadow-cyan-500/20 transition-all hover:scale-105 active:scale-95"
          >
            <Plus className="w-4 h-4" />
            <span>Post Transaction</span>
          </button>
        </div>
      </div>

      {/* Filter & Search Bar */}
      <div className="p-4 rounded-xl bg-slate-900 border border-slate-800 flex flex-col md:flex-row gap-3 items-stretch md:items-center justify-between">
        <form onSubmit={handleSearchSubmit} className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search by ID, Account #, Customer name, or Description..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 transition-colors"
          />
        </form>

        <div className="flex flex-wrap items-center gap-2">
          {/* Channel Filter */}
          <select
            value={channelFilter}
            onChange={(e) => {
              setChannelFilter(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All Channels</option>
            <option value="MOBILE_APP">Mobile App</option>
            <option value="NET_BANKING">Net Banking</option>
            <option value="ATM">ATM</option>
            <option value="POS">POS Terminal</option>
            <option value="UPI">UPI</option>
          </select>

          {/* Type Filter */}
          <select
            value={typeFilter}
            onChange={(e) => {
              setTypeFilter(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All Types</option>
            <option value="TRANSFER">Transfer</option>
            <option value="PAYMENT">Payment</option>
            <option value="DEPOSIT">Deposit</option>
            <option value="WITHDRAWAL">Withdrawal</option>
          </select>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className="px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-xs text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All Statuses</option>
            <option value="COMPLETED">Completed</option>
            <option value="FLAGGED">Flagged</option>
            <option value="PENDING">Pending</option>
          </select>
        </div>
      </div>

      {/* Transactions Table */}
      <div className="rounded-xl bg-slate-900 border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/50 text-slate-400 font-mono">
                <th className="py-3 px-4 font-semibold">Tx ID</th>
                <th className="py-3 px-4 font-semibold">Customer & Account</th>
                <th className="py-3 px-4 font-semibold">Type</th>
                <th className="py-3 px-4 font-semibold">Amount (INR)</th>
                <th className="py-3 px-4 font-semibold">Channel</th>
                <th className="py-3 px-4 font-semibold">Status</th>
                <th className="py-3 px-4 font-semibold">Surveillance</th>
                <th className="py-3 px-4 font-semibold">Timestamp</th>
                <th className="py-3 px-4 font-semibold text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 font-sans">
              {isLoading ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-slate-400 font-mono text-xs">
                    Loading Oracle transaction stream...
                  </td>
                </tr>
              ) : transactions.length === 0 ? (
                <tr>
                  <td colSpan={9} className="py-12 text-center text-slate-400">
                    No transactions match the selected filters.
                  </td>
                </tr>
              ) : (
                transactions.map((t) => (
                  <tr key={t.transaction_id} className="hover:bg-slate-800/40 transition-colors">
                    <td className="py-3 px-4 font-mono font-bold text-cyan-400">
                      #{t.transaction_id}
                    </td>
                    <td className="py-3 px-4">
                      <div className="font-medium text-slate-200">{t.customer_name || 'N/A'}</div>
                      <div className="text-[10px] font-mono text-slate-400">
                        {t.account_number || `Acc #${t.account_id}`}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <span className="font-mono text-[11px] text-slate-300 font-semibold">
                        {t.transaction_type}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-mono font-bold text-white text-[13px] whitespace-nowrap">
                      {formatINR(t.amount)}
                    </td>
                    <td className="py-3 px-4">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-mono text-[10px] border border-slate-700/60">
                        {t.channel}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <StatusBadge status={t.status} />
                    </td>
                    <td className="py-3 px-4">
                      {t.alert_generated || t.status === 'FLAGGED' ? (
                        <div className="flex items-center gap-1.5 text-rose-400 font-medium">
                          <AlertTriangle className="w-3.5 h-3.5" />
                          <span className="text-[11px]">Alert #{t.alert_id || 'FLAG'}</span>
                        </div>
                      ) : (
                        <div className="flex items-center gap-1.5 text-slate-500">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500/70" />
                          <span className="text-[11px]">Pass</span>
                        </div>
                      )}
                    </td>
                    <td className="py-3 px-4 font-mono text-[11px] text-slate-400 whitespace-nowrap">
                      {t.transaction_date}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setSelectedTx(t)}
                        className="p-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 hover:text-white transition-colors"
                        title="View Full Transaction Dossier"
                      >
                        <Eye className="w-3.5 h-3.5" />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination Bar */}
        <div className="p-4 border-t border-slate-800 flex items-center justify-between text-xs text-slate-400">
          <div>
            Showing page <span className="font-bold text-white font-mono">{page}</span> of{' '}
            <span className="font-bold text-white font-mono">{totalPages}</span> (Total{' '}
            <span className="font-bold text-white font-mono">{totalCount}</span> records)
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setPage((p) => Math.max(p - 1, 1))}
              disabled={page <= 1}
              className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <span className="font-mono font-medium px-2 text-white">
              {page} / {totalPages}
            </span>
            <button
              onClick={() => setPage((p) => Math.min(p + 1, totalPages))}
              disabled={page >= totalPages}
              className="p-1.5 rounded-lg bg-slate-950 border border-slate-800 hover:bg-slate-800 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      {/* Transaction Detail Modal */}
      <Modal
        isOpen={selectedTx !== null}
        onClose={() => setSelectedTx(null)}
        title={`Transaction Dossier #${selectedTx?.transaction_id}`}
        subtitle="Complete record facts and PL/SQL rule evaluation audit"
        maxWidth="lg"
      >
        {selectedTx && (
          <div className="space-y-4 text-xs">
            <div className="grid grid-cols-2 gap-3 p-4 rounded-xl bg-slate-950 border border-slate-800">
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Amount Settled</p>
                <p className="text-xl font-bold font-mono text-cyan-400 mt-0.5">
                  {formatINR(selectedTx.amount)}
                </p>
              </div>
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Status</p>
                <div className="mt-1">
                  <StatusBadge status={selectedTx.status} />
                </div>
              </div>
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Customer</p>
                <p className="text-slate-200 font-medium mt-0.5">{selectedTx.customer_name || 'N/A'}</p>
              </div>
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Account Number</p>
                <p className="text-slate-200 font-mono mt-0.5">
                  {selectedTx.account_number || `Acc #${selectedTx.account_id}`}
                </p>
              </div>
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Transaction Type</p>
                <p className="text-slate-200 font-mono mt-0.5">{selectedTx.transaction_type}</p>
              </div>
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Payment Channel</p>
                <p className="text-slate-200 font-mono mt-0.5">{selectedTx.channel}</p>
              </div>
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Counterparty</p>
                <p className="text-slate-200 font-mono mt-0.5 truncate">
                  {selectedTx.counterparty_account || 'N/A (Self/ATM Draw)'}
                </p>
              </div>
              <div>
                <p className="text-slate-400 uppercase font-mono text-[10px]">Timestamp</p>
                <p className="text-slate-200 font-mono mt-0.5">{selectedTx.transaction_date}</p>
              </div>
            </div>

            {/* Description */}
            <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800">
              <p className="text-slate-400 text-[10px] uppercase font-mono">Ledger Description</p>
              <p className="text-slate-300 mt-1">{selectedTx.description || 'No memo attached.'}</p>
            </div>

            {/* Surveillance Evaluation Banner */}
            <div
              className={`p-4 rounded-xl border ${
                selectedTx.status === 'FLAGGED' || selectedTx.alert_generated
                  ? 'bg-rose-500/10 border-rose-500/30'
                  : 'bg-emerald-500/10 border-emerald-500/30'
              }`}
            >
              <div className="flex items-start gap-3">
                {selectedTx.status === 'FLAGGED' || selectedTx.alert_generated ? (
                  <AlertTriangle className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
                ) : (
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
                )}
                <div>
                  <h4 className="font-semibold text-white">
                    {selectedTx.status === 'FLAGGED' || selectedTx.alert_generated
                      ? 'Surveillance Breach Flagged'
                      : 'Cleared Standard Surveillance'}
                  </h4>
                  <p className="text-[11px] text-slate-300 mt-1">
                    {selectedTx.rule_triggered ||
                      (selectedTx.amount > 50000
                        ? 'Triggered rule: High value transfer exceeded ₹50,000 threshold (SP_EVALUATE_AND_ALERT_TRANSACTION).'
                        : 'Transaction amount within normal operational velocity limits.')}
                  </p>
                  {selectedTx.alert_id && (
                    <div className="mt-2 text-xs font-mono text-rose-300 font-medium">
                      Generated Surveillance Alert ID: #{selectedTx.alert_id}
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        )}
      </Modal>

      {/* Post Transaction Modal */}
      <Modal
        isOpen={isCreateOpen}
        onClose={() => {
          setIsCreateOpen(false);
          if (onCloseCreateModal) onCloseCreateModal();
        }}
        title="Post Financial Transaction"
        subtitle="Submits to Oracle TRANSACTIONS and executes SP_EVALUATE_AND_ALERT_TRANSACTION"
        maxWidth="md"
      >
        {createdSuccessTx ? (
          <div className="space-y-4">
            <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-xs">
              <div className="flex items-center gap-2 font-bold text-sm text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
                <span>Transaction Recorded into Oracle</span>
              </div>
              <p className="mt-1">
                Transaction ID <span className="font-mono font-bold">#{createdSuccessTx.transaction_id}</span> has been committed to the live database.
              </p>
            </div>

            {createdSuccessTx.alert_generated ? (
              <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-xs">
                <div className="flex items-center gap-2 font-bold text-rose-400">
                  <AlertTriangle className="w-4 h-4" />
                  <span>Procedural Rule Violation Triggered</span>
                </div>
                <p className="mt-1 text-slate-300">
                  Amount <span className="font-mono font-bold text-white">{formatINR(createdSuccessTx.amount)}</span> breached the ₹50,000 tier!
                </p>
                <p className="mt-1 font-mono text-cyan-400">
                  Alert #{createdSuccessTx.alert_id} generated via stored procedure!
                </p>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs text-slate-300">
                Amount <span className="font-mono font-bold">{formatINR(createdSuccessTx.amount)}</span> was under the ₹50,000 threshold. Cleared without alert.
              </div>
            )}

            <button
              onClick={() => {
                setCreatedSuccessTx(null);
                setCreateForm({
                  account_id: accounts[0]?.account_id || 2001,
                  transaction_type: 'TRANSFER',
                  amount: 15000,
                  channel: 'MOBILE_APP',
                  counterparty_account: '',
                  description: '',
                });
              }}
              className="w-full py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-white font-medium text-xs transition-colors"
            >
              Post Another Transaction
            </button>
          </div>
        ) : (
          <form onSubmit={handleCreateSubmit} className="space-y-4 text-xs">
            {formError && (
              <div className="p-3 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-400">
                {formError}
              </div>
            )}

            {/* Account Selector */}
            <div>
              <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
                Originating Account (Oracle ACCOUNT Table)
              </label>
              <select
                value={createForm.account_id}
                onChange={(e) =>
                  setCreateForm((prev) => ({ ...prev, account_id: Number(e.target.value) }))
                }
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500"
              >
                {accounts.map((acc) => (
                  <option key={acc.account_id} value={acc.account_id}>
                    {acc.account_number} — {acc.customer_name} ({acc.account_type}, Bal: {formatINR(acc.balance)})
                  </option>
                ))}
              </select>
            </div>

            {/* Transaction Type & Channel */}
            <div className="grid grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
                  Transaction Type
                </label>
                <select
                  value={createForm.transaction_type}
                  onChange={(e) =>
                    setCreateForm((prev) => ({ ...prev, transaction_type: e.target.value }))
                  }
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500"
                >
                  <option value="TRANSFER">TRANSFER</option>
                  <option value="PAYMENT">PAYMENT</option>
                  <option value="DEPOSIT">DEPOSIT</option>
                  <option value="WITHDRAWAL">WITHDRAWAL</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
                  Payment Channel
                </label>
                <select
                  value={createForm.channel}
                  onChange={(e) =>
                    setCreateForm((prev) => ({ ...prev, channel: e.target.value }))
                  }
                  className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500"
                >
                  <option value="MOBILE_APP">Mobile App</option>
                  <option value="NET_BANKING">Net Banking</option>
                  <option value="ATM">ATM</option>
                  <option value="POS">POS Terminal</option>
                  <option value="UPI">UPI</option>
                </select>
              </div>
            </div>

            {/* Amount */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="block text-slate-400 font-medium font-mono text-[11px]">
                  Amount in INR (₹)
                </label>
                <span className="text-[10px] text-cyan-400 font-mono">
                  Threshold: ₹50,000 (triggers alert)
                </span>
              </div>
              <input
                type="number"
                step="0.01"
                min="1"
                required
                value={createForm.amount}
                onChange={(e) =>
                  setCreateForm((prev) => ({ ...prev, amount: parseFloat(e.target.value) || 0 }))
                }
                className="w-full px-3 py-2.5 rounded-lg bg-slate-950 border border-slate-800 text-white font-mono text-base font-bold focus:outline-none focus:border-cyan-500"
              />
              <div className="flex gap-2 mt-2">
                <button
                  type="button"
                  onClick={() => setCreateForm((prev) => ({ ...prev, amount: 15000 }))}
                  className="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-300 text-[10px] font-mono"
                >
                  ₹15,000 (Normal)
                </button>
                <button
                  type="button"
                  onClick={() => setCreateForm((prev) => ({ ...prev, amount: 85000 }))}
                  className="px-2.5 py-1 rounded bg-rose-500/20 hover:bg-rose-500/30 text-rose-300 text-[10px] font-mono border border-rose-500/40 font-semibold"
                >
                  ₹85,000 (Trigger High Rule)
                </button>
              </div>
            </div>

            {/* Counterparty Account */}
            <div>
              <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
                Counterparty Account (Beneficiary / Merchant)
              </label>
              <input
                type="text"
                placeholder="e.g. BENEFICIARY-NEFT-8890"
                value={createForm.counterparty_account}
                onChange={(e) =>
                  setCreateForm((prev) => ({ ...prev, counterparty_account: e.target.value }))
                }
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500 font-mono"
              />
            </div>

            {/* Description */}
            <div>
              <label className="block text-slate-400 font-medium mb-1 font-mono text-[11px]">
                Transaction Description Memo
              </label>
              <input
                type="text"
                placeholder="e.g. Commercial raw material settlement"
                value={createForm.description}
                onChange={(e) =>
                  setCreateForm((prev) => ({ ...prev, description: e.target.value }))
                }
                className="w-full px-3 py-2 rounded-lg bg-slate-950 border border-slate-800 text-white text-xs focus:outline-none focus:border-cyan-500"
              />
            </div>

            <div className="pt-2">
              <button
                type="submit"
                disabled={isSubmitting}
                className="w-full py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-slate-950 font-bold text-xs tracking-wide shadow-md shadow-cyan-500/20 transition-all"
              >
                {isSubmitting ? 'Executing Oracle Stored Procedure...' : 'Submit Transaction'}
              </button>
            </div>
          </form>
        )}
      </Modal>
    </div>
  );
};
