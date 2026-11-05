/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useEffect, useState } from 'react';

interface TransactionRecord {
  transaction_id: string;
  tx_type: string;
  amount: number;
  fee: number;
  total_impact: number;
  balance_after: number;
  note: string;
  timestamp: string;
}

interface AccountRules {
  class_name: string;
  maintaining_balance: number;
  per_tx_limit: number;
  withdrawal_fee: number;
  policy_description: string;
}

interface AccountData {
  class_name: string;
  account_number: string;
  holder_name: string;
  balance: number;
  account_type: string;
  rules: AccountRules;
  max_withdrawable: number;
  transactions: TransactionRecord[];
}

interface FeedbackMessage {
  status: 'success' | 'error' | 'info';
  title: string;
  message: string;
  error_code?: string;
}

interface PolyComparison {
  class_name: string;
  account_type: string;
  starting_balance: number;
  requested_withdrawal: number;
  fee_charged: number;
  total_deducted: number;
  ending_balance: number;
  status: string;
  explanation: string;
}

interface PolyDemoData {
  sample_starting_balance: number;
  requested_amount: number;
  comparisons: PolyComparison[];
}

interface TestCaseResult {
  case_id: string;
  test_type: string;
  scenario: string;
  user_input: string;
  expected_output: string;
  actual_output: string;
  result: string;
}

interface SourceFileItem {
  path: string;
  label: string;
  language: string;
  content: string;
}

type NavTab = 'terminal' | 'polymorphism' | 'uml' | 'source';
type QuickActionMode = 'deposit' | 'withdraw' | 'create';

