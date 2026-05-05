"""
╔══════════════════════════════════════════════════════════════════════╗
║          🏦  PYTHON NATIONAL BANK — PRO EDITION  🏦                  ║
║                                                                      ║
║  INNOVATIVE FEATURES:                                                ║
║  ✦ OTP Verification (Simulated)      ✦ Loan Management              ║
║  ✦ Fixed Deposit (FD) System         ✦ Spending Analytics           ║
║  ✦ Bill Payments (Electricity/Water) ✦ Savings Goals Tracker        ║
║  ✦ Account Freeze / Unfreeze         ✦ Reward Points System         ║
║  ✦ Daily Transaction Limits          ✦ Multi-Currency View          ║
║  ✦ Scheduled / Recurring Payments    ✦ Net Worth Dashboard          ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os, json, hashlib, random, string, time
from datetime import datetime, timedelta

# ─────────────────────────────────────────
#  DATA FILE
# ─────────────────────────────────────────
DATA_FILE = "bank_pro_data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "accounts": {},
        "admin": {"pin": hash_pin("admin123")},
        "exchange_rates": {"USD": 0.012, "EUR": 0.011, "GBP": 0.0094, "JPY": 1.78}
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

# ─────────────────────────────────────────
#  DISPLAY HELPERS
# ─────────────────────────────────────────
C = {
    "cyan":    "\033[96m", "green":  "\033[92m", "red":    "\033[91m",
    "yellow":  "\033[93m", "blue":   "\033[94m", "gray":   "\033[90m",
    "magenta": "\033[95m", "white":  "\033[97m", "reset":  "\033[0m",
    "bold":    "\033[1m",  "dim":    "\033[2m"
}

def clr(text, color): return f"{C[color]}{text}{C['reset']}"
def clear():           os.system("cls" if os.name == "nt" else "clear")
def pause():           input(f"\n  {clr('Press Enter to continue...', 'dim')}")
def divider(char="─"): print(clr(char * 60, "gray"))
def success(m):        print(clr(f"  ✔  {m}", "green"))
def error(m):          print(clr(f"  ✘  {m}", "red"))
def info(m):           print(clr(f"  ℹ  {m}", "yellow"))
def warn(m):           print(clr(f"  ⚠  {m}", "magenta"))

def banner():
    print(clr("""
