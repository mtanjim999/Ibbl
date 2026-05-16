const ADMIN_PIN = '0000';
const STORAGE_KEY = 'ibbl_web_accounts';
let currentAccount = null;

const screens = {
  home: document.getElementById('home-screen'),
  login: document.getElementById('login-screen'),
  adminAuth: document.getElementById('adminAuth-screen'),
  admin: document.getElementById('admin-screen'),
  dashboard: document.getElementById('dashboard-screen'),
  history: document.getElementById('history-screen'),
  loginHistory: document.getElementById('login-history-screen'),
};

const inputAccount = document.getElementById('login-account');
const inputPin = document.getElementById('login-pin');
const dashboardBalance = document.getElementById('dashboard-balance');
const dashboardAccount = document.getElementById('dashboard-account');
const messageArea = document.getElementById('message-area');
const adminAuthPin = document.getElementById('admin-pin');
const adminAccountInput = document.getElementById('admin-account');
const adminPinInput = document.getElementById('admin-account-pin');
const adminBalanceInput = document.getElementById('admin-account-balance');
const historyBody = document.getElementById('history-body');
const loginHistoryBody = document.getElementById('login-history-body');

function getStoredAccounts() {
  const data = localStorage.getItem(STORAGE_KEY);
  if (!data) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([]));
    return [];
  }
  try {
    return JSON.parse(data);
  } catch (err) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify([]));
    return [];
  }
}

function saveAccounts(accounts) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(accounts));
}

function showScreen(screenId) {
  Object.values(screens).forEach(screen => screen.classList.add('hidden'));
  screens[screenId].classList.remove('hidden');
  clearMessage();
}

function showMessage(text, type = 'success') {
  messageArea.innerHTML = `<div class="message ${type === 'warning' ? 'warning' : ''}">${text}</div>`;
}

function clearMessage() {
  messageArea.innerHTML = '';
}

function formatCurrency(amount) {
  return `BDT ${amount.toFixed(2)}`;
}

function findAccount(accountNumber) {
  const accounts = getStoredAccounts();
  return accounts.find(acc => acc.acc_no === accountNumber);
}

function updateCurrentAccountInfo() {
  if (!currentAccount) return;
  dashboardAccount.textContent = currentAccount.acc_no;
  dashboardBalance.textContent = formatCurrency(currentAccount.balance);
}

function recordLoginEvent(accountNumber, status) {
  const accounts = getStoredAccounts();
  const account = accounts.find(acc => acc.acc_no === accountNumber);
  if (!account) {
    return;
  }
  const entry = { status, time: new Date().toLocaleString() };
  account.loginHistory = account.loginHistory || [];
  account.loginHistory.unshift(entry);
  saveAccounts(accounts);
}

function loginUser() {
  const acc = inputAccount.value.trim();
  const pin = inputPin.value.trim();
  if (!acc || !pin) {
    showMessage('Please enter both account number and PIN.', 'warning');
    return;
  }
  const account = findAccount(acc);
  if (!account || account.pin !== pin) {
    recordLoginEvent(acc, 'Failed');
    showMessage('Invalid account number or PIN.', 'warning');
    return;
  }
  recordLoginEvent(acc, 'Success');
  currentAccount = account;
  updateCurrentAccountInfo();
  showScreen('dashboard');
}

function logoutUser() {
  currentAccount = null;
  inputAccount.value = '';
  inputPin.value = '';
  showScreen('home');
}

function authenticateAdmin() {
  const pin = adminAuthPin.value.trim();
  if (pin === ADMIN_PIN) {
    adminAuthPin.value = '';
    showScreen('admin');
    return;
  }
  showMessage('Incorrect admin PIN.', 'warning');
}

function createNewAccount() {
  const acc_no = adminAccountInput.value.trim();
  const pin = adminPinInput.value.trim();
  const balance = parseFloat(adminBalanceInput.value);

  if (!acc_no || !pin || Number.isNaN(balance)) {
    showMessage('Fill all fields correctly.', 'warning');
    return;
  }
  if (pin.length !== 4 || !/^[0-9]{4}$/.test(pin)) {
    showMessage('PIN must be exactly 4 digits.', 'warning');
    return;
  }
  const accounts = getStoredAccounts();
  if (accounts.some(acc => acc.acc_no === acc_no)) {
    showMessage('This account already exists.', 'warning');
    return;
  }
  accounts.push({ acc_no, pin, balance, history: [], loginHistory: [] });
  saveAccounts(accounts);
  adminAccountInput.value = '';
  adminPinInput.value = '';
  adminBalanceInput.value = '';
  showMessage(`Account ${acc_no} was created successfully.`);
}

