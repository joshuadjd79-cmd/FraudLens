import {
  Transaction,
  Alert,
  Investigation,
  Investigator,
  AuditRecord,
  DashboardSummary,
  TrendItem,
  ChannelMetric,
  CustomerExposure,
  SystemHealth,
  AccountOption,
  ApiResponse,
  PaginatedResult,
} from '../types';

const BASE_URL = '/api';

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${BASE_URL}${endpoint}`;
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {}),
  };

  const response = await fetch(url, { ...options, headers });
  const json = await response.json();

  if (!response.ok) {
    const errorMsg = json.detail || json.message || 'An unexpected error occurred';
    throw new Error(errorMsg);
  }

  return json.data;
}

export const api = {
  // System Health
  getHealth: () => request<SystemHealth>('/health'),

  // Dashboard
  getDashboardSummary: () => request<DashboardSummary>('/dashboard/summary'),
  getDashboardTrends: () => request<TrendItem[]>('/dashboard/trends'),

  // Transactions
  getTransactions: (params: {
    page?: number;
    page_size?: number;
    account_id?: number;
    channel?: string;
    transaction_type?: string;
    status?: string;
    min_amount?: number;
    max_amount?: number;
    search?: string;
  }) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, String(val));
      }
    });
    return request<PaginatedResult<Transaction>>(`/transactions?${query.toString()}`);
  },

  getTransactionById: (id: number) => request<Transaction>(`/transactions/${id}`),

  createTransaction: (data: {
    account_id: number;
    transaction_type: string;
    amount: number;
    channel: string;
    counterparty_account?: string;
    description?: string;
  }) =>
    request<Transaction>('/transactions', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getActiveAccounts: () => request<AccountOption[]>('/accounts'),

  exportTransactionsCsvUrl: () => `${BASE_URL}/transactions/export/csv`,

  // Alerts
  getAlerts: (params: {
    page?: number;
    page_size?: number;
    severity?: string;
    status?: string;
    search?: string;
  }) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, String(val));
      }
    });
    return request<PaginatedResult<Alert>>(`/alerts?${query.toString()}`);
  },

  getAlertById: (id: number) => request<Alert>(`/alerts/${id}`),

  // Investigations
  getInvestigations: (params: {
    page?: number;
    page_size?: number;
    status?: string;
    outcome?: string;
    search?: string;
  }) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, String(val));
      }
    });
    return request<PaginatedResult<Investigation>>(`/investigations?${query.toString()}`);
  },

  getInvestigationById: (id: number) => request<Investigation>(`/investigations/${id}`),

  createInvestigation: (data: { alert_id: number; investigator_id?: number; notes?: string }) =>
    request<Investigation>('/investigations', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  assignInvestigator: (investigationId: number, investigatorId: number) =>
    request<Investigation>(`/investigations/${investigationId}/assign`, {
      method: 'POST',
      body: JSON.stringify({ investigator_id: investigatorId }),
    }),

  updateInvestigationStatus: (
    investigationId: number,
    data: { new_status: string; outcome?: string; notes?: string }
  ) =>
    request<Investigation>(`/investigations/${investigationId}/status`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  getInvestigators: (activeOnly: boolean = true) =>
    request<Investigator[]>(`/investigators?active_only=${activeOnly}`),

  // Audit
  getAuditTrail: (params: {
    page?: number;
    page_size?: number;
    table_name?: string;
    search?: string;
  }) => {
    const query = new URLSearchParams();
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, String(val));
      }
    });
    return request<PaginatedResult<AuditRecord>>(`/audit?${query.toString()}`);
  },

  // Analytics
  getAnalyticsSummary: () =>
    request<{
      kpis: DashboardSummary;
      channel_breakdown: ChannelMetric[];
      severity_breakdown: { severity: string; count: number }[];
      outcome_breakdown: { outcome: string; count: number }[];
      timeline: TrendItem[];
    }>('/analytics/summary'),

  getCustomerExposure: () => request<CustomerExposure[]>('/analytics/customer-exposure'),

  // Demo Runner
  runDemoScenario: () => request<any>('/demo/run-scenario', { method: 'POST' }),
};