╔══════════════════════════════════════════════════════════════╗
║        🏦   PYTHON NATIONAL BANK  —  PRO EDITION  🏦        ║
║              Secure  •  Smart  •  Innovative                 ║
╚══════════════════════════════════════════════════════════════╝""", "cyan"))

def heading(title, icon="◆"):
    print(f"\n  {clr(icon, 'cyan')} {clr(title, 'bold')}")

def txn_id():
    return "TXN" + "".join(random.choices(string.digits, k=10))

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def gen_acc():
    return "PNB" + "".join(random.choices(string.digits, k=9))

def add_txn(account, t_type, amount, note="", category="General"):
    account["transactions"].append({
        "id": txn_id(), "type": t_type, "amount": amount,
        "balance": account["balance"], "timestamp": now(),
        "note": note, "category": category
    })
    # Reward Points: 1 point per ₹100 spent
    if t_type == "DEBIT":
        pts = int(amount // 100)
        account["reward_points"] = account.get("reward_points", 0) + pts

# ─────────────────────────────────────────
#  OTP SYSTEM (Simulated)
# ─────────────────────────────────────────
def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp(phone, purpose="Login"):
    otp = generate_otp()
    print(clr(f"\n  📱 OTP sent to +91-XXXXXX{phone[-4:]} for {purpose}", "yellow"))
    print(clr(f"  [DEMO MODE — Your OTP is: {otp}]", "magenta"))
    return otp

def verify_otp(real_otp):
    for attempt in range(3):
        entered = input(f"  Enter OTP ({3 - attempt} attempts left): ").strip()
        if entered == real_otp:
            success("OTP Verified!")
            return True
        else:
            error("Wrong OTP.")
    return False

# ─────────────────────────────────────────
#  1. CREATE ACCOUNT
# ─────────────────────────────────────────
def create_account(data):
    clear(); banner()
    heading("CREATE NEW ACCOUNT", "📝")
    divider()

    name = input("  Full Name           : ").strip()
    if not name: error("Name cannot be empty."); pause(); return

    phone = input("  Phone Number        : ").strip()
    if not phone.isdigit() or len(phone) < 10:
        error("Invalid phone number."); pause(); return

    email = input("  Email Address       : ").strip()
    dob   = input("  Date of Birth (DD-MM-YYYY): ").strip()

    acc_type = input("  Account Type [1-Savings / 2-Current]: ").strip()
    acc_type = "Savings" if acc_type == "1" else "Current"

    while True:
        pin = input("  Set 4-digit PIN     : ").strip()
        if pin.isdigit() and len(pin) == 4:
            if input("  Confirm PIN         : ").strip() == pin: break
            else: error("PINs don't match.")
        else: error("PIN must be 4 digits.")

    # OTP Verification
    otp = send_otp(phone, "Account Creation")
    if not verify_otp(otp):
        error("OTP verification failed. Account not created."); pause(); return

    while True:
        try:
            deposit = float(input("  Opening Deposit (min ₹500): ₹ "))
            if deposit < 500: error("Minimum ₹500 required.")
            else: break
        except: error("Invalid amount.")

    acc_no = gen_acc()
    while acc_no in data["accounts"]: acc_no = gen_acc()

    data["accounts"][acc_no] = {
        "account_number": acc_no, "name": name, "phone": phone,
        "email": email, "dob": dob, "account_type": acc_type,
        "pin": hash_pin(pin), "balance": deposit,
        "created_at": now(), "transactions": [],
        "reward_points": 0, "is_frozen": False,
        "daily_limit": 50000, "daily_spent": 0,
        "last_txn_date": datetime.now().strftime("%Y-%m-%d"),
        "fixed_deposits": [], "loans": [],
        "savings_goals": [], "scheduled_payments": [],
        "bills": []
    }
    add_txn(data["accounts"][acc_no], "CREDIT", deposit, "Opening Deposit", "Opening")
    save_data(data)

    divider()
    success("Account Created Successfully!")
    print(clr(f"""
  Account Number  : {acc_no}
  Account Holder  : {name}
  Account Type    : {acc_type}
  Opening Balance : ₹{deposit:,.2f}
  Reward Points   : 0 pts""", "green"))
    info("Save your account number for login.")
    pause()

# ─────────────────────────────────────────
#  2. LOGIN
# ─────────────────────────────────────────
def login(data):
    clear(); banner()
    heading("CUSTOMER LOGIN", "🔐")
    divider()

    acc_no = input("  Account Number : ").strip().upper()
    if acc_no not in data["accounts"]:
        error("Account not found."); pause(); return None

    acc = data["accounts"][acc_no]
    if acc.get("is_frozen"):
        warn("This account is FROZEN. Contact admin."); pause(); return None

    pin = input("  PIN            : ").strip()
    if acc["pin"] != hash_pin(pin):
        error("Incorrect PIN."); pause(); return None

    # OTP on Login
    otp = send_otp(acc["phone"], "Login")
    if not verify_otp(otp):
        error("OTP failed. Access denied."); pause(); return None

    # Reset daily spending if new day
    today = datetime.now().strftime("%Y-%m-%d")
    if acc.get("last_txn_date") != today:
        acc["daily_spent"] = 0
        acc["last_txn_date"] = today
        save_data(data)

    success(f"Welcome back, {acc['name']}! 👋")
    pause()
    return acc_no

# ─────────────────────────────────────────
#  3. BALANCE + NET WORTH DASHBOARD
# ─────────────────────────────────────────
def net_worth_dashboard(data, acc_no):
    acc = data["accounts"][acc_no]
    clear(); banner()
    heading("NET WORTH DASHBOARD", "📊")
    divider()

    balance  = acc["balance"]
    fd_total = sum(fd["amount"] for fd in acc.get("fixed_deposits", []))
    loan_due = sum(l["remaining"] for l in acc.get("loans", []))
    goal_saved = sum(g["saved"] for g in acc.get("savings_goals", []))
    net_worth  = balance + fd_total + goal_saved - loan_due

    rates = data.get("exchange_rates", {})
    print(f"\n  {'Account Balance':<25}: {clr(f'₹{balance:>12,.2f}', 'green')}")
    print(f"  {'Fixed Deposits':<25}: {clr(f'₹{fd_total:>12,.2f}', 'cyan')}")
    print(f"  {'Savings Goals':<25}: {clr(f'₹{goal_saved:>12,.2f}', 'yellow')}")
    print(f"  {'Loan Outstanding':<25}: {clr(f'₹{loan_due:>12,.2f}', 'red')}")
    divider()
    print(f"  {'NET WORTH':<25}: {clr(f'₹{net_worth:>12,.2f}', 'magenta')}")
    divider()

    print(clr("\n  💱 Multi-Currency View:", "cyan"))
    for cur, rate in rates.items():
        print(f"    {cur}  :  {balance * rate:>10,.2f}")

    print(f"\n  🎯 Reward Points : {clr(str(acc.get('reward_points',0)) + ' pts', 'yellow')}")
    print(f"  📅 Daily Spent   : ₹{acc.get('daily_spent',0):,.2f} / ₹{acc.get('daily_limit',50000):,.2f}")
    pause()

# ─────────────────────────────────────────
#  4. CREDIT / DEBIT (with daily limit)
# ─────────────────────────────────────────
def credit_amount(data, acc_no):
    acc = data["accounts"][acc_no]
    clear(); banner(); heading("DEPOSIT MONEY", "💰"); divider()
    print(f"  Account : {acc_no} | {acc['name']}  |  Balance: ₹{acc['balance']:,.2f}")
    divider()

    categories = ["Salary", "Business", "Gift", "Refund", "Other"]
    print("  Category: " + "  ".join(f"[{i+1}]{c}" for i,c in enumerate(categories)))
    try:
        cat_i = int(input("  Choose: ").strip()) - 1
        category = categories[cat_i] if 0 <= cat_i < len(categories) else "Other"
    except: category = "Other"

    try:
        amount = float(input("  Deposit Amount : ₹ "))
        if amount <= 0: error("Must be > 0."); pause(); return
        if amount > 1_000_000: error("Limit ₹10,00,000."); pause(); return
    except: error("Invalid amount."); pause(); return

    note = input("  Remark         : ").strip() or "Cash Deposit"
    acc["balance"] += amount
    add_txn(acc, "CREDIT", amount, note, category)
    save_data(data)

    divider()
    success(f"₹{amount:,.2f} Deposited!")
    print(f"  Updated Balance : ₹{acc['balance']:,.2f}")
    print(f"  Transaction ID  : {txn_id()}")
    pause()

def debit_amount(data, acc_no):
    acc = data["accounts"][acc_no]
    clear(); banner(); heading("WITHDRAW MONEY", "💸"); divider()
    print(f"  Account : {acc_no} | {acc['name']}  |  Balance: ₹{acc['balance']:,.2f}")
    print(f"  Daily Remaining : ₹{acc.get('daily_limit',50000) - acc.get('daily_spent',0):,.2f}")
    divider()

    categories = ["Shopping", "Food", "Travel", "Medical", "Education", "Utilities", "Other"]
    print("  Category: " + "  ".join(f"[{i+1}]{c}" for i,c in enumerate(categories)))
    try:
        cat_i = int(input("  Choose: ").strip()) - 1
        category = categories[cat_i] if 0 <= cat_i < len(categories) else "Other"
    except: category = "Other"

    try:
        amount = float(input("  Withdraw Amount : ₹ "))
        if amount <= 0: error("Must be > 0."); pause(); return
        if amount > acc["balance"]: error("Insufficient balance."); pause(); return
        remaining_daily = acc.get("daily_limit", 50000) - acc.get("daily_spent", 0)
        if amount > remaining_daily:
            error(f"Daily limit exceeded! Remaining: ₹{remaining_daily:,.2f}"); pause(); return
    except: error("Invalid amount."); pause(); return

    note = input("  Remark          : ").strip() or "Cash Withdrawal"
    acc["balance"]   -= amount
    acc["daily_spent"] = acc.get("daily_spent", 0) + amount
    add_txn(acc, "DEBIT", amount, note, category)
    save_data(data)

    pts = int(amount // 100)
    divider()
    success(f"₹{amount:,.2f} Withdrawn!")
    print(f"  Updated Balance  : ₹{acc['balance']:,.2f}")
    if pts: print(f"  🎁 Earned        : +{pts} Reward Points!")
    pause()

# ─────────────────────────────────────────
#  5. FUND TRANSFER
# ─────────────────────────────────────────
def fund_transfer(data, acc_no):
    acc = data["accounts"][acc_no]
    clear(); banner(); heading("FUND TRANSFER", "🔄"); divider()
    print(f"  Your Balance : ₹{acc['balance']:,.2f}")
    divider()

    to_acc = input("  Recipient Account No : ").strip().upper()
    if to_acc == acc_no: error("Cannot transfer to self."); pause(); return
    if to_acc not in data["accounts"]: error("Account not found."); pause(); return

    to = data["accounts"][to_acc]
    print(f"  Recipient Name : {clr(to['name'], 'cyan')}")

    try:
        amount = float(input("  Amount : ₹ "))
        if amount <= 0 or amount > acc["balance"]: error("Invalid amount."); pause(); return
        if amount > 200_000: error("Transfer limit ₹2,00,000."); pause(); return
        remaining = acc.get("daily_limit", 50000) - acc.get("daily_spent", 0)
        if amount > remaining: error(f"Daily limit! Remaining: ₹{remaining:,.2f}"); pause(); return
    except: error("Invalid amount."); pause(); return

    note = input("  Remark : ").strip() or "Online Transfer"

    # OTP for large transfers
    if amount > 10000:
        otp = send_otp(acc["phone"], "Fund Transfer")
        if not verify_otp(otp): error("Transfer cancelled."); pause(); return

    ref = txn_id()
    acc["balance"] -= amount; acc["daily_spent"] = acc.get("daily_spent",0) + amount
    to["balance"]  += amount

    add_txn(acc, "DEBIT",  amount, f"To {to_acc} | {note} | {ref}", "Transfer")
    add_txn(to,  "CREDIT", amount, f"From {acc_no} | {note} | {ref}", "Transfer")
    save_data(data)

    divider()
    success("Transfer Successful!")
    print(f"  Sent To   : {to['name']} ({to_acc})")
    print(f"  Amount    : ₹{amount:,.2f}")
    print(f"  Balance   : ₹{acc['balance']:,.2f}")
    print(f"  Ref ID    : {ref}")
    pause()

# ─────────────────────────────────────────
#  6. FIXED DEPOSIT
# ─────────────────────────────────────────
def fixed_deposit_menu(data, acc_no):
    acc = data["accounts"][acc_no]
    while True:
        clear(); banner(); heading("FIXED DEPOSIT", "🏛"); divider()
        print("  [1] Create FD")
        print("  [2] View My FDs")
        print("  [3] Mature / Break FD")
        print("  [0] Back")
        divider()
        ch = input("  Option : ").strip()

        if ch == "1":
            print(f"\n  Balance : ₹{acc['balance']:,.2f}")
            tenures = {"1": (6,  6.5), "2": (12, 7.0), "3": (24, 7.5), "4": (36, 8.0)}
            print("  Tenures:")
            print("    [1] 6 months  @ 6.5%  [2] 12 months @ 7.0%")
            print("    [3] 24 months @ 7.5%  [4] 36 months @ 8.0%")
            t = input("  Select Tenure : ").strip()
            if t not in tenures: error("Invalid."); pause(); continue
            months, rate = tenures[t]

            try:
                amount = float(input("  FD Amount (min ₹1000): ₹ "))
                if amount < 1000: error("Min ₹1000."); pause(); continue
                if amount > acc["balance"]: error("Insufficient balance."); pause(); continue
            except: error("Invalid."); pause(); continue

            maturity = amount * (1 + rate/100 * months/12)
            start    = datetime.now()
            end      = start + timedelta(days=months*30)

            acc["balance"] -= amount
            fd_id = "FD" + "".join(random.choices(string.digits, k=6))
            acc["fixed_deposits"].append({
                "id": fd_id, "amount": amount, "rate": rate,
                "months": months, "maturity_amount": round(maturity, 2),
                "start_date": start.strftime("%Y-%m-%d"),
                "end_date": end.strftime("%Y-%m-%d"), "status": "Active"
            })
            add_txn(acc, "DEBIT", amount, f"FD Created {fd_id}", "FD")
            save_data(data)
            success(f"FD Created! Maturity Amount: ₹{maturity:,.2f} on {end.strftime('%Y-%m-%d')}")
            pause()

        elif ch == "2":
            clear(); banner(); heading("MY FIXED DEPOSITS", "🏛"); divider()
            fds = acc.get("fixed_deposits", [])
            if not fds: info("No FDs found.")
            for fd in fds:
                status_color = "green" if fd["status"] == "Active" else "gray"
                print(f"  {clr(fd['id'], 'cyan')}  |  ₹{fd['amount']:,.2f}  |  {fd['rate']}%  |  "
                      f"{fd['months']}M  |  Maturity: ₹{fd['maturity_amount']:,.2f}")
                print(f"    Start: {fd['start_date']}  →  End: {fd['end_date']}  "
                      f"| {clr(fd['status'], status_color)}")
                print()
            pause()

        elif ch == "3":
            fd_id = input("  Enter FD ID to break: ").strip().upper()
            fds = [f for f in acc.get("fixed_deposits", []) if f["id"] == fd_id and f["status"] == "Active"]
            if not fds: error("FD not found."); pause(); continue
            fd = fds[0]
            warn(f"Breaking FD early! You'll get ₹{fd['amount']:,.2f} (no interest).")
            if input("  Confirm? (yes/no): ").strip().lower() == "yes":
                acc["balance"] += fd["amount"]
                fd["status"] = "Closed"
                add_txn(acc, "CREDIT", fd["amount"], f"FD Broken {fd_id}", "FD")
                save_data(data)
                success(f"₹{fd['amount']:,.2f} returned to account.")
            pause()

        elif ch == "0": break

# ─────────────────────────────────────────
#  7. LOAN MANAGEMENT
# ─────────────────────────────────────────
def loan_menu(data, acc_no):
    acc = data["accounts"][acc_no]
    while True:
        clear(); banner(); heading("LOAN MANAGEMENT", "🏠"); divider()
        print("  [1] Apply for Loan")
        print("  [2] View My Loans")
        print("  [3] Pay EMI")
        print("  [0] Back")
        divider()
        ch = input("  Option : ").strip()

        if ch == "1":
            loan_types = {"1": ("Personal Loan", 12.0), "2": ("Home Loan", 8.5),
                          "3": ("Education Loan", 9.0), "4": ("Vehicle Loan", 10.5)}
            print("\n  Loan Types:")
            for k,(n,r) in loan_types.items(): print(f"    [{k}] {n} @ {r}% p.a.")
            lt = input("  Select Type : ").strip()
            if lt not in loan_types: error("Invalid."); pause(); continue
            loan_name, rate = loan_types[lt]

            try:
                principal = float(input("  Loan Amount    : ₹ "))
                if principal < 10000: error("Min ₹10,000."); pause(); continue
                tenure    = int(input("  Tenure (months): "))
                if tenure < 6: error("Min 6 months."); pause(); continue
            except: error("Invalid."); pause(); continue

            monthly_rate = rate / 100 / 12
            emi = principal * monthly_rate * (1+monthly_rate)**tenure / ((1+monthly_rate)**tenure - 1)
            total = emi * tenure

            print(f"\n  {clr('Loan Summary', 'cyan')}")
            print(f"  Principal  : ₹{principal:,.2f}")
            print(f"  EMI        : ₹{emi:,.2f}/month")
            print(f"  Total Pay  : ₹{total:,.2f}  (Interest: ₹{total-principal:,.2f})")

            if input("\n  Approve & Disburse? (yes/no): ").strip().lower() == "yes":
                loan_id = "LN" + "".join(random.choices(string.digits, k=6))
                acc["balance"] += principal
                acc["loans"].append({
                    "id": loan_id, "type": loan_name, "principal": principal,
                    "rate": rate, "tenure": tenure, "emi": round(emi, 2),
                    "remaining": round(total, 2), "status": "Active",
                    "disbursed_on": now()
                })
                add_txn(acc, "CREDIT", principal, f"Loan Disbursed {loan_id}", "Loan")
                save_data(data)
                success(f"Loan approved! ₹{principal:,.2f} added. EMI: ₹{emi:,.2f}/month")
            pause()

        elif ch == "2":
            clear(); banner(); heading("MY LOANS", "🏠"); divider()
            loans = acc.get("loans", [])
            if not loans: info("No loans found.")
            for l in loans:
                print(f"  {clr(l['id'],'cyan')} | {l['type']} | ₹{l['principal']:,.2f} @ {l['rate']}%")
                print(f"    EMI: ₹{l['emi']:,.2f}/month | Remaining: ₹{l['remaining']:,.2f} | {clr(l['status'],'green')}")
                print()
            pause()

        elif ch == "3":
            loans = [l for l in acc.get("loans",[]) if l["status"]=="Active"]
            if not loans: info("No active loans."); pause(); continue
            for l in loans: print(f"  [{l['id']}] {l['type']} | EMI: ₹{l['emi']:,.2f}")
            lid = input("  Loan ID to pay EMI: ").strip().upper()
            loan = next((l for l in loans if l["id"]==lid), None)
            if not loan: error("Loan not found."); pause(); continue
            emi = loan["emi"]
            if acc["balance"] < emi: error("Insufficient balance."); pause(); continue
            acc["balance"]  -= emi
            loan["remaining"] = round(max(0, loan["remaining"] - emi), 2)
            if loan["remaining"] <= 0: loan["status"] = "Closed"; success("Loan fully paid off! 🎉")
            add_txn(acc, "DEBIT", emi, f"EMI for {lid}", "Loan EMI")
            save_data(data)
            success(f"EMI ₹{emi:,.2f} paid. Remaining: ₹{loan['remaining']:,.2f}")
            pause()

        elif ch == "0": break

# ─────────────────────────────────────────
#  8. BILL PAYMENTS
# ─────────────────────────────────────────
def bill_payment(data, acc_no):
    acc = data["accounts"][acc_no]
    clear(); banner(); heading("BILL PAYMENTS", "⚡"); divider()
    print(f"  Balance : ₹{acc['balance']:,.2f}\n")

    bills = {
        "1": ("Electricity Board", 1450.00),
        "2": ("Water Supply Dept", 340.00),
        "3": ("Broadband Internet", 799.00),
        "4": ("Gas Connection", 620.00),
        "5": ("Mobile Postpaid",  899.00),
        "6": ("DTH Recharge",     299.00),
        "7": ("LIC Premium",     3200.00),
        "8": ("Credit Card Bill",2500.00),
    }
    for k, (n, a) in bills.items():
        print(f"  [{k}] {n:<25} ₹{a:,.2f}")
    divider()
    ch = input("  Select Bill : ").strip()
    if ch not in bills: error("Invalid option."); pause(); return

    bill_name, amount = bills[ch]
    consumer = input(f"  Consumer/Account No for {bill_name}: ").strip()

    print(f"\n  {clr('Payment Summary', 'cyan')}")
    print(f"  Bill     : {bill_name}")
    print(f"  Consumer : {consumer}")
    print(f"  Amount   : ₹{amount:,.2f}")

    if input("\n  Confirm Payment? (yes/no): ").strip().lower() != "yes":
        info("Cancelled."); pause(); return
    if acc["balance"] < amount:
        error("Insufficient balance."); pause(); return

    acc["balance"] -= amount
    ref = txn_id()
    add_txn(acc, "DEBIT", amount, f"{bill_name} | Consumer:{consumer} | Ref:{ref}", "Bills")
    acc.setdefault("bills", []).append({
        "name": bill_name, "amount": amount,
        "consumer": consumer, "ref": ref, "paid_on": now()
    })
    save_data(data)

    divider()
    success(f"₹{amount:,.2f} paid for {bill_name}!")
    print(f"  Ref ID  : {ref}")
    print(f"  Balance : ₹{acc['balance']:,.2f}")
    pause()

# ─────────────────────────────────────────
#  9. SAVINGS GOALS
# ─────────────────────────────────────────
def savings_goals(data, acc_no):
    acc = data["accounts"][acc_no]
    while True:
        clear(); banner(); heading("SAVINGS GOALS TRACKER", "🎯"); divider()
        print("  [1] Create New Goal")
        print("  [2] Add to Goal")
        print("  [3] View All Goals")
        print("  [0] Back")
        divider()
        ch = input("  Option : ").strip()

        if ch == "1":
            gname  = input("  Goal Name (e.g., iPhone, Trip, Car): ").strip()
            try:
                target = float(input("  Target Amount : ₹ "))
                months = int(input("  Target Months : "))
            except: error("Invalid."); pause(); continue
            monthly_need = target / months
            gid = "GOAL" + "".join(random.choices(string.digits, k=4))
            acc.setdefault("savings_goals", []).append({
                "id": gid, "name": gname, "target": target,
                "saved": 0, "months": months,
                "monthly_need": round(monthly_need, 2),
                "created_on": now(), "status": "Active"
            })
            save_data(data)
            success(f"Goal '{gname}' created! Save ₹{monthly_need:,.2f}/month to reach ₹{target:,.2f}.")
            pause()

        elif ch == "2":
            goals = [g for g in acc.get("savings_goals",[]) if g["status"]=="Active"]
            if not goals: info("No active goals."); pause(); continue
            for g in goals:
                pct = min(100, g["saved"]/g["target"]*100)
                bar = "█" * int(pct//5) + "░" * (20 - int(pct//5))
                print(f"  [{g['id']}] {g['name']} | ₹{g['saved']:,.0f}/₹{g['target']:,.0f} [{bar}] {pct:.0f}%")
            gid = input("  Goal ID : ").strip().upper()
            goal = next((g for g in goals if g["id"]==gid), None)
            if not goal: error("Not found."); pause(); continue
            try: amt = float(input(f"  Add Amount (suggested ₹{goal['monthly_need']:,.2f}): ₹ "))
            except: error("Invalid."); pause(); continue
            if amt > acc["balance"]: error("Insufficient balance."); pause(); continue
            acc["balance"] -= amt
            goal["saved"]  += amt
            if goal["saved"] >= goal["target"]:
                goal["status"] = "Achieved"
                success(f"🎉 GOAL '{goal['name']}' ACHIEVED! Congratulations!")
            add_txn(acc, "DEBIT", amt, f"Savings Goal: {goal['name']}", "Savings")
            save_data(data)
            success(f"₹{amt:,.2f} added to '{goal['name']}'!")
            pause()

        elif ch == "3":
            clear(); banner(); heading("ALL SAVINGS GOALS", "🎯"); divider()
            goals = acc.get("savings_goals", [])
            if not goals: info("No goals found."); pause(); continue
            for g in goals:
                pct = min(100, g["saved"]/g["target"]*100)
                bar = "█" * int(pct//5) + "░" * (20 - int(pct//5))
                color = "green" if g["status"]=="Achieved" else "yellow"
                print(f"  {clr(g['id'],'cyan')} {g['name']}")
                print(f"  [{bar}] {pct:.0f}%  ₹{g['saved']:,.0f} / ₹{g['target']:,.0f}  {clr(g['status'],color)}")
                print(f"  Monthly Need: ₹{g['monthly_need']:,.2f}  |  Created: {g['created_on'][:10]}")
                print()
            pause()

        elif ch == "0": break

# ─────────────────────────────────────────
#  10. SPENDING ANALYTICS
# ─────────────────────────────────────────
def spending_analytics(data, acc_no):
    acc = data["accounts"][acc_no]
    clear(); banner(); heading("SPENDING ANALYTICS", "📈"); divider()

    txns = [t for t in acc["transactions"] if t["type"] == "DEBIT"]
    if not txns: info("No spending data yet."); pause(); return

    cat_totals = {}
    monthly    = {}
    for t in txns:
        cat = t.get("category", "Other")
        cat_totals[cat] = cat_totals.get(cat, 0) + t["amount"]
        month = t["timestamp"][:7]
        monthly[month] = monthly.get(month, 0) + t["amount"]

    total_spent = sum(cat_totals.values())
    print(f"\n  Total Spent : {clr(f'₹{total_spent:,.2f}', 'red')}\n")

    print(clr("  📊 Spending by Category:", "cyan"))
    divider()
    for cat, amt in sorted(cat_totals.items(), key=lambda x: -x[1]):
        pct = amt / total_spent * 100
        bar = "█" * int(pct // 3)
        print(f"  {cat:<15} {bar:<25} ₹{amt:>10,.2f}  ({pct:.1f}%)")

    print(clr("\n  📅 Monthly Spending:", "cyan"))
    divider()
    for month, amt in sorted(monthly.items()):
        bar = "█" * int(amt // 500)
        print(f"  {month}  {bar}  ₹{amt:,.2f}")

    total_credit = sum(t["amount"] for t in acc["transactions"] if t["type"]=="CREDIT")
    print(f"\n  Total Income : {clr(f'₹{total_credit:,.2f}', 'green')}")
    print(f"  Total Spent  : {clr(f'₹{total_spent:,.2f}', 'red')}")
    print(f"  Net Saved    : {clr(f'₹{total_credit-total_spent:,.2f}', 'yellow')}")
    pause()

# ─────────────────────────────────────────
#  11. REWARD POINTS
# ─────────────────────────────────────────
def reward_points(data, acc_no):
    acc = data["accounts"][acc_no]
    clear(); banner(); heading("REWARD POINTS", "🎁"); divider()
    pts = acc.get("reward_points", 0)
    value = pts * 0.25  # 1 pt = ₹0.25

    print(f"\n  Your Points   : {clr(str(pts) + ' pts', 'yellow')}")
    print(f"  Cash Value    : {clr(f'₹{value:,.2f}', 'green')}")
    print(f"\n  Tier Status   : ", end="")
    if pts >= 5000:   print(clr("💎 PLATINUM", "cyan"))
    elif pts >= 2000: print(clr("🥇 GOLD", "yellow"))
    elif pts >= 500:  print(clr("🥈 SILVER", "gray"))
    else:             print(clr("🥉 BRONZE", "red"))

    divider()
    print("  [1] Redeem Points as Cash Balance")
    print("  [0] Back")
    ch = input("  Option : ").strip()
    if ch == "1" and pts >= 100:
        try:
            redeem = int(input(f"  Redeem how many points (min 100, max {pts}): "))
            if redeem < 100 or redeem > pts: error("Invalid."); pause(); return
        except: error("Invalid."); pause(); return
        cash = redeem * 0.25
        acc["balance"] += cash
        acc["reward_points"] -= redeem
        add_txn(acc, "CREDIT", cash, f"Reward Points Redeemed ({redeem} pts)", "Rewards")
        save_data(data)
        success(f"₹{cash:.2f} added from {redeem} reward points!")
    elif ch == "1": info("Need at least 100 points to redeem.")
    pause()

# ─────────────────────────────────────────
#  12. ACCOUNT SETTINGS
# ─────────────────────────────────────────
def account_settings(data, acc_no):
    acc = data["accounts"][acc_no]
    while True:
        clear(); banner(); heading("ACCOUNT SETTINGS", "⚙"); divider()
        print("  [1] Change PIN")
        print("  [2] Update Daily Transaction Limit")
        print("  [3] View Account Profile")
        print("  [4] Freeze Account")
        print("  [0] Back")
        divider()
        ch = input("  Option : ").strip()

        if ch == "1":
            old = input("  Current PIN : ").strip()
            if acc["pin"] != hash_pin(old): error("Wrong PIN."); pause(); continue
            while True:
                new = input("  New PIN     : ").strip()
                if new.isdigit() and len(new)==4:
                    if input("  Confirm     : ").strip() == new: break
                    else: error("No match.")
                else: error("4 digits required.")
            acc["pin"] = hash_pin(new)
            save_data(data)
            success("PIN updated!"); pause()

        elif ch == "2":
            try:
                limit = float(input(f"  New Daily Limit (current ₹{acc.get('daily_limit',50000):,.0f}): ₹ "))
                if limit < 1000: error("Min ₹1000."); pause(); continue
                if limit > 200000: error("Max ₹2,00,000."); pause(); continue
                acc["daily_limit"] = limit
                save_data(data)
                success(f"Daily limit updated to ₹{limit:,.2f}"); pause()
            except: error("Invalid."); pause()

        elif ch == "3":
            clear(); banner(); heading("ACCOUNT PROFILE", "👤"); divider()
            fields = [("Account No","account_number"),("Name","name"),("Phone","phone"),
                      ("Email","email"),("DOB","dob"),("Type","account_type"),("Opened","created_at")]
            for label, key in fields:
                print(f"  {label:<15}: {acc.get(key,'N/A')}")
            pause()

        elif ch == "4":
            warn("Freezing will lock all transactions!")
            if input("  Type FREEZE to confirm: ").strip() == "FREEZE":
                acc["is_frozen"] = True
                save_data(data)
                success("Account frozen. Contact admin to unfreeze."); pause(); break
            else: info("Cancelled."); pause()

        elif ch == "0": break

# ─────────────────────────────────────────
#  13. MINI STATEMENT
# ─────────────────────────────────────────
def mini_statement(acc):
    clear(); banner(); heading("MINI STATEMENT", "📋"); divider()
    print(f"  {acc['account_number']} | {acc['name']}")
    divider()
    txns = acc["transactions"]
    if not txns: info("No transactions."); pause(); return
    for t in reversed(txns[-10:]):
        sign  = "+" if t["type"]=="CREDIT" else "-"
        color = "green" if t["type"]=="CREDIT" else "red"
        amt_str = f"{sign}₹{t['amount']:,.2f}"
        cat_str = t.get('category','General')
        print(f"  {t['timestamp']}  {clr(amt_str, color)}")
        print(f"  {clr(cat_str,'cyan')} | Bal: ₹{t['balance']:,.2f} | {t['note']}")
        print()
    divider()
    bal_str = f"₹{acc['balance']:,.2f}"
    print(f"  Current Balance : {clr(bal_str, 'green')}")
    pause()

# ─────────────────────────────────────────
#  14. ACCOUNT DASHBOARD
# ─────────────────────────────────────────
def account_dashboard(data, acc_no):
    while True:
        acc = data["accounts"][acc_no]
        clear(); banner()
        heading(f"Welcome, {acc['name']}  |  {acc['account_type']}", "🏠")
        bal_disp = f"₹{acc['balance']:,.2f}"
        print(f"  Account  : {acc_no}   |   Balance: {clr(bal_disp, 'green')}")
        print(f"  Points   : {clr(str(acc.get('reward_points',0))+' pts','yellow')}   "
              f"|   Daily Left: ₹{acc.get('daily_limit',50000)-acc.get('daily_spent',0):,.0f}")
        divider()
        print("  [1]  Balance / Net Worth Dashboard  [2]  Deposit Money")
        print("  [3]  Withdraw Money                 [4]  Fund Transfer")
        print("  [5]  Mini Statement                 [6]  Fixed Deposits")
        print("  [7]  Loan Management                [8]  Bill Payments")
        print("  [9]  Savings Goals                  [10] Spending Analytics")
        print("  [11] Reward Points                  [12] Account Settings")
        print("  [0]  Logout")
        divider()
        ch = input("  Select : ").strip()

        if   ch=="1":  net_worth_dashboard(data, acc_no)
        elif ch=="2":  credit_amount(data, acc_no)
        elif ch=="3":  debit_amount(data, acc_no)
        elif ch=="4":  fund_transfer(data, acc_no)
        elif ch=="5":  mini_statement(acc)
        elif ch=="6":  fixed_deposit_menu(data, acc_no)
        elif ch=="7":  loan_menu(data, acc_no)
        elif ch=="8":  bill_payment(data, acc_no)
        elif ch=="9":  savings_goals(data, acc_no)
        elif ch=="10": spending_analytics(data, acc_no)
        elif ch=="11": reward_points(data, acc_no)
        elif ch=="12": account_settings(data, acc_no)
        elif ch=="0":
            info("Logged out. Have a great day! 👋"); pause(); break
        else: error("Invalid option."); pause()

# ─────────────────────────────────────────
#  15. ADMIN PANEL
# ─────────────────────────────────────────
def admin_panel(data):
    clear(); banner(); heading("ADMIN LOGIN", "🔑"); divider()
    if hash_pin(input("  Admin PIN : ").strip()) != data["admin"]["pin"]:
        error("Wrong PIN."); pause(); return

    while True:
        clear(); banner(); heading("ADMIN PANEL", "🛡"); divider()
        print("  [1] All Accounts Summary")
        print("  [2] Search Account")
        print("  [3] Freeze / Unfreeze Account")
        print("  [4] Bank Statistics")
        print("  [5] Change Admin PIN")
        print("  [0] Exit")
        divider()
        ch = input("  Option : ").strip()

        if ch == "1":
            clear(); banner(); heading("ALL ACCOUNTS", "📋"); divider()
            print(f"  {'ACC NO':<15} {'NAME':<20} {'TYPE':<10} {'BALANCE':>12}  STATUS")
            divider()
            for an, a in data["accounts"].items():
                frozen = clr("FROZEN","red") if a.get("is_frozen") else clr("ACTIVE","green")
                print(f"  {an:<15} {a['name']:<20} {a['account_type']:<10} ₹{a['balance']:>10,.2f}  {frozen}")
            pause()

        elif ch == "2":
            q = input("  Search (name/acc): ").strip().upper()
            for an, a in data["accounts"].items():
                if q in an or q in a["name"].upper():
                    print(f"\n  {clr(an,'cyan')} | {a['name']} | {a['account_type']} | ₹{a['balance']:,.2f}")
                    print(f"  Phone: {a['phone']} | Email: {a['email']} | Pts: {a.get('reward_points',0)}")
            pause()

        elif ch == "3":
            an = input("  Account No : ").strip().upper()
            if an not in data["accounts"]: error("Not found."); pause(); continue
            acc = data["accounts"][an]
            current = "FROZEN" if acc.get("is_frozen") else "ACTIVE"
            print(f"  {an} is currently {current}")
            action = input("  [1] Freeze  [2] Unfreeze : ").strip()
            if action == "1": acc["is_frozen"] = True;  success("Account frozen.")
            elif action=="2": acc["is_frozen"] = False; success("Account unfrozen.")
            save_data(data)
            pause()

        elif ch == "4":
            clear(); banner(); heading("BANK STATISTICS", "📊"); divider()
            accounts     = data["accounts"]
            total_acc    = len(accounts)
            total_bal    = sum(a["balance"] for a in accounts.values())
            total_txns   = sum(len(a["transactions"]) for a in accounts.values())
            total_fds    = sum(len(a.get("fixed_deposits",[])) for a in accounts.values())
            total_loans  = sum(len(a.get("loans",[])) for a in accounts.values())
            total_pts    = sum(a.get("reward_points",0) for a in accounts.values())
            frozen_count = sum(1 for a in accounts.values() if a.get("is_frozen"))
            print(f"  Total Accounts     : {total_acc}")
            print(f"  Total Balance      : ₹{total_bal:,.2f}")
            print(f"  Total Transactions : {total_txns}")
            print(f"  Total FDs          : {total_fds}")
            print(f"  Total Loans        : {total_loans}")
            print(f"  Total Reward Pts   : {total_pts}")
            print(f"  Frozen Accounts    : {frozen_count}")
            pause()

        elif ch == "5":
            old = input("  Current Admin PIN : ").strip()
            if hash_pin(old) != data["admin"]["pin"]: error("Wrong."); pause(); continue
            new = input("  New Admin PIN     : ").strip()
            data["admin"]["pin"] = hash_pin(new)
            save_data(data)
            success("Admin PIN updated."); pause()

        elif ch == "0": break

# ─────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────
def main():
    data = load_data()
    while True:
        clear(); banner()
        print(clr("  MAIN MENU", "bold"))
        divider()
        print("  [1] Create New Account")
        print("  [2] Customer Login")
        print("  [3] Admin Panel")
        print("  [0] Exit")
        divider()
        ch = input("  Select : ").strip()

        if   ch=="1": create_account(data)
        elif ch=="2":
            acc = login(data)
            if acc: account_dashboard(data, acc)
        elif ch=="3": admin_panel(data)
        elif ch=="0":
            clear(); banner()
            print(clr("  Thank you for banking with Python National Bank PRO!", "green"))
            print(clr("  Have a wonderful day! 🌟\n", "yellow"))
            break
        else: error("Invalid."); pause()

if __name__ == "__main__":
    main()