function formatPHP(amount: number): string {
  return amount.toLocaleString('en-PH', {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

export default function App() {
  const [activeTab, setActiveTab] = useState<NavTab>('terminal');
  const [actionMode, setActionMode] = useState<QuickActionMode>('deposit');

  const [pythonVersion, setPythonVersion] = useState<string>('3.10.12');
  const [activeAccount, setActiveAccount] = useState<AccountData | null>(null);
  const [accounts, setAccounts] = useState<AccountData[]>([]);
  const [feedback, setFeedback] = useState<FeedbackMessage | null>(null);
  const [polyDemo, setPolyDemo] = useState<PolyDemoData | null>(null);
  const [testCases, setTestCases] = useState<TestCaseResult[]>([]);
  const [sourceFiles, setSourceFiles] = useState<SourceFileItem[]>([]);
  const [selectedFileIndex, setSelectedFileIndex] = useState<number>(0);
  const [copiedPath, setCopiedPath] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);

  // Form states
  const [depositAmount, setDepositAmount] = useState<string>('');
  const [depositNote, setDepositNote] = useState<string>('');
  const [withdrawAmount, setWithdrawAmount] = useState<string>('');
  const [withdrawNote, setWithdrawNote] = useState<string>('');
  const [newHolderName, setNewHolderName] = useState<string>('');
  const [newAccountKind, setNewAccountKind] = useState<string>('savings');
  const [newStartingBalance, setNewStartingBalance] = useState<string>('5000');
  const [polyTestAmount, setPolyTestAmount] = useState<string>('2000');
  const [polySampleBalance, setPolySampleBalance] = useState<string>('10000');

  async function callPythonBackend(payload: Record<string, unknown>) {
    setIsLoading(true);
    try {
      const response = await fetch('/api/atm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
      const data = await response.json();
      if (data.active_account) {
        setPythonVersion(data.python_version || '3.10.12');
        setActiveAccount(data.active_account);
        setAccounts(data.accounts || []);
        if (data.feedback) {
          setFeedback(data.feedback);
        }
        if (data.poly_demo) {
          setPolyDemo(data.poly_demo);
        }
        if (data.test_cases) {
          setTestCases(data.test_cases);
        }
      }
    } catch (err) {
      setFeedback({
        status: 'error',
        title: 'Communication Error',
        message: err instanceof Error ? err.message : 'Unable to reach Python OOP backend.',
      });
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    callPythonBackend({ action: 'state' });
    fetch('/api/source-files')
      .then((res) => res.json())
      .then((data) => {
        if (data.files) {
          setSourceFiles(data.files);
        }
      })
      .catch(() => {});
  }, []);

  const handleDepositSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    callPythonBackend({
      action: 'deposit',
      amount: depositAmount,
      note: depositNote || 'Cash Deposit via Express ATM',
    });
    setDepositAmount('');
    setDepositNote('');
  };

  const handleWithdrawSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    callPythonBackend({
      action: 'withdraw',
      amount: withdrawAmount,
      note: withdrawNote || 'ATM Cash Withdrawal',
    });
    setWithdrawAmount('');
    setWithdrawNote('');
  };

  const handleCreateAccountSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    callPythonBackend({
      action: 'create',
      holder_name: newHolderName,
      account_kind: newAccountKind,
      starting_balance: newStartingBalance,
    });
    setNewHolderName('');
  };

  const handlePolySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    callPythonBackend({
      action: 'polymorphism',
      test_amount: polyTestAmount,
      sample_balance: Number(polySampleBalance) || 10000,
    });
  };

  const handleCopyCode = (pathStr: string, code: string) => {
    navigator.clipboard.writeText(code);
    setCopiedPath(pathStr);
    setTimeout(() => setCopiedPath(''), 2000);
  };

  return (
    <div className="min-h-screen flex flex-col">
      {/* Top Bar Contract: Strictly 3 Zones separated by gap-8 */}
      <header className="sticky top-0 z-40 flex items-center justify-between gap-8 px-6 py-3.5 bg-white/80 backdrop-blur-xl border-b border-sky-200/70">
        {/* Zone 1: Single text element Brand wordmark */}
        <a
          href="#top"
          onClick={(e) => {
            e.preventDefault();
            setActiveTab('terminal');
          }}
          className="text-xl font-extrabold tracking-tight text-slate-900 whitespace-nowrap shrink-0"
          style={{ fontFamily: 'var(--font-display)' }}
        >
          CTU Express ATM
        </a>

        {/* Zone 2: 4 concise single-line text navigation links */}
        <nav className="hidden md:flex items-center gap-7 text-sm font-bold text-slate-600">
          <button
            type="button"
            onClick={() => setActiveTab('terminal')}
            className={`py-1 border-b-2 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeTab === 'terminal'
                ? 'text-sky-600 border-sky-500'
                : 'border-transparent hover:text-slate-900'
            }`}
          >
            ATM Simulator
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('polymorphism')}
            className={`py-1 border-b-2 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeTab === 'polymorphism'
                ? 'text-sky-600 border-sky-500'
                : 'border-transparent hover:text-slate-900'
            }`}
          >
            Polymorphism Lab
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('uml')}
            className={`py-1 border-b-2 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeTab === 'uml'
                ? 'text-sky-600 border-sky-500'
                : 'border-transparent hover:text-slate-900'
            }`}
          >
            UML &amp; 6 Test Cases
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('source')}
            className={`py-1 border-b-2 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeTab === 'source'
                ? 'text-sky-600 border-sky-500'
                : 'border-transparent hover:text-slate-900'
            }`}
          >
            Python &amp; Django Code
          </button>
        </nav>

        {/* Zone 3: 1 Primary Action Button */}
        <div className="flex items-center gap-3 shrink-0">
          <a
            href="/CTU_PELEC1_ATM_Simulator_Django.zip"
            download="CTU_PELEC1_ATM_Simulator_Django.zip"
            className="glass-solid-blue px-4 py-2 rounded-xl text-xs font-bold tracking-tight inline-flex items-center gap-2 whitespace-nowrap shrink-0 transition-transform active:scale-95"
            style={{ fontFamily: 'var(--font-display)' }}
          >
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
              <polyline points="7 10 12 15 17 10" />
              <line x1="12" y1="15" x2="12" y2="3" />
            </svg>
            Download Django ZIP
          </a>
        </div>
      </header>

      {/* Mobile Navigation Bar */}
      <div className="flex md:hidden items-center justify-around bg-white/75 backdrop-blur-md border-b border-sky-200/70 px-3 py-2 text-xs font-bold">
        <button
          type="button"
          onClick={() => setActiveTab('terminal')}
          className={`px-3 py-1.5 rounded-lg whitespace-nowrap ${
            activeTab === 'terminal' ? 'bg-sky-500 text-white' : 'text-slate-700'
          }`}
        >
          ATM Terminal
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('polymorphism')}
          className={`px-3 py-1.5 rounded-lg whitespace-nowrap ${
            activeTab === 'polymorphism' ? 'bg-sky-500 text-white' : 'text-slate-700'
          }`}
        >
          Polymorphism
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('uml')}
          className={`px-3 py-1.5 rounded-lg whitespace-nowrap ${
            activeTab === 'uml' ? 'bg-sky-500 text-white' : 'text-slate-700'
          }`}
        >
          UML &amp; Tests
        </button>
        <button
          type="button"
          onClick={() => setActiveTab('source')}
          className={`px-3 py-1.5 rounded-lg whitespace-nowrap ${
            activeTab === 'source' ? 'bg-sky-500 text-white' : 'text-slate-700'
          }`}
        >
          Django Files
        </button>
      </div>

      {/* Main Content Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-7">
        {/* Top Context Strip */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-6 pb-4 border-b border-sky-200/70">
          <div className="text-xs font-semibold text-slate-600 flex flex-wrap items-center gap-2">
            <span className="font-bold text-sky-900">Cebu Technological University · P ELEC 1 Final Project</span>
            <span aria-hidden="true">·</span>
            <span>Option C: ATM Simulator</span>
            <span aria-hidden="true">·</span>
            <span>Python {pythonVersion} OOP Engine + Django Session Architecture</span>
          </div>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => callPythonBackend({ action: 'inquire' })}
              className="glass-soft-blue-btn px-3.5 py-1.5 rounded-xl text-xs font-bold inline-flex items-center gap-1.5 cursor-pointer whitespace-nowrap"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="12" cy="12" r="10" />
                <line x1="12" y1="16" x2="12" y2="12" />
                <line x1="12" y1="8" x2="12.01" y2="8" />
              </svg>
              Balance Inquiry
            </button>
            <button
              type="button"
              onClick={() => callPythonBackend({ action: 'reset' })}
              className="glass-soft-blue-btn px-3.5 py-1.5 rounded-xl text-xs font-bold inline-flex items-center gap-1.5 cursor-pointer whitespace-nowrap"
            >
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="1 4 1 10 7 10" />
                <path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10" />
              </svg>
              Reset Session
            </button>
          </div>
        </div>

        {/* Feedback Alert Banner (Custom Exception & Operation Status) */}
        {feedback && (
          <div
            role="status"
            className={`mb-6 p-4 rounded-2xl backdrop-blur-md flex items-start justify-between gap-4 border ${
              feedback.status === 'error'
                ? 'bg-red-50/90 border-red-300 text-red-900'
                : feedback.status === 'success'
                ? 'bg-sky-50/95 border-sky-300 text-sky-950'
                : 'bg-white/90 border-sky-300 text-slate-900'
            }`}
          >
            <div className="flex items-start gap-3.5">
              <div
                className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 mt-0.5 ${
                  feedback.status === 'error'
                    ? 'bg-red-100 text-red-700'
                    : 'bg-sky-100 text-sky-700'
                }`}
              >
                {feedback.status === 'error' ? (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="12" y1="8" x2="12" y2="12" />
                    <line x1="12" y1="16" x2="12.01" y2="16" />
                  </svg>
                ) : (
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14" />
                    <polyline points="22 4 12 14.01 9 11.01" />
                  </svg>
                )}
              </div>
              <div>
                <div className="font-extrabold text-sm sm:text-base" style={{ fontFamily: 'var(--font-display)' }}>
                  {feedback.title}
                </div>
                <p className="text-xs sm:text-sm mt-0.5 font-medium leading-relaxed">
                  {feedback.message}
                </p>
              </div>
            </div>
            <button
              type="button"
              onClick={() => setFeedback(null)}
              className="text-xs font-bold opacity-60 hover:opacity-100 px-2 py-1 cursor-pointer"
              aria-label="Dismiss notification"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* ================================================================
            TAB 1: ATM SIMULATOR TERMINAL (SCREENSHOT-INSPIRED UI)
           ================================================================ */}
        {activeTab === 'terminal' && activeAccount && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-7 items-stretch">
            {/* LEFT COLUMN: Screenshot-inspired Account Profile, 3-Tile Action Grid, Wallet Card & Rules */}
            <section className="lg:col-span-5 glass-surface rounded-3xl p-6 sm:p-7 flex flex-col justify-between">
              <div>
                {/* Top Header Row ("Account" + Gear/Inquire Circle Icon from Screenshot) */}
                <div className="flex items-center justify-between pb-4 mb-5 border-b border-sky-200/60">
                  <span
                    className="text-lg font-extrabold tracking-tight text-slate-900"
                    style={{ fontFamily: 'var(--font-display)' }}
                  >
                    Account
                  </span>
                  <button
                    type="button"
                    onClick={() => callPythonBackend({ action: 'inquire' })}
                    title="Execute Account.inquire_balance()"
                    className="w-11 h-11 rounded-full bg-white/90 border border-sky-200 flex items-center justify-center text-sky-700 hover:bg-sky-50 transition-colors shadow-xs cursor-pointer"
                  >
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                      <circle cx="12" cy="12" r="3" />
                      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
                    </svg>
                  </button>
                </div>

                {/* Holder Name & Subtitle ("Hanz Dee" / "View profile" typography from Screenshot) */}
                <div className="mb-5">
                  <h1
                    className="text-3xl sm:text-4xl font-extrabold tracking-tight text-slate-900 leading-tight"
                    style={{ fontFamily: 'var(--font-display)' }}
                  >
                    {activeAccount.holder_name}
                  </h1>
                  <p className="text-sm font-bold text-sky-800 mt-1">
                    {activeAccount.account_type} · {activeAccount.account_number} · Python {activeAccount.class_name}
                  </p>
                </div>

                {/* 3-Column Rounded Action Tile Grid ("Orders / Favourites / Addresses" layout from Screenshot) */}
                <div className="grid grid-cols-3 gap-3 mb-6">
                  <button
                    type="button"
                    onClick={() => setActionMode('deposit')}
                    className={`glass-tile rounded-2xl py-4 px-2 flex flex-col items-center justify-center gap-2 cursor-pointer ${
                      actionMode === 'deposit' ? 'active-tile ring-2 ring-sky-400/50' : ''
                    }`}
                  >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth="2.1" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M12 3v12" />
                      <polyline points="8 11 12 15 16 11" />
                      <rect x="4" y="17" width="16" height="4" rx="1" />
                    </svg>
                    <span
                      className="text-sm font-extrabold text-slate-900 whitespace-nowrap"
                      style={{ fontFamily: 'var(--font-display)' }}
                    >
                      Deposit
                    </span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActionMode('withdraw')}
                    className={`glass-tile rounded-2xl py-4 px-2 flex flex-col items-center justify-center gap-2 cursor-pointer ${
                      actionMode === 'withdraw' ? 'active-tile ring-2 ring-sky-400/50' : ''
                    }`}
                  >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth="2.1" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M12 15V3" />
                      <polyline points="8 7 12 3 16 7" />
                      <rect x="4" y="17" width="16" height="4" rx="1" />
                    </svg>
                    <span
                      className="text-sm font-extrabold text-slate-900 whitespace-nowrap"
                      style={{ fontFamily: 'var(--font-display)' }}
                    >
                      Withdraw
                    </span>
                  </button>

                  <button
                    type="button"
                    onClick={() => setActionMode('create')}
                    className={`glass-tile rounded-2xl py-4 px-2 flex flex-col items-center justify-center gap-2 cursor-pointer ${
                      actionMode === 'create' ? 'active-tile ring-2 ring-sky-400/50' : ''
                    }`}
                  >
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth="2.1" strokeLinecap="round" strokeLinejoin="round">
                      <path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2" />
                      <circle cx="8.5" cy="7" r="4" />
                      <line x1="20" y1="8" x2="20" y2="14" />
                      <line x1="23" y1="11" x2="17" y2="11" />
                    </svg>
                    <span
                      className="text-sm font-extrabold text-slate-900 whitespace-nowrap"
                      style={{ fontFamily: 'var(--font-display)' }}
                    >
                      New Account
                    </span>
                  </button>
                </div>

                {/* Wallet Section ("Wallet" + "pandapay ₱ 0.00" Pill Card from Screenshot) */}
                <div className="mb-6">
                  <h2
                    className="text-xl font-extrabold tracking-tight text-slate-900 mb-3"
                    style={{ fontFamily: 'var(--font-display)' }}
                  >
                    Wallet
                  </h2>
                  <div className="glass-wallet-banner rounded-2xl p-4 sm:px-5 flex items-center justify-between gap-3">
                    <div className="flex items-center gap-3">
                      <span
                        className="px-2.5 py-1 rounded-lg border-2 border-sky-600 bg-sky-100/80 text-sky-700 text-xs font-extrabold tracking-tight inline-flex items-center gap-1"
                        style={{ fontFamily: 'var(--font-display)' }}
                      >
                        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                          <rect x="2" y="5" width="20" height="14" rx="2" />
                          <line x1="2" y1="10" x2="22" y2="10" />
                        </svg>
                        ctupay
                      </span>
                      <div>
                        <div
                          className="text-base font-extrabold text-slate-900 leading-tight"
                          style={{ fontFamily: 'var(--font-display)' }}
                        >
                          {activeAccount.account_type}
                        </div>
                        <div className="text-xs font-semibold text-slate-500">
                          Max withdrawable now: ₱ {formatPHP(activeAccount.max_withdrawable)}
                        </div>
                      </div>
                    </div>
                    <div
                      className="text-xl sm:text-2xl font-extrabold text-slate-900 tabular-nums whitespace-nowrap"
                      style={{ fontFamily: 'var(--font-display)' }}
                    >
                      ₱ {formatPHP(activeAccount.balance)}
                    </div>
                  </div>
                </div>

                {/* Polymorphic Account Rules ("Perks for you" Clean Divided Row Style from Screenshot) */}
                <div className="mb-6">
                  <h2
                    className="text-xl font-extrabold tracking-tight text-slate-900 mb-2"
                    style={{ fontFamily: 'var(--font-display)' }}
                  >
                    Polymorphic Rules ({activeAccount.class_name})
                  </h2>
                  <div className="divide-y divide-sky-200/70 border-t border-b border-sky-200/70">
                    <div className="py-3.5 flex items-center justify-between gap-3">
                      <div className="flex items-center gap-3.5">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
                        </svg>
                        <div>
                          <div className="text-sm font-extrabold text-slate-900" style={{ fontFamily: 'var(--font-display)' }}>
                            Minimum Maintaining Balance
                          </div>
                          <div className="text-xs font-medium text-slate-500">
                            Protected inside {activeAccount.class_name}.withdraw()
                          </div>
                        </div>
                      </div>
                      <span className="text-sm font-extrabold text-slate-900 tabular-nums whitespace-nowrap">
                        ₱ {formatPHP(activeAccount.rules.maintaining_balance)}
                      </span>
                    </div>

                    <div className="py-3.5 flex items-center justify-between gap-3">
                      <div className="flex items-center gap-3.5">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <rect x="2" y="5" width="20" height="14" rx="2" />
                          <line x1="2" y1="10" x2="22" y2="10" />
                        </svg>
                        <div>
                          <div className="text-sm font-extrabold text-slate-900" style={{ fontFamily: 'var(--font-display)' }}>
                            Single Withdrawal Limit
                          </div>
                          <div className="text-xs font-medium text-slate-500">
                            Raises WithdrawalLimitError if exceeded
                          </div>
                        </div>
                      </div>
                      <span className="text-sm font-extrabold text-slate-900 tabular-nums whitespace-nowrap">
                        ₱ {formatPHP(activeAccount.rules.per_tx_limit)}
                      </span>
                    </div>

                    <div className="py-3.5 flex items-center justify-between gap-3">
                      <div className="flex items-center gap-3.5">
                        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#0284c7" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <line x1="12" y1="1" x2="12" y2="23" />
                          <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6" />
                        </svg>
                        <div>
                          <div className="text-sm font-extrabold text-slate-900" style={{ fontFamily: 'var(--font-display)' }}>
                            Withdrawal Processing Fee
                          </div>
                          <div className="text-xs font-medium text-slate-500">
                            {activeAccount.rules.withdrawal_fee > 0
                              ? 'Flat checking fee deducted per withdrawal'
                              : 'Free withdrawal for SavingsAccount'}
                          </div>
                        </div>
                      </div>
                      <span className="text-sm font-extrabold text-sky-700 tabular-nums whitespace-nowrap">
                        ₱ {formatPHP(activeAccount.rules.withdrawal_fee)}
                      </span>
                    </div>
                  </div>
                </div>
              </div>

              {/* Predefined & Session Account Switcher ("General" section style) */}
              <div>
                <h2
                  className="text-lg font-extrabold tracking-tight text-slate-900 mb-2.5"
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  Switch Fictional Account
                </h2>
                <div className="space-y-2">
                  {accounts.map((acc) => {
                    const isSelected = acc.account_number === activeAccount.account_number;
                    return (
                      <button
                        key={acc.account_number}
                        type="button"
                        onClick={() =>
                          callPythonBackend({
                            action: 'switch',
                            account_number: acc.account_number,
                          })
                        }
                        className={`w-full text-left p-3.5 rounded-2xl border transition-all flex items-center justify-between gap-3 cursor-pointer ${
                          isSelected
                            ? 'glass-solid-blue'
                            : 'bg-white/80 hover:bg-sky-50/90 border-sky-200/80 text-slate-900'
                        }`}
                      >
                        <div className="flex items-center gap-3 min-w-0">
                          <div
                            className={`w-9 h-9 rounded-xl flex items-center justify-center shrink-0 ${
                              isSelected ? 'bg-white/20 text-white' : 'bg-sky-100 text-sky-700'
                            }`}
                          >
                            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.1" strokeLinecap="round" strokeLinejoin="round">
                              <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                              <circle cx="12" cy="7" r="4" />
                            </svg>
                          </div>
                          <div className="truncate">
                            <div
                              className="text-sm font-extrabold truncate"
                              style={{ fontFamily: 'var(--font-display)' }}
                            >
                              {acc.holder_name} · {acc.account_type}
                            </div>
                            <div className={`text-xs font-medium ${isSelected ? 'text-sky-100' : 'text-slate-500'}`}>
                              {acc.account_number} · {acc.class_name}
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center gap-2 shrink-0">
                          <span className="text-sm font-extrabold tabular-nums">
                            ₱ {formatPHP(acc.balance)}
                          </span>
                          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
                            <polyline points="9 18 15 12 9 6" />
                          </svg>
                        </div>
                      </button>
                    );
                  })}
                </div>
              </div>
            </section>

            {/* RIGHT COLUMN: Interactive Transaction Forms, Defense Quick Test Presets & Session History */}
            <section className="lg:col-span-7 flex flex-col gap-6">
              {/* Transaction Operation Deck */}
              <div className="glass-surface rounded-3xl p-6 sm:p-7">
                <div className="flex flex-wrap items-center justify-between gap-3 pb-4 mb-5 border-b border-sky-200/70">
                  <div>
                    <h2
                      className="text-2xl font-extrabold tracking-tight text-slate-900"
                      style={{ fontFamily: 'var(--font-display)' }}
                    >
                      {actionMode === 'deposit' && 'Deposit Cash to Account'}
                      {actionMode === 'withdraw' && `Withdraw Cash (${activeAccount.class_name})`}
                      {actionMode === 'create' && 'Create New Fictional Account'}
                    </h2>
                    <p className="text-xs font-semibold text-slate-500 mt-0.5">
                      {actionMode === 'deposit' &&
                        'Calls inherited Account.deposit(amount) in atm_app/oop_models.py'}
                      {actionMode === 'withdraw' &&
                        `Calls overridden ${activeAccount.class_name}.withdraw(amount) demonstrating Polymorphism`}
                      {actionMode === 'create' &&
                        'Instantiates a new SavingsAccount or CheckingAccount object in the active session'}
                    </p>
                  </div>

                  {/* Segmented Mode Switcher */}
                  <div className="flex items-center gap-1 p-1 bg-sky-100/80 rounded-xl border border-sky-200/80">
                    <button
                      type="button"
                      onClick={() => setActionMode('deposit')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-extrabold transition-colors cursor-pointer whitespace-nowrap ${
                        actionMode === 'deposit'
                          ? 'bg-white text-sky-900 shadow-xs'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      Deposit
                    </button>
                    <button
                      type="button"
                      onClick={() => setActionMode('withdraw')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-extrabold transition-colors cursor-pointer whitespace-nowrap ${
                        actionMode === 'withdraw'
                          ? 'bg-white text-sky-900 shadow-xs'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      Withdraw
                    </button>
                    <button
                      type="button"
                      onClick={() => setActionMode('create')}
                      className={`px-3 py-1.5 rounded-lg text-xs font-extrabold transition-colors cursor-pointer whitespace-nowrap ${
                        actionMode === 'create'
                          ? 'bg-white text-sky-900 shadow-xs'
                          : 'text-slate-600 hover:text-slate-900'
                      }`}
                    >
                      New Account
                    </button>
                  </div>
                </div>

                {/* DEPOSIT FORM */}
                {actionMode === 'deposit' && (
                  <form onSubmit={handleDepositSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="dep-amount" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                          Deposit Amount (PHP)
                        </label>
                        <input
                          id="dep-amount"
                          type="text"
                          value={depositAmount}
                          onChange={(e) => setDepositAmount(e.target.value)}
                          placeholder="e.g. 2500.00"
                          className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-bold text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                        />
                      </div>
                      <div>
                        <label htmlFor="dep-note" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                          Transaction Note (Optional)
                        </label>
                        <input
                          id="dep-note"
                          type="text"
                          value={depositNote}
                          onChange={(e) => setDepositNote(e.target.value)}
                          placeholder="e.g. Cash Deposit / Allowance"
                          className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-semibold text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                        />
                      </div>
                    </div>

                    {/* Quick Amount & Defense Validation Test Buttons */}
                    <div className="flex flex-wrap items-center gap-2 pt-1">
                      <span className="text-xs font-bold text-slate-500 mr-1">Quick Fill:</span>
                      {['500', '1000', '2500', '5000'].map((amt) => (
                        <button
                          key={amt}
                          type="button"
                          onClick={() => setDepositAmount(amt)}
                          className="glass-soft-blue-btn px-3 py-1 rounded-lg text-xs font-bold cursor-pointer"
                        >
                          +₱ {Number(amt).toLocaleString()}
                        </button>
                      ))}
                      <button
                        type="button"
                        onClick={() => setDepositAmount('-500')}
                        className="px-3 py-1 rounded-lg text-xs font-bold bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 cursor-pointer"
                      >
                        Test Invalid (-500)
                      </button>
                      <button
                        type="button"
                        onClick={() => setDepositAmount('abc')}
                        className="px-3 py-1 rounded-lg text-xs font-bold bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 cursor-pointer"
                      >
                        Test Non-Numeric (abc)
                      </button>
                    </div>

                    <div className="pt-2">
                      <button
                        type="submit"
                        disabled={isLoading}
                        className="glass-solid-blue w-full py-3.5 px-6 rounded-xl font-extrabold text-sm inline-flex items-center justify-center gap-2 cursor-pointer"
                        style={{ fontFamily: 'var(--font-display)' }}
                      >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M12 3v12" />
                          <polyline points="8 11 12 15 16 11" />
                          <rect x="4" y="17" width="16" height="4" rx="1" />
                        </svg>
                        Confirm Deposit via Account.deposit()
                      </button>
                    </div>
                  </form>
                )}

                {/* WITHDRAW FORM */}
                {actionMode === 'withdraw' && (
                  <form onSubmit={handleWithdrawSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                      <div>
                        <label htmlFor="wd-amount" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                          Withdrawal Amount (PHP)
                        </label>
                        <input
                          id="wd-amount"
                          type="text"
                          value={withdrawAmount}
                          onChange={(e) => setWithdrawAmount(e.target.value)}
                          placeholder="e.g. 1500.00"
                          className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-bold text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                        />
                      </div>
                      <div>
                        <label htmlFor="wd-note" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                          Withdrawal Note (Optional)
                        </label>
                        <input
                          id="wd-note"
                          type="text"
                          value={withdrawNote}
                          onChange={(e) => setWithdrawNote(e.target.value)}
                          placeholder="e.g. ATM Cash Dispense"
                          className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-semibold text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                        />
                      </div>
                    </div>

                    {/* Quick Fill & Exception Test Triggers */}
                    <div className="flex flex-wrap items-center gap-2 pt-1">
                      <span className="text-xs font-bold text-slate-500 mr-1">Quick Fill:</span>
                      {['500', '1500', '3000', String(activeAccount.max_withdrawable)].map((amt, idx) => (
                        <button
                          key={`${amt}-${idx}`}
                          type="button"
                          onClick={() => setWithdrawAmount(amt)}
                          className="glass-soft-blue-btn px-3 py-1 rounded-lg text-xs font-bold cursor-pointer"
                        >
                          {idx === 3 ? `Max (₱ ${formatPHP(Number(amt))})` : `₱ ${Number(amt).toLocaleString()}`}
                        </button>
                      ))}
                      <button
                        type="button"
                        onClick={() => setWithdrawAmount(String(activeAccount.balance))}
                        className="px-3 py-1 rounded-lg text-xs font-bold bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 cursor-pointer"
                      >
                        Test Rule Violation (₱ {formatPHP(activeAccount.balance)})
                      </button>
                      <button
                        type="button"
                        onClick={() => setWithdrawAmount('60000')}
                        className="px-3 py-1 rounded-lg text-xs font-bold bg-red-50 text-red-700 border border-red-200 hover:bg-red-100 cursor-pointer"
                      >
                        Test Limit (60,000)
                      </button>
                    </div>

                    <div className="pt-2">
                      <button
                        type="submit"
                        disabled={isLoading}
                        className="glass-solid-blue w-full py-3.5 px-6 rounded-xl font-extrabold text-sm inline-flex items-center justify-center gap-2 cursor-pointer"
                        style={{ fontFamily: 'var(--font-display)' }}
                      >
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M12 15V3" />
                          <polyline points="8 7 12 3 16 7" />
                          <rect x="4" y="17" width="16" height="4" rx="1" />
                        </svg>
                        Process Withdrawal via {activeAccount.class_name}.withdraw()
                      </button>
                    </div>
                  </form>
                )}

                {/* CREATE CUSTOM ACCOUNT FORM */}
                {actionMode === 'create' && (
                  <form onSubmit={handleCreateAccountSubmit} className="space-y-4">
                    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                      <div>
                        <label htmlFor="holder-name" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                          Account Holder Name
                        </label>
                        <input
                          id="holder-name"
                          type="text"
                          value={newHolderName}
                          onChange={(e) => setNewHolderName(e.target.value)}
                          placeholder="e.g. Juan Dela Cruz"
                          className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-bold text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                          required
                        />
                      </div>
                      <div>
                        <label htmlFor="acc-kind" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                          Python Child Class
                        </label>
                        <select
                          id="acc-kind"
                          value={newAccountKind}
                          onChange={(e) => setNewAccountKind(e.target.value)}
                          className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-bold text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                        >
                          <option value="savings">SavingsAccount (Min ₱500)</option>
                          <option value="checking">CheckingAccount (+₱15 Fee)</option>
                        </select>
                      </div>
                      <div>
                        <label htmlFor="start-bal" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                          Starting Balance (PHP)
                        </label>
                        <input
                          id="start-bal"
                          type="text"
                          value={newStartingBalance}
                          onChange={(e) => setNewStartingBalance(e.target.value)}
                          placeholder="e.g. 5000.00"
                          className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-bold text-sm focus:outline-none focus:ring-2 focus:ring-sky-500"
                          required
                        />
                      </div>
                    </div>
                    <button
                      type="submit"
                      disabled={isLoading}
                      className="glass-solid-blue w-full py-3.5 px-6 rounded-xl font-extrabold text-sm inline-flex items-center justify-center gap-2 cursor-pointer"
                      style={{ fontFamily: 'var(--font-display)' }}
                    >
                      Instantiate New Account Object
                    </button>
                  </form>
                )}
              </div>

              {/* Active Session Transaction History Table */}
              <div className="glass-surface rounded-3xl p-6 sm:p-7 flex-1">
                <div className="flex items-center justify-between gap-4 mb-4">
                  <div>
                    <h2
                      className="text-xl font-extrabold tracking-tight text-slate-900"
                      style={{ fontFamily: 'var(--font-display)' }}
                    >
                      Session Transaction History
                    </h2>
                    <p className="text-xs font-semibold text-slate-500">
                      Encapsulated Transaction objects recorded on {activeAccount.account_number} ({activeAccount.transactions.length} entries)
                    </p>
                  </div>
                </div>

                <div className="overflow-x-auto">
                  <table className="w-full text-left border-collapse">
                    <thead>
                      <tr className="border-b border-sky-200/80 text-xs font-extrabold text-slate-600">
                        <th className="py-3 px-3">Reference</th>
                        <th className="py-3 px-3">Operation &amp; Note</th>
                        <th className="py-3 px-3">Timestamp</th>
                        <th className="py-3 px-3 text-right">Amount</th>
                        <th className="py-3 px-3 text-right">Fee</th>
                        <th className="py-3 px-3 text-right">Balance After</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-sky-200/50 text-sm">
                      {activeAccount.transactions.map((tx) => (
                        <tr key={tx.transaction_id} className="hover:bg-sky-50/50 transition-colors">
                          <td className="py-3.5 px-3 font-mono text-xs font-bold text-sky-900 whitespace-nowrap">
                            {tx.transaction_id}
                          </td>
                          <td className="py-3.5 px-3">
                            <div className="font-extrabold text-slate-900" style={{ fontFamily: 'var(--font-display)' }}>
                              {tx.tx_type}
                            </div>
                            <div className="text-xs font-medium text-slate-500">{tx.note}</div>
                          </td>
                          <td className="py-3.5 px-3 text-xs font-semibold text-slate-500 whitespace-nowrap">
                            {tx.timestamp}
                          </td>
                          <td className="py-3.5 px-3 text-right font-extrabold tabular-nums text-slate-900 whitespace-nowrap">
                            ₱ {formatPHP(tx.amount)}
                          </td>
                          <td className="py-3.5 px-3 text-right font-semibold tabular-nums text-slate-600 whitespace-nowrap">
                            ₱ {formatPHP(tx.fee)}
                          </td>
                          <td className="py-3.5 px-3 text-right font-extrabold tabular-nums text-sky-700 whitespace-nowrap">
                            ₱ {formatPHP(tx.balance_after)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            </section>
          </div>
        )}

        {/* ================================================================
            TAB 2: POLYMORPHISM LAB (SAVINGS vs CHECKING withdraw() DEMO)
           ================================================================ */}
        {activeTab === 'polymorphism' && (
          <div className="space-y-7">
            <div className="glass-surface rounded-3xl p-6 sm:p-8">
              <div className="max-w-3xl mb-6">
                <h1
                  className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900"
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  Interactive Polymorphism Verifier: Overridden withdraw()
                </h1>
                <p className="text-sm font-medium text-slate-600 mt-1.5 leading-relaxed">
                  Part III &amp; Part IX Requirement: Run the exact same overridden method{' '}
                  <code className="font-mono font-bold text-sky-800">account.withdraw(amount)</code> on two child-class
                  objects (<code className="font-mono font-bold text-sky-800">SavingsAccount</code> and{' '}
                  <code className="font-mono font-bold text-sky-800">CheckingAccount</code>) through a common{' '}
                  <code className="font-mono font-bold text-sky-800">Account</code> reference and verify distinct results.
                </p>
              </div>

              <form onSubmit={handlePolySubmit} className="grid grid-cols-1 sm:grid-cols-3 gap-4 items-end mb-7">
                <div>
                  <label htmlFor="poly-bal" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                    Identical Starting Balance (PHP)
                  </label>
                  <input
                    id="poly-bal"
                    type="text"
                    value={polySampleBalance}
                    onChange={(e) => setPolySampleBalance(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-bold text-sm"
                  />
                </div>
                <div>
                  <label htmlFor="poly-amt" className="block text-xs font-extrabold text-slate-700 mb-1.5">
                    Test Withdrawal Amount Passed to withdraw(amount)
                  </label>
                  <input
                    id="poly-amt"
                    type="text"
                    value={polyTestAmount}
                    onChange={(e) => setPolyTestAmount(e.target.value)}
                    className="w-full px-4 py-3 rounded-xl bg-white/95 border border-sky-300 text-slate-900 font-bold text-sm"
                  />
                </div>
                <button
                  type="submit"
                  className="glass-solid-blue py-3 px-6 rounded-xl font-extrabold text-sm cursor-pointer h-[46px]"
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  Run Polymorphic Comparison in Python
                </button>
              </form>

              {/* Quick Scenario Presets */}
              <div className="flex flex-wrap items-center gap-2 mb-6">
                <span className="text-xs font-bold text-slate-500">Test Scenarios:</span>
                <button
                  type="button"
                  onClick={() => {
                    setPolySampleBalance('10000');
                    setPolyTestAmount('2000');
                    callPythonBackend({ action: 'polymorphism', test_amount: '2000', sample_balance: 10000 });
                  }}
                  className="glass-soft-blue-btn px-3 py-1.5 rounded-lg text-xs font-bold cursor-pointer"
                >
                  Normal (₱2,000 from ₱10,000) — Shows ₱15 Fee Difference
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setPolySampleBalance('10000');
                    setPolyTestAmount('9700');
                    callPythonBackend({ action: 'polymorphism', test_amount: '9700', sample_balance: 10000 });
                  }}
                  className="glass-soft-blue-btn px-3 py-1.5 rounded-lg text-xs font-bold cursor-pointer"
                >
                  Maintaining Balance Boundary (₱9,700 from ₱10,000) — Savings Rejects, Checking Succeeds
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setPolySampleBalance('40000');
                    setPolyTestAmount('25000');
                    callPythonBackend({ action: 'polymorphism', test_amount: '25000', sample_balance: 40000 });
                  }}
                  className="glass-soft-blue-btn px-3 py-1.5 rounded-lg text-xs font-bold cursor-pointer"
                >
                  Per-Withdrawal Limit (₱25,000 from ₱40,000) — Savings Rejects (&gt;20k), Checking Succeeds
                </button>
              </div>

              {polyDemo && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  {polyDemo.comparisons.map((item) => (
                    <div
                      key={item.class_name}
                      className="glass-wallet-banner rounded-2xl p-6 border border-sky-300/90 flex flex-col justify-between"
                    >
                      <div>
                        <div className="flex items-center justify-between gap-2 pb-3 mb-4 border-b border-sky-200/80">
                          <div>
                            <h3
                              className="text-xl font-extrabold text-slate-900"
                              style={{ fontFamily: 'var(--font-display)' }}
                            >
                              {item.class_name}.withdraw({formatPHP(item.requested_withdrawal)})
                            </h3>
                            <p className="text-xs font-semibold text-slate-500">
                              Child Class of Account · {item.account_type}
                            </p>
                          </div>
                          <span
                            className={`text-xs font-extrabold px-2.5 py-1 rounded-lg ${
                              item.status === 'SUCCESS'
                                ? 'bg-sky-100 text-sky-800'
                                : 'bg-red-100 text-red-800'
                            }`}
                          >
                            {item.status}
                          </span>
                        </div>

                        <div className="space-y-2.5 text-sm mb-4">
                          <div className="flex justify-between">
                            <span className="text-slate-600 font-semibold">Starting Balance:</span>
                            <span className="font-bold tabular-nums">₱ {formatPHP(item.starting_balance)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-600 font-semibold">Requested Withdrawal:</span>
                            <span className="font-bold tabular-nums">₱ {formatPHP(item.requested_withdrawal)}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-slate-600 font-semibold">Polymorphic Processing Fee:</span>
                            <span className="font-bold tabular-nums text-sky-700">₱ {formatPHP(item.fee_charged)}</span>
                          </div>
                          <div className="flex justify-between pt-2 border-t border-sky-200/70">
                            <span className="text-slate-900 font-extrabold">Resulting Ending Balance:</span>
                            <span className="text-lg font-extrabold tabular-nums text-sky-800">
                              ₱ {formatPHP(item.ending_balance)}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="p-3.5 rounded-xl bg-white/85 border border-sky-200/80 text-xs font-semibold text-slate-700 leading-relaxed">
                        {item.explanation}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* ================================================================
            TAB 3: UML CLASS DIAGRAM, OOP MAPPING & 6 DOCUMENTED TEST CASES
           ================================================================ */}
        {activeTab === 'uml' && (
          <div className="space-y-7">
            {/* Vector SVG UML Class Diagram */}
            <section className="glass-surface rounded-3xl p-6 sm:p-8">
              <h1
                className="text-2xl font-extrabold tracking-tight text-slate-900 mb-2"
                style={{ fontFamily: 'var(--font-display)' }}
              >
                UML Class Diagram &amp; Inheritance Architecture
              </h1>
              <p className="text-sm font-medium text-slate-600 mb-6">
                Part VI Requirement: UML class diagram showing the key classes, encapsulated attributes/methods, and inheritance relationships.
              </p>

              <div className="w-full overflow-x-auto bg-white/90 rounded-2xl border border-sky-200 p-4">
                <svg viewBox="0 0 980 470" className="w-full min-w-[780px] h-auto" role="img" aria-label="UML Class Diagram for ATM Simulator">
                  {/* Inheritance & Association Connector Lines */}
                  <line x1="490" y1="195" x2="490" y2="235" stroke="#0284c7" strokeWidth="2.5" />
                  <line x1="230" y1="235" x2="750" y2="235" stroke="#0284c7" strokeWidth="2.5" />
                  <line x1="230" y1="235" x2="230" y2="265" stroke="#0284c7" strokeWidth="2.5" />
                  <line x1="750" y1="235" x2="750" y2="265" stroke="#0284c7" strokeWidth="2.5" />
                  {/* Hollow Triangle for Inheritance ("is-a") */}
                  <polygon points="490,183 482,197 498,197" fill="#ffffff" stroke="#0284c7" strokeWidth="2.5" />

                  {/* Composition Line from Account to Transaction */}
                  <line x1="650" y1="95" x2="720" y2="95" stroke="#0284c7" strokeWidth="2" strokeDasharray="5,4" />

                  {/* Controller Line from ATMService to Account */}
                  <line x1="260" y1="95" x2="330" y2="95" stroke="#0284c7" strokeWidth="2" strokeDasharray="5,4" />

                  {/* Box 1: ATMService */}
                  <rect x="20" y="25" width="240" height="150" rx="12" fill="#f0f9ff" stroke="#0284c7" strokeWidth="2" />
                  <rect x="20" y="25" width="240" height="34" rx="12" fill="#0284c7" />
                  <text x="140" y="47" textAnchor="middle" fill="#ffffff" fontWeight="800" fontSize="14" fontFamily="Outfit, sans-serif">
                    ATMService (Controller)
                  </text>
                  <text x="32" y="78" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _accounts: Dict[str, Account]</text>
                  <text x="32" y="96" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _active_account_number: str</text>
                  <line x1="20" y1="108" x2="260" y2="108" stroke="#bae6fd" strokeWidth="1.5" />
                  <text x="32" y="126" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ perform_deposit(amount)</text>
                  <text x="32" y="144" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ perform_withdrawal(amount)</text>
                  <text x="32" y="162" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ demonstrate_polymorphism()</text>

                  {/* Box 2: Account (Parent Class) */}
                  <rect x="330" y="15" width="320" height="168" rx="12" fill="#ffffff" stroke="#0284c7" strokeWidth="2.5" />
                  <rect x="330" y="15" width="320" height="34" rx="12" fill="#0284c7" />
                  <text x="490" y="37" textAnchor="middle" fill="#ffffff" fontWeight="800" fontSize="14" fontFamily="Outfit, sans-serif">
                    Account (Parent Class)
                  </text>
                  <text x="344" y="68" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _account_number: str</text>
                  <text x="344" y="85" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _holder_name: str</text>
                  <text x="344" y="102" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _balance: float (@property)</text>
                  <text x="344" y="119" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _transactions: List[Transaction]</text>
                  <line x1="330" y1="128" x2="650" y2="128" stroke="#bae6fd" strokeWidth="1.5" />
                  <text x="344" y="146" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ deposit(raw_amount): Transaction</text>
                  <text x="344" y="163" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ withdraw(raw_amount): Transaction</text>
                  <text x="344" y="178" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ inquire_balance(): Dict</text>

                  {/* Box 3: Transaction */}
                  <rect x="720" y="25" width="240" height="150" rx="12" fill="#f0f9ff" stroke="#0284c7" strokeWidth="2" />
                  <rect x="720" y="25" width="240" height="34" rx="12" fill="#0284c7" />
                  <text x="840" y="47" textAnchor="middle" fill="#ffffff" fontWeight="800" fontSize="14" fontFamily="Outfit, sans-serif">
                    Transaction (Record)
                  </text>
                  <text x="732" y="78" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _transaction_id: str</text>
                  <text x="732" y="96" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _tx_type: str</text>
                  <text x="732" y="114" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _amount / _fee: float</text>
                  <text x="732" y="132" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">- _balance_after: float</text>
                  <line x1="720" y1="142" x2="960" y2="142" stroke="#bae6fd" strokeWidth="1.5" />
                  <text x="732" y="162" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ to_dict() / from_dict()</text>

                  {/* Box 4: Child Class 1 - SavingsAccount */}
                  <rect x="55" y="265" width="350" height="180" rx="12" fill="#f0f9ff" stroke="#0284c7" strokeWidth="2.2" />
                  <rect x="55" y="265" width="350" height="34" rx="12" fill="#0ea5e9" />
                  <text x="230" y="287" textAnchor="middle" fill="#ffffff" fontWeight="800" fontSize="14" fontFamily="Outfit, sans-serif">
                    SavingsAccount (Child of Account)
                  </text>
                  <text x="70" y="318" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ MAINTAINING_BALANCE = 500.00</text>
                  <text x="70" y="336" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ WITHDRAWAL_LIMIT = 20000.00</text>
                  <text x="70" y="354" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ WITHDRAWAL_FEE = 0.00</text>
                  <line x1="55" y1="366" x2="405" y2="366" stroke="#bae6fd" strokeWidth="1.5" />
                  <text x="70" y="388" fill="#0369a1" fontWeight="700" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ withdraw(raw_amount) [OVERRIDDEN]</text>
                  <text x="70" y="408" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ get_max_withdrawable() [OVERRIDDEN]</text>
                  <text x="70" y="428" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ get_rules_summary() [OVERRIDDEN]</text>

                  {/* Box 5: Child Class 2 - CheckingAccount */}
                  <rect x="575" y="265" width="350" height="180" rx="12" fill="#f0f9ff" stroke="#0284c7" strokeWidth="2.2" />
                  <rect x="575" y="265" width="350" height="34" rx="12" fill="#0ea5e9" />
                  <text x="750" y="287" textAnchor="middle" fill="#ffffff" fontWeight="800" fontSize="14" fontFamily="Outfit, sans-serif">
                    CheckingAccount (Child of Account)
                  </text>
                  <text x="590" y="318" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ MAINTAINING_BALANCE = 0.00</text>
                  <text x="590" y="336" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ WITHDRAWAL_LIMIT = 50000.00</text>
                  <text x="590" y="354" fill="#0b2239" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ WITHDRAWAL_FEE = 15.00</text>
                  <line x1="575" y1="366" x2="925" y2="366" stroke="#bae6fd" strokeWidth="1.5" />
                  <text x="590" y="388" fill="#0369a1" fontWeight="700" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ withdraw(raw_amount) [OVERRIDDEN]</text>
                  <text x="590" y="408" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ get_max_withdrawable() [OVERRIDDEN]</text>
                  <text x="590" y="428" fill="#0369a1" fontSize="11.5" fontFamily="JetBrains Mono, monospace">+ get_rules_summary() [OVERRIDDEN]</text>
                </svg>
              </div>
            </section>

            {/* OOP Implementation Summary Mapping Table */}
            <section className="glass-surface rounded-3xl p-6 sm:p-8">
              <h2
                className="text-2xl font-extrabold tracking-tight text-slate-900 mb-2"
                style={{ fontFamily: 'var(--font-display)' }}
              >
                Part III &amp; Part VI: Mandatory Python OOP Implementation Mapping
              </h2>
              <p className="text-sm font-medium text-slate-600 mb-5">
                Maps each required OOP concept to the exact Python file, class, and method for group presentation and individual defense.
              </p>

              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-sm">
                  <thead>
                    <tr className="border-b-2 border-sky-200 text-slate-700 font-extrabold">
                      <th className="py-3 px-3">OOP Concept</th>
                      <th className="py-3 px-3">Python File</th>
                      <th className="py-3 px-3">Classes Involved</th>
                      <th className="py-3 px-3">Methods / Evidence in Workflow</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-sky-200/60">
                    <tr>
                      <td className="py-3.5 px-3 font-extrabold text-sky-900">1. Classes &amp; Objects</td>
                      <td className="py-3.5 px-3 font-mono text-xs">atm_app/oop_models.py</td>
                      <td className="py-3.5 px-3 font-mono text-xs">Account, SavingsAccount, CheckingAccount, Transaction, ATMService</td>
                      <td className="py-3.5 px-3 text-slate-700">
                        5 meaningful classes instantiated and used across every deposit, withdrawal, balance inquiry, and session store.
                      </td>
                    </tr>
                    <tr>
                      <td className="py-3.5 px-3 font-extrabold text-sky-900">2. Encapsulation</td>
                      <td className="py-3.5 px-3 font-mono text-xs">atm_app/oop_models.py</td>
                      <td className="py-3.5 px-3 font-mono text-xs">Account, Transaction</td>
                      <td className="py-3.5 px-3 text-slate-700">
                        Internal attributes <code className="font-mono">_balance</code>, <code className="font-mono">_account_number</code>, <code className="font-mono">_transactions</code> protected with <code className="font-mono">@property</code> getters and validated mutators.
                      </td>
                    </tr>
                    <tr>
                      <td className="py-3.5 px-3 font-extrabold text-sky-900">3. Inheritance</td>
                      <td className="py-3.5 px-3 font-mono text-xs">atm_app/oop_models.py</td>
                      <td className="py-3.5 px-3 font-mono text-xs">Parent: Account · Children: SavingsAccount, CheckingAccount</td>
                      <td className="py-3.5 px-3 text-slate-700">
                        Both child classes call <code className="font-mono">super().__init__()</code> and inherit <code className="font-mono">deposit()</code>, <code className="font-mono">inquire_balance()</code>, and <code className="font-mono">_record_transaction()</code>.
                      </td>
                    </tr>
                    <tr>
                      <td className="py-3.5 px-3 font-extrabold text-sky-900">4. Polymorphism</td>
                      <td className="py-3.5 px-3 font-mono text-xs">atm_app/oop_models.py</td>
                      <td className="py-3.5 px-3 font-mono text-xs">SavingsAccount.withdraw() vs CheckingAccount.withdraw()</td>
                      <td className="py-3.5 px-3 text-slate-700">
                        Overridden <code className="font-mono">withdraw()</code> enforces ₱500 maintaining balance &amp; ₱0 fee on Savings vs. ₱0 maintaining balance &amp; ₱15 fee on Checking.
                      </td>
                    </tr>
                    <tr>
                      <td className="py-3.5 px-3 font-extrabold text-sky-900">5. Exception Handling</td>
                      <td className="py-3.5 px-3 font-mono text-xs">atm_app/oop_models.py &amp; views.py</td>
                      <td className="py-3.5 px-3 font-mono text-xs">ATMTransactionError, InvalidAmountError, InsufficientFundsError, MaintainingBalanceError, WithdrawalLimitError</td>
                      <td className="py-3.5 px-3 text-slate-700">
                        Custom exceptions raised on negative, zero, non-numeric, or overdraft inputs and caught in Django views while preserving balance.
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </section>

            {/* Six (6) Documented Test Cases Report (Executed Live by Python 3.10) */}
            <section className="glass-surface rounded-3xl p-6 sm:p-8">
              <div className="flex flex-wrap items-center justify-between gap-4 mb-5">
                <div>
                  <h2
                    className="text-2xl font-extrabold tracking-tight text-slate-900"
                    style={{ fontFamily: 'var(--font-display)' }}
                  >
                    Part VI &amp; Part IX: Six (6) Documented Test Cases Report
                  </h2>
                  <p className="text-sm font-medium text-slate-600">
                    Live verification executed directly by Python {pythonVersion} against <code className="font-mono">atm_app/oop_models.py</code>.
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() => callPythonBackend({ action: 'state' })}
                  className="glass-solid-blue px-4 py-2 rounded-xl text-xs font-extrabold cursor-pointer"
                >
                  Re-Run All 6 Test Cases in Python
                </button>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse text-sm">
                  <thead>
                    <tr className="border-b-2 border-sky-200 text-slate-700 font-extrabold">
                      <th className="py-3 px-3">ID &amp; Type</th>
                      <th className="py-3 px-3">Scenario</th>
                      <th className="py-3 px-3">Exact Input</th>
                      <th className="py-3 px-3">Expected Output</th>
                      <th className="py-3 px-3">Actual Output (Python {pythonVersion})</th>
                      <th className="py-3 px-3 text-right">Result</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-sky-200/60">
                    {testCases.map((tc) => (
                      <tr key={tc.case_id} className="hover:bg-sky-50/50">
                        <td className="py-3.5 px-3 whitespace-nowrap">
                          <div className="font-mono font-extrabold text-sky-900">{tc.case_id}</div>
                          <div className="text-xs font-bold text-slate-500">{tc.test_type}</div>
                        </td>
                        <td className="py-3.5 px-3 text-slate-800 font-medium">{tc.scenario}</td>
                        <td className="py-3.5 px-3 font-mono text-xs text-sky-900">{tc.user_input}</td>
                        <td className="py-3.5 px-3 text-xs text-slate-600">{tc.expected_output}</td>
                        <td className="py-3.5 px-3 text-xs font-semibold text-slate-800">{tc.actual_output}</td>
                        <td className="py-3.5 px-3 text-right font-extrabold text-emerald-700 whitespace-nowrap">
                          {tc.result}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </section>
          </div>
        )}

        {/* ================================================================
            TAB 4: PYTHON, DJANGO, HTML & CSS SOURCE CODE + ZIP DOWNLOAD
           ================================================================ */}
        {activeTab === 'source' && (
          <div className="space-y-6">
            <div className="glass-surface rounded-3xl p-6 sm:p-8">
              <div className="flex flex-wrap items-center justify-between gap-4 pb-5 mb-6 border-b border-sky-200/70">
                <div>
                  <h1
                    className="text-2xl font-extrabold tracking-tight text-slate-900"
                    style={{ fontFamily: 'var(--font-display)' }}
                  >
                    Runnable Django Source Code (Pure Python, HTML &amp; CSS)
                  </h1>
                  <p className="text-sm font-medium text-slate-600 mt-1">
                    Download the complete submission ZIP archive or inspect every file in <code className="font-mono font-bold text-sky-800">django_atm_project/</code>.
                  </p>
                </div>
                <a
                  href="/CTU_PELEC1_ATM_Simulator_Django.zip"
                  download="CTU_PELEC1_ATM_Simulator_Django.zip"
                  className="glass-solid-blue px-5 py-3 rounded-xl text-sm font-extrabold inline-flex items-center gap-2"
                  style={{ fontFamily: 'var(--font-display)' }}
                >
                  <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.3" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4" />
                    <polyline points="7 10 12 15 17 10" />
                    <line x1="12" y1="15" x2="12" y2="3" />
                  </svg>
                  Download CTU_PELEC1_ATM_Simulator_Django.zip
                </a>
              </div>

              {sourceFiles.length > 0 && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                  <div className="lg:col-span-4 space-y-2">
                    {sourceFiles.map((file, idx) => (
                      <button
                        key={file.path}
                        type="button"
                        onClick={() => setSelectedFileIndex(idx)}
                        className={`w-full text-left p-3.5 rounded-xl border text-xs font-bold transition-all cursor-pointer ${
                          selectedFileIndex === idx
                            ? 'glass-solid-blue'
                            : 'bg-white/85 hover:bg-sky-50 border-sky-200 text-slate-800'
                        }`}
                      >
                        <div className="font-mono font-extrabold text-sm truncate">{file.path}</div>
                        <div className={`mt-0.5 truncate ${selectedFileIndex === idx ? 'text-sky-100' : 'text-slate-500'}`}>
                          {file.label}
                        </div>
                      </button>
                    ))}
                  </div>

                  <div className="lg:col-span-8">
                    <div className="rounded-2xl border border-sky-200 bg-slate-950 text-slate-100 overflow-hidden">
                      <div className="flex items-center justify-between px-4 py-3 bg-slate-900 border-b border-slate-800">
                        <span className="font-mono text-xs font-bold text-sky-300">
                          django_atm_project/{sourceFiles[selectedFileIndex]?.path}
                        </span>
                        <button
                          type="button"
                          onClick={() =>
                            handleCopyCode(
                              sourceFiles[selectedFileIndex].path,
                              sourceFiles[selectedFileIndex].content
                            )
                          }
                          className="px-3 py-1 rounded-lg bg-sky-500/20 hover:bg-sky-500/30 text-sky-200 text-xs font-bold cursor-pointer"
                        >
                          {copiedPath === sourceFiles[selectedFileIndex]?.path ? 'Copied!' : 'Copy File Code'}
                        </button>
                      </div>
                      <pre className="p-4 text-xs font-mono leading-relaxed overflow-x-auto max-h-[560px]">
                        <code>{sourceFiles[selectedFileIndex]?.content}</code>
                      </pre>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
