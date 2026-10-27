// TypeScript definitions for FraudLens Financial Platform

export type TransactionType = 'DEPOSIT' | 'WITHDRAWAL' | 'TRANSFER' | 'PAYMENT';
export type ChannelType = 'MOBILE_APP' | 'NET_BANKING' | 'ATM' | 'POS' | 'UPI';
export type TransactionStatus = 'COMPLETED' | 'PENDING' | 'FLAGGED' | 'FAILED';

export interface Transaction {
  transaction_id: number;
  account_id: number;
  account_number?: string;
  customer_id?: number;
  customer_name?: string;
  transaction_type: string;
  amount: number;
  transaction_date: string;
  channel: string;
  status: string;
  counterparty_account?: string;
  description?: string;
  alert_generated?: boolean;
  alert_id?: number;
  rule_triggered?: string;
}

export type SeverityLevel = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';
export type AlertStatus = 'PENDING' | 'ESCALATED' | 'DISMISSED' | 'RESOLVED';

export interface Alert {
  alert_id: number;
  transaction_id: number;
  alert_type: string;
  severity: SeverityLevel;
  rule_triggered: string;
  alert_date: string;
  status: AlertStatus;
  amount?: number;
  channel?: string;
  account_number?: string;
  customer_name?: string;
  has_investigation?: boolean;
  investigation_id?: number;
}

export type InvestigationStatus = 'OPEN' | 'UNDER REVIEW' | 'CLOSED';
export type InvestigationOutcome = 'CONFIRMED_FRAUD' | 'FALSE_POSITIVE' | 'INCONCLUSIVE' | 'PENDING';

export interface Investigation {
  investigation_id: number;
  alert_id: number;
  investigator_id?: number;
  investigator_name?: string;
  investigator_dept?: string;
  start_date: string;
  end_date?: string;
  status: InvestigationStatus;
  outcome: InvestigationOutcome;
  notes?: string;
  alert_type?: string;
  severity?: string;
  rule_triggered?: string;
  transaction_id?: number;
  amount?: number;
  channel?: string;
  account_number?: string;
  customer_name?: string;
}

export interface Investigator {
  investigator_id: number;
  first_name: string;
  last_name: string;
  full_name: string;
  email: string;
  department: string;
  experience_years: number;
  active_status: string;
}

export interface AccountOption {
  account_id: number;
  account_number: string;
  account_type: string;
  balance: number;
  customer_id: number;
  customer_name: string;
}

export interface AuditRecord {
  audit_id: number;
  source_table: string;
  record_id: number;
  old_status?: string;
  new_status?: string;
  changed_by: string;
  change_timestamp: string;
  action_type: string;
  remarks?: string;
}

export interface DashboardSummary {
  total_transactions: number;
  total_volume_inr: number;
  flagged_transactions: number;
  total_alerts: number;
  pending_alerts: number;
  critical_alerts: number;
  open_investigations: number;
  under_review_investigations: number;
  closed_investigations: number;
  confirmed_fraud_cases: number;
  active_investigators: number;
  high_amount_threshold: number;
}

export interface TrendItem {
  date: string;
  total_volume: number;
  tx_count: number;
  flagged_count: number;
}

export interface ChannelMetric {
  channel: string;
  total_tx: number;
  total_volume: number;
  avg_ticket: number;
}

export interface CustomerExposure {
  customer_id: number;
  customer_name: string;
  kyc_status: string;
  risk_score: number;
  total_accounts: number;
  total_transacted_volume: number;
  total_tx_count: number;
  alerts_incurred: number;
}

export interface SystemHealth {
  status: string;
  database_connected: boolean;
  database: {
    connected: boolean;
    info: {
      version?: string;
      container?: string;
      user?: string;
      db_name?: string;
      dsn?: string;
      mode?: string;
    };
    last_error?: string;
    active_tables: string[];
  };
  high_amount_threshold: number;
  timestamp: string;
  version: string;
  mode: string;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  is_live_oracle: boolean;
}

export interface PaginatedResult<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