function performTransaction(type) {
  if (!currentAccount) return;
  const amount = parseFloat(prompt(`Enter amount to ${type} (BDT):`, '0'));
  if (Number.isNaN(amount) || amount <= 0) {
    showMessage('Please enter a valid amount.', 'warning');
    return;
  }
  if (type === 'Withdraw' && amount > currentAccount.balance) {
    showMessage('Insufficient balance for this withdrawal.', 'warning');
    return;
  }
  currentAccount.balance += type === 'Withdraw' ? -amount : amount;
  currentAccount.history = currentAccount.history || [];
  currentAccount.history.unshift({ type, amount, time: new Date().toLocaleTimeString() });
  const accounts = getStoredAccounts();
  const index = accounts.findIndex(acc => acc.acc_no === currentAccount.acc_no);
  accounts[index] = currentAccount;
  saveAccounts(accounts);
  updateCurrentAccountInfo();
  showMessage(`${type} completed successfully.`);
}

function showTransactionHistory() {
  if (!currentAccount) return;
  const history = [...(currentAccount.history || [])].sort((a, b) => b.amount - a.amount);
  historyBody.innerHTML = history.length
    ? history.map(entry => `<tr><td>${entry.type}</td><td>${entry.time}</td><td>${formatCurrency(entry.amount)}</td></tr>`).join('')
    : '<tr><td colspan="3" style="text-align:center; padding:16px; color:#64748b;">No transactions yet.</td></tr>';
  showScreen('history');
}

function showLoginHistory() {
  if (!currentAccount) return;
  const logins = currentAccount.loginHistory || [];
  loginHistoryBody.innerHTML = logins.length
    ? logins.map(entry => `<tr><td class="status-${entry.status.toLowerCase()}">${entry.status}</td><td>${entry.time}</td></tr>`).join('')
    : '<tr><td colspan="2" style="text-align:center; padding:16px; color:#64748b;">No login history yet.</td></tr>';
  showScreen('loginHistory');
}

function initApp() {
  showScreen('home');
  const accounts = getStoredAccounts();
  if (accounts.length === 0) {
    accounts.push({
      acc_no: '1001',
      pin: '1234',
      balance: 15000,
      history: [],
      loginHistory: [],
    });
    saveAccounts(accounts);
  }
}

window.addEventListener('DOMContentLoaded', () => {
  document.getElementById('home-login').addEventListener('click', () => showScreen('login'));
  document.getElementById('open-admin-auth').addEventListener('click', () => showScreen('adminAuth'));
  document.getElementById('login-submit').addEventListener('click', loginUser);
  document.getElementById('login-back').addEventListener('click', () => showScreen('home'));
  document.getElementById('dashboard-logout').addEventListener('click', logoutUser);
  document.getElementById('dashboard-withdraw').addEventListener('click', () => performTransaction('Withdraw'));
  document.getElementById('dashboard-deposit').addEventListener('click', () => performTransaction('Deposit'));
  document.getElementById('dashboard-history').addEventListener('click', showTransactionHistory);
  document.getElementById('dashboard-login-history').addEventListener('click', showLoginHistory);
  document.getElementById('history-back').addEventListener('click', () => showScreen('dashboard'));
  document.getElementById('login-history-back').addEventListener('click', () => showScreen('dashboard'));
  document.getElementById('open-admin-auth').addEventListener('click', () => showScreen('adminAuth'));
  document.getElementById('admin-auth-submit').addEventListener('click', authenticateAdmin);
  document.getElementById('admin-auth-back').addEventListener('click', () => showScreen('home'));
  document.getElementById('admin-create').addEventListener('click', createNewAccount);
  document.getElementById('admin-back').addEventListener('click', () => showScreen('home'));

  initApp();
});
