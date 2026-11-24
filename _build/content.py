"""Content for every page of the HR Connect website.

Only describe features that are live in the HR Connect app. Not live yet (keep off
the site until they ship): asset tracking, performance reviews, access/ID cards,
attendance and shifts, recruitment, payroll tax calculation and filing, government returns,
sending salary payments, non-monthly pay schedules, third-party integrations.

Audience: growing companies anywhere. Keep copy country-neutral: no country-specific laws,
holidays or tax terms. Example amounts in mocks use $; the multi-location mock shows several currencies.
"""

# ---------------------------------------------------------------- site settings
# Placeholders: replace before going live.
SITE_URL = "https://www.hrconnect.ai"
APP_URL = "https://app.hrconnect.ai"
CONTACT_EMAIL = "hello@hrconnect.ai"
TAGLINE = "HR, payroll and expense software for growing companies."

# ---------------------------------------------------------------- products
# (slug, name, menu description, icon)
PRODUCTS = [
    ("core-hr", "Core HR & Employee Records", "Profiles, documents and org chart", "users"),
    ("payroll", "Payroll", "Monthly payroll with approvals and payslips", "banknote"),
    ("leave", "Leave Management", "Time-off requests, balances and carry-over", "calendar"),
    ("expenses", "Expenses & Advances", "Claims with AI receipt scanning", "receipt"),
    ("loans", "Employee Loans", "Loans repaid through payroll", "wallet"),
    ("offboarding", "Offboarding & Final Settlement", "Exit checklist and final pay", "logout"),
    ("self-service", "Employee Self-Service", "Everything employees need, in one place", "user"),
    ("ai", "HR AI Assistant", "Answers from your policies and our guides", "sparkles"),
    ("policies", "Company Policies", "Publish policies employees can read", "file"),
    ("celebrations", "Employee Celebrations", "Automatic birthday and anniversary cards", "gift"),
    ("reports", "Dashboards & Reports", "Dashboards for every role", "chart"),
]
SOLUTIONS = [
    ("hr-teams", "For HR Teams", "Less admin, one source of truth", "users"),
    ("finance-teams", "For Finance & Payroll Teams", "Accurate payroll and spend control", "banknote"),
    ("business-owners", "For Business Owners", "Your workforce at a glance", "building"),
    ("employees", "For Employees & Managers", "Requests and approvals in one portal", "user"),
]
TOOLS = [
    ("leave-balance-calculator", "Leave Balance Calculator", "Leave earned and remaining", "calendar"),
]

def P(slug):
    return f"/product/{slug}/"

NAV = [
    ("Product", [("Platform overview", "/product/", "layers", "Every module in one place")] +
                [(n, P(s), ic, d) for s, n, d, ic in PRODUCTS]),
    ("Solutions", [(n, f"/solutions/{s}/", ic, d) for s, n, d, ic in SOLUTIONS]),
    ("Resources", [("Resources hub", "/resources/", "book", "Guides, tools and articles"),
                   ("Blog", "/blog/", "file", "HR and payroll articles"),
                   ("HR Glossary", "/glossary/", "list", "HR terms explained"),
                   ("Help Center", "/help/", "message", "How to use HR Connect")] +
                  [(n, f"/tools/{s}/", ic, d) for s, n, d, ic in TOOLS]),
    ("Pricing", "/pricing/"),
]

FOOTER = [
    ("Product", [("Platform overview", "/product/")] + [(n, P(s)) for s, n, d, ic in PRODUCTS[:7]] + [("Pricing", "/pricing/")]),
    ("More product", [(n, P(s)) for s, n, d, ic in PRODUCTS[7:]] + [("Security & Privacy", "/security/"), ("Why HR Connect", "/why-hr-connect/")]),
    ("Resources", [("Resources hub", "/resources/"), ("Blog", "/blog/"), ("HR Glossary", "/glossary/"), ("Help Center", "/help/")] +
                  [(n, f"/tools/{s}/") for s, n, d, ic in TOOLS]),
    ("Company", [("About us", "/about/"), ("Contact us", "/contact/"), ("Book a demo", "/book-a-demo/"), ("Careers", "/careers/"),
                 ("Partners & referral", "/partners/"), ("Privacy policy", "/privacy/"), ("Terms of service", "/terms/"), ("Cookie policy", "/cookies/")]),
]

CTA = {"type": "cta"}

def related(slugs, title="Works together with"):
    items = [(ic, n, d, P(s)) for s, n, d, ic in PRODUCTS if s in slugs]
    return {"type": "cards", "title": title, "items": items, "cols": 3, "alt": True}

# ---------------------------------------------------------------- mocks
M_PAYROLL = {"title": "Payroll run · October 2026", "kpis": [("Employees", "48"), ("Gross pay", "$398,400"), ("Net pay", "$301,250")],
             "rows": [("Sarah Mitchell", "Finance · Base salary + bonus", "$9,200", "Approved"),
                      ("David Kim", "Sales · Commission one-off", "$8,450", "Approved"),
                      ("Ashley Martinez", "Joined Oct 12 · pro-rated", "$3,980", "Approved"),
                      ("Chris Nguyen", "Loan installment deducted", "$6,150", "Approved")],
             "foot": "Status: **Approved** · ready to pay"}
M_LEAVE = {"title": "Time-off requests", "kpis": [("Annual left", "14.5 days"), ("Sick used", "3 days"), ("Carried over", "5 days")],
           "rows": [("Michael Brooks", "Annual leave · 4 working days", "", "Pending"),
                    ("Emily Carter", "Bereavement leave · 3 working days", "", "Approved"),
                    ("Jordan Lee", "Sick leave · 1 working day · note attached", "", "Approved"),
                    ("Megan Price", "Parental leave", "", "Approved")]}
M_EXPENSE = {"title": "Expense claim · AI scan", "kpis": [("Merchant", "Union Street Grill"), ("Date", "Nov 8"), ("Amount", "$86.40")],
             "rows": [("Client lunch", "Meals & entertainment · receipt read by AI", "$86.40", "Pending"),
                      ("Rideshare to airport", "Travel", "$42.00", "Approved"),
                      ("Cash advance", "Client visit · adjusted against claims", "$750.00", "Paid")],
             "foot": "Approved claims are reimbursed in the next payroll run"}
M_HR = {"title": "Employee directory", "kpis": [("Headcount", "128"), ("Departments", "9"), ("New this month", "6")],
        "rows": [("Sarah Mitchell", "Finance Manager · London", "", "Active"),
                 ("David Kim", "Account Executive · Toronto", "", "Active"),
                 ("Priya Patel", "HR Specialist · Singapore", "", "Active"),
                 ("Marcus Johnson", "Certification expires in 45 days", "", "Pending")]}
M_LOAN = {"title": "Loan · Chris Nguyen", "kpis": [("Amount", "$6,000"), ("Monthly installment", "$500"), ("Remaining", "$4,000")],
          "rows": [("November 2026", "Installment 5 of 12", "$500", "Scheduled"),
                   ("October 2026", "Installment 4 of 12", "$500", "Paid"),
                   ("September 2026", "Installment 3 of 12", "$500", "Paid")]}
M_OFF = {"title": "Separation · Kevin Walsh", "kpis": [("Type", "Resignation"), ("Last day", "Nov 30"), ("Stage", "Final settlement")],
         "rows": [("Return laptop", "IT · exit checklist", "", "Cleared"),
                  ("Handover to manager", "Department · exit checklist", "", "Cleared"),
                  ("Final settlement", "Salary to last day, leave, deductions", "$7,840", "Pending approval")],
         "foot": "Paid with the **November** payroll run"}
M_SELF = {"title": "My dashboard", "kpis": [("Leave left", "17.5 d"), ("Next payday", "Nov 28"), ("Open requests", "2")],
          "rows": [("October payslip", "Net pay $4,860", "", "Paid"),
                   ("Annual leave Dec 14–17", "Waiting for manager", "", "Pending"),
                   ("Expense claim · rideshare", "$42.00", "", "Approved")]}
M_AI = {"title": "HR assistant", "rows": [("You", "How many days of annual leave can I carry over?", ""),
                                          ("HR Connect AI", "Under the Leave Policy (section 4.2) you can carry over up to 5 days into next year.", ""),
                                          ("You", "Where do I download my payslip?", ""),
                                          ("HR Connect AI", "Go to Me → Payslips, open the month and choose Download.", "")]}
M_POLICY = {"title": "My policies", "rows": [("Leave Policy 2026", "Updated Jan 2, 2026 · PDF", "", "Read"),
                                             ("Code of Conduct", "Updated Mar 15, 2026 · PDF", "", "Read"),
                                             ("Travel & Expenses Policy", "Updated Oct 1, 2026 · PDF", "", "Unread")],
            "foot": "Ask the AI assistant anything about these policies"}
M_CARDS = {"title": "Celebrations this week", "rows": [("Olivia Turner", "Birthday · Tuesday", "", "Scheduled"),
                                                       ("Ryan Cooper", "5-year work anniversary · Wednesday", "", "Scheduled"),
                                                       ("Hannah Scott", "Birthday · Monday", "", "Sent")],
           "foot": "Cards are emailed automatically at **9:00 AM**"}
M_REPORTS = {"title": "People dashboard", "kpis": [("Headcount", "128"), ("Payroll cost", "$842K"), ("On leave today", "7")],
             "rows": [("Pending approvals", "Leave 4 · Expenses 6 · Loans 1", "11"),
                      ("Payroll register", "October 2026 · XLSX", ""),
                      ("Leave balances", "All employees · XLSX", "")]}
M_HOME = {"title": "HR Connect · People", "kpis": [("Employees", "128"), ("Payroll this month", "$842K"), ("Approvals", "11")],
          "rows": [("October payroll", "48 employees · $301,250 net", "", "Approved"),
                   ("Emily Carter", "Annual leave · 4 days", "", "Pending"),
                   ("David Kim", "Expense claim · $86.40 · AI scanned", "", "Pending"),
                   ("Kevin Walsh", "Final settlement", "", "In progress")]}

# Connected-hub visual for the AI hero slide: (label, icon, angle in degrees; 0 = right, 90 = down)
AI_HUB = [("Payroll", "banknote", 240), ("Leave", "calendar", 300), ("Expenses", "receipt", 0),
          ("Self-service", "user", 60), ("Policies", "book", 120), ("Loans", "wallet", 180)]

# ---------------------------------------------------------------- product pages
def product_page(slug, title, desc, eyebrow, h1, lead, mk, features, splits, steps, faq, rel):
    name = next(n for s, n, d, ic in PRODUCTS if s == slug)
    blocks = [{"type": "hero", "crumbs": [("Product", "/product/"), (name, P(slug))], "eyebrow": eyebrow, "title": h1, "lead": lead,
               "ctas": [("Book a demo", "/book-a-demo/"), ("See pricing", "/pricing/")], "mock": mk},
              {"type": "features", "title": features[0], "lead": features[1], "items": features[2], "cols": 3}]
    for i, sp in enumerate(splits):
        blocks.append(dict({"type": "split", "rev": i % 2 == 1, "alt": i % 2 == 0}, **sp))
    if steps:
        blocks.append({"type": "steps", "title": steps[0], "items": steps[1]})
    if faq:
        blocks.append({"type": "faq", "items": faq, "alt": True})
    blocks.append(related(rel))
    blocks.append(CTA)
    return {"title": title, "desc": desc, "blocks": blocks}

PAGES = {}

PAGES["product/core-hr"] = product_page(
    "core-hr", "Core HR Software & Employee Records",
    "Keep every employee record in one place: profiles, documents, bank details, compensation history and a live org chart.",
    "Core HR", "Every employee record, **in one place**",
    "Replace scattered spreadsheets with one employee directory. Profiles, documents, bank details and salary history stay up to date, and the org chart updates itself.",
    M_HR,
    ("Everything HR needs to know about each person", "One profile per employee, split into clear sections so the right people see the right details.", [
        ("user", "Complete profiles", "Work details, employee code, address, emergency contacts, dependants and education."),
        ("file", "Documents in one place", "Store IDs, certifications, contracts and other documents, with expiry dates on each profile."),
        ("banknote", "Bank details", "Bank accounts with a verification flag and a full change history, used for payroll bank advice."),
        ("wallet", "Compensation history", "Every salary change is kept, so you can see how pay has moved over time."),
        ("org", "Live org chart", "Built from reporting lines, so it is always current. Employees can see it too."),
        ("building", "Company structure", "Set up divisions, departments, designations with levels, and employee types."),
    ]),
    [{"eyebrow": "Onboarding", "title": "Add an employee in minutes", "text": "A step-by-step wizard collects personal, job, pay and bank details. The new hire gets an email invite to activate their account.",
      "bullets": ["Assign department, designation, manager and payroll setup", "Resend invites or send new login details at any time", "Export the employee list to Excel when you need it"], "mock": M_HR},
     {"eyebrow": "Important dates", "title": "Never miss a birthday or an expiring document", "text": "Important dates show upcoming birthdays and work anniversaries, and document expiry dates are kept on each profile.",
      "bullets": ["Birthday and anniversary cards can be sent automatically", "HR sees what is coming up from the People dashboard"],
      "mock": M_CARDS}],
    ("How it works", [("Set up your structure", "Add divisions, departments, designations and employee types, or use the defaults."),
                      ("Add or import employees", "Use the add-employee wizard for each person and invite them to the app."),
                      ("Keep it current", "Employees update their own details through self-service. HR approves what matters.")]),
    [("Can employees edit their own profile?", "Yes. In the Me workspace employees can view and update their own details. What they can change depends on the permissions you give their role."),
     ("Who can see salary and bank details?", "Only roles you allow. Permissions are set per module and per action, and can be overridden for individual users."),
     ("Can I export the employee list?", "Yes. HR can export the directory to Excel.")],
    ["payroll", "leave", "self-service"])

PAGES["product/payroll"] = product_page(
    "payroll", "Payroll Software with Approvals & Pay Stubs",
    "Run monthly payroll in any currency with a clear approval flow, automatic pro-rating, loans, expenses and final settlements included, then issue payslips and a bank payment file.",
    "Payroll", "Monthly payroll, **approved and paid** without the spreadsheet",
    "Set up pay once, then run payroll in a few clicks. HR Connect pulls in loans, expenses, advances and final settlements, routes the run for approval, and issues payslips when it's paid.",
    M_PAYROLL,
    ("Built for how payroll really runs", "Every step is tracked, from calculation to payment.", [
        ("layers", "Payroll setup wizard", "Choose country and currency, add earnings and deductions, and set leave and final pay rules."),
        ("refresh", "Recalculate any time", "Open runs can be recalculated as often as you like. Before submitting you see exactly what changed."),
        ("check", "Approval flow", "Runs move from open to pending approval, approved and paid. Rejections need a reason and go back for editing."),
        ("calendar", "Pro-rating for new joiners", "Employees who join mid-month are paid for the days they worked, automatically."),
        ("download", "Bank payment file", "Export the bank advice file as CSV or XLSX to pay employees through your bank."),
        ("file", "Payslips", "Paying a run issues payslips that employees can view and download as PDF."),
    ]),
    [{"eyebrow": "Everything in one run", "title": "Loans, expenses and final settlements, included", "text": "You don't need to add them by hand. When a run is calculated, HR Connect brings in everything that's due that month.",
      "bullets": ["Loan disbursements and monthly installments", "Approved expense claims and cash advances", "One-off earnings and deductions, such as bonuses or commission", "Final settlements for employees leaving that month"], "mock": M_PAYROLL},
     {"eyebrow": "Accurate in every currency", "title": "Money handled the way accountants expect", "text": "Amounts are stored in whole minor units, such as cents or pence, so totals don't drift through rounding.",
      "bullets": ["Separate payroll setups for different countries, currencies or entities", "Payroll analytics show cost trends over time", "A full history of every run and who approved it"],
      "mock": M_REPORTS}],
    ("Run payroll in four steps", [("Create the run", "Pick the payroll setup and month. HR Connect calculates every employee straight away."),
                                   ("Review and adjust", "Add one-off earnings or deductions, then recalculate."),
                                   ("Submit for approval", "An approver checks the totals and approves or rejects with a reason."),
                                   ("Pay and issue payslips", "Mark the run paid. Payslips go out, and loans, expenses and final settlements update.")]),
    [("How often can I run payroll?", "Payroll runs monthly. Each payroll setup has one run per month. Weekly, biweekly and semimonthly pay schedules aren't available yet."),
     ("Can I pay staff in different countries or currencies?", "Yes. Create a payroll setup for each country, currency or entity and assign employees to the right one."),
     ("Can I add my own earnings and deductions?", "Yes. Add any earning or deduction as a component in your payroll setup, for example a bonus, an allowance or a benefits deduction."),
     ("Does HR Connect file taxes or pay employees?", "No. HR Connect doesn't calculate or file payroll taxes or government returns, and it doesn't send payments. It produces a bank payment file (CSV or XLSX) that you use to pay employees through your bank.")],
    ["loans", "expenses", "offboarding"])

PAGES["product/leave"] = product_page(
    "leave", "Leave Management Software",
    "Leave requests, approvals and balances in one place, with carry-over, attachments and your own leave types.",
    "Leave management", "Time off and balances, **without the back-and-forth**",
    "Employees request time off in seconds and see their balance before they do. Managers approve from one list. Balances update and carry over automatically.",
    M_LEAVE,
    ("Leave that follows your rules", "Configure leave once in your payroll setup. HR Connect does the counting.", [
        ("list", "Leave types ready to use", "Annual, sick, maternity, paternity, emergency and bereavement, plus your own."),
        ("calendar", "Working days counted for you", "Requests count working days using your weekend days, so a request that spans a weekend is counted correctly, whichever days your weekend falls on."),
        ("check", "Simple approvals", "Approve to deduct the balance. Reject with a reason so the employee knows why."),
        ("file", "Attachments", "Employees can attach up to four files, such as a medical note."),
        ("refresh", "Carry-over", "Unused annual leave rolls into the next year under your carry-over rules. HR can preview it before year-end."),
        ("chart", "Clear balances", "Allocated, used, carried over and remaining days for every leave type."),
    ]),
    [{"eyebrow": "For HR", "title": "Every request and balance, one screen", "text": "See a calendar of who's off, open any pending request, or create a request on an employee's behalf.",
      "bullets": ["Filter requests by employee and status", "Leave balances export for reporting", "Pending requests can be edited or withdrawn, approved ones are locked"], "mock": M_LEAVE}],
    ("How it works", [("Set your leave rules", "Choose leave types, days per year, weekend days and carry-over in your payroll setup."),
                      ("Employees request leave", "They pick dates and a type, see working days counted, and submit."),
                      ("Approve and track", "Approvals update balances straight away, and carry-over runs at year-end.")]),
    [("Can I add my own leave types?", "Yes. Add custom leave types alongside the standard ones in HR settings."),
     ("Does it handle different work weeks?", "Yes. Weekend days are set per payroll setup, so teams with different schedules can each have their own."),
     ("Can HR apply leave on behalf of an employee?", "Yes. HR can create, approve or reject requests for any employee they manage."),
     ("Want to check a balance quickly?", "Try our free [leave balance calculator](/tools/leave-balance-calculator/).")],
    ["payroll", "self-service", "reports"])

PAGES["product/expenses"] = product_page(
    "expenses", "Expense Management with AI Receipt Scanning",
    "Expense claims and cash advances with AI receipt scanning, approvals and reimbursement through payroll.",
    "Expenses & advances · Premium", "Snap the receipt. **AI fills in the claim.**",
    "Employees upload a receipt and HR Connect reads the merchant, date and amount for them. Approved claims and cash advances are paid through payroll, so finance has one process instead of two.",
    M_EXPENSE,
    ("Spend control without the paperwork", "From claim to reimbursement, everything is tracked.", [
        ("sparkles", "AI receipt scanning", "Upload a photo or PDF and the claim is filled in for you, with a confidence score for each field."),
        ("list", "Your own categories", "Set up expense categories that match how you account for spend."),
        ("check", "Approvals", "Claims go to an approver before they are paid."),
        ("wallet", "Cash advances", "Give employees an advance for a trip, send reminders, and adjust it against their claims."),
        ("banknote", "Paid through payroll", "Approved claims and advances are included in the next payroll run."),
        ("chart", "Expense analytics", "See spend by category, employee and month."),
    ]),
    [{"eyebrow": "Advances", "title": "Advances that close themselves", "text": "When an employee spends an advance, their claims are adjusted against it. Finance can see what is still outstanding.",
      "bullets": ["Reminders for advances that haven't been settled", "Advances paid out through payroll", "A clear history for every employee"], "mock": M_EXPENSE}],
    ("How it works", [("Employee submits", "Upload a receipt. AI fills in the details, the employee checks them and submits."),
                      ("Manager approves", "The approver sees the receipt and the details side by side."),
                      ("Payroll reimburses", "Approved claims are added to the next payroll run and marked paid.")]),
    [("Which plan includes expenses?", "Expenses & Advances is part of the [Premium plan](/pricing/)."),
     ("What can the AI read?", "Receipts and invoices as images or PDFs. It reads the merchant, date, amount and other details, and the employee can correct anything before submitting."),
     ("Are expenses paid separately?", "No. Approved claims are reimbursed with the next payroll run, so there is one payment to make.")],
    ["payroll", "ai", "reports"])

PAGES["product/loans"] = product_page(
    "loans", "Employee Loan Management",
    "Employee loan requests with approvals and monthly installments deducted from payroll automatically.",
    "Employee loans", "Employee loans, **repaid automatically** through payroll",
    "Employees request a loan, you approve it, and HR Connect pays it out and deducts each installment from payroll until it's repaid.",
    M_LOAN,
    ("Loans without a tracking spreadsheet", "", [
        ("message", "Loan requests", "Employees request a loan from self-service with the amount and reason."),
        ("check", "Approval workflow", "Approvers review the request before anything is paid."),
        ("banknote", "Disbursed with payroll", "Approved loans are paid out in the payroll run."),
        ("calendar", "Repayment schedule", "A clear installment plan, month by month."),
        ("refresh", "Change the installment", "Adjust the monthly installment if circumstances change."),
        ("chart", "Always up to date", "Remaining balance updates every time payroll is paid."),
    ]),
    [],
    ("How it works", [("Request", "The employee asks for a loan and chooses a repayment period."),
                      ("Approve", "HR or finance approves the request."),
                      ("Repay", "Each month's installment is deducted in payroll until the loan is cleared.")]),
    [("What happens if an employee leaves with a loan outstanding?", "The remaining balance can be recovered in the final settlement when you process their offboarding, where the law allows."),
     ("Can employees see their loan balance?", "Yes. Employees see their loans, installments and remaining balance in self-service.")],
    ["payroll", "offboarding", "self-service"])

PAGES["product/offboarding"] = product_page(
    "offboarding", "Employee Offboarding Software",
    "Manage resignations and terminations with approvals, an exit checklist and a final settlement paid through payroll.",
    "Offboarding", "Clean exits, **from resignation to final pay**",
    "Every separation follows the same steps: approval, exit checklist, final settlement and payment. Nothing gets missed and the employee is paid correctly on the way out.",
    M_OFF,
    ("Every step of an exit, tracked", "", [
        ("list", "All separation types", "Resignation, termination, job abandonment, retirement, contract end and death."),
        ("org", "Reassign direct reports", "If the employee manages people, their reports must be reassigned before the case goes ahead."),
        ("check", "Approval", "Separations are approved before work starts."),
        ("list", "Exit checklist", "Use your own checklist template, such as returning equipment and handover, and clear each item."),
        ("calc", "Final pay worksheet", "Work out final pay, including salary to the last day, unused leave and any deductions, with its own approval."),
        ("banknote", "Paid with payroll", "The final settlement is paid in the payroll run for the last working month, then the employee is marked as exited."),
    ]),
    [{"eyebrow": "Final settlement", "title": "Final pay that matches payroll", "text": "Because the final settlement is paid inside the payroll run, it uses the same pay data and approvals as everyone else's salary.",
      "bullets": ["Outstanding loans can be recovered", "Final pay rules set in your payroll setup", "Check local rules on final pay timing and leave payout before you pay"],
      "mock": M_OFF}],
    ("The offboarding steps", [("Request", "Start a separation from the directory, with type, reason and last working day."),
                               ("Approval", "The separation is approved."),
                               ("Exit checklist", "Each checklist item is cleared."),
                               ("Final settlement", "The final pay is approved and paid in payroll. The employee is marked exited.")]),
    [("Can a separation be withdrawn?", "Yes. A case can be withdrawn or cancelled before it is completed."),
     ("Can I customize the exit checklist?", "Yes. Set up your own exit checklist template in HR settings.")],
    ["payroll", "loans", "core-hr"])

PAGES["product/self-service"] = product_page(
    "self-service", "Employee Self-Service Portal",
    "Give employees one place for payslips, leave, loans, expenses, policies and their own profile.",
    "Employee self-service", "Fewer questions to HR. **Happier employees.**",
    "Every employee gets their own workspace. They can check payslips, request leave, claim expenses and read policies without emailing HR.",
    M_SELF,
    ("What employees can do on their own", "", [
        ("user", "My profile", "View and update personal details, contacts, dependants and education."),
        ("file", "My payslips", "View and download every payslip as PDF."),
        ("calendar", "My leave", "Check balances, request leave and track approvals."),
        ("receipt", "My expenses & advances", "Submit claims with AI receipt scanning and request advances."),
        ("wallet", "My loans", "Request a loan and follow the repayment schedule."),
        ("book", "My policies", "Read company policies and ask the AI assistant about them."),
    ]),
    [{"eyebrow": "Two workspaces", "title": "“Me” for employees, “People” for HR", "text": "Everyone sees a workspace built for them. Employees see their own information in Me. HR and managers manage the company in People, based on their permissions.",
      "bullets": ["Personal dashboard with leave, payday and open requests", "Org chart to find colleagues", "Notifications when something needs attention"], "mock": M_SELF}],
    None,
    [("Does it work on mobile?", "Yes. HR Connect works in the browser on phones, tablets and computers. There is no separate app to install."),
     ("Can I limit what employees see?", "Yes. Each role has its own permissions, so you control what's available in self-service.")],
    ["leave", "expenses", "ai"])

PAGES["product/ai"] = product_page(
    "ai", "HR AI Assistant",
    "AI that answers employee questions from your company policies, helps users find their way around HR Connect, and reads receipts.",
    "AI in HR Connect", "An HR assistant that **knows your policies**",
    "Employees ask questions in plain language and get answers from your own policy documents. The same AI helps people use HR Connect and fills in expense claims from receipts.",
    M_AI,
    ("Three ways AI saves your team time", "", [
        ("book", "Policy answers", "Upload your policies and employees can ask questions about them. Answers come from your documents."),
        ("message", "In-app help", "Stuck? The assistant explains how to do things in HR Connect, step by step."),
        ("sparkles", "Receipt and document reading", "Upload a receipt and the AI fills in the merchant, date and amount for you."),
    ]),
    [{"eyebrow": "Your documents, your answers", "title": "Answers based on what you've published", "text": "The assistant answers from the policies you upload and HR Connect's own product guides, so employees get your rules, not generic advice.",
      "bullets": ["Fewer repeat questions to HR", "Available any time employees need it", "Update a policy and answers update too"], "mock": M_AI}],
    None,
    [("Which AI models do you use?", "HR Connect uses large language models from established AI providers to answer questions and read documents. See our [privacy policy](/privacy/) for how data is handled."),
     ("Does the AI make decisions about employees?", "No. The AI answers questions and fills in forms. Approvals and pay decisions are always made by people.")],
    ["policies", "expenses", "self-service"])

PAGES["product/policies"] = product_page(
    "policies", "Company Policy Management",
    "Publish company policies in one place, let employees read them, and answer questions with the HR AI assistant.",
    "Company policies", "Your policies, **where employees will actually read them**",
    "Upload your handbook and policies once. Employees find them under My Policies, and can ask the AI assistant what they mean.",
    M_POLICY,
    ("One home for your policies", "", [
        ("file", "Upload and publish", "Add policy documents and make them available to employees."),
        ("book", "My Policies", "Employees see every policy that applies to them in self-service."),
        ("sparkles", "Ask the AI", "Employees ask questions and get answers from your policies."),
    ]),
    [],
    ("How it works", [("Upload", "HR uploads policy documents."), ("Publish", "Employees see them in My Policies."), ("Ask", "Employees ask the assistant about anything in them.")]),
    [("What file types can I upload?", "Upload policies as documents such as PDF. They're prepared for the AI assistant automatically.")],
    ["ai", "self-service", "core-hr"])

PAGES["product/celebrations"] = product_page(
    "celebrations", "Employee Birthday & Anniversary Cards",
    "Send automatic birthday and work-anniversary e-cards to employees, with your own message, theme and send time.",
    "Employee celebrations", "Remember **every birthday and work anniversary**",
    "HR Connect emails a card to employees on their birthday and work anniversary, automatically. Set it up once and nobody gets forgotten.",
    M_CARDS,
    ("Small touches that build culture", "", [
        ("gift", "Birthday cards", "An e-card on every employee's birthday."),
        ("calendar", "Work anniversaries", "Celebrate each year with the company."),
        ("mail", "Sent automatically", "Choose the send time and cards go out by email on the day."),
        ("sparkles", "Your style", "Set the message, theme and sender name."),
        ("users", "Important dates view", "See upcoming birthdays and anniversaries in HR Connect."),
        ("clock", "No reminders needed", "Dates come from employee profiles, so new joiners are included automatically."),
    ]),
    [], None, None,
    ["core-hr", "self-service", "reports"])

PAGES["product/reports"] = product_page(
    "reports", "HR Dashboards & Reports",
    "Dashboards for employees, HR and admins, plus payroll, leave, headcount and expense reports you can export.",
    "Dashboards & reports", "The numbers you need, **the moment you log in**",
    "Every role gets a dashboard that shows what matters to them, and the reports HR and finance ask for most are a click away.",
    M_REPORTS,
    ("See what's happening across your company", "", [
        ("chart", "Role-based dashboards", "Employees, HR and admins each see their own dashboard. Tiles appear only if you have permission to see them."),
        ("banknote", "Payroll analytics", "Payroll cost and trends by month."),
        ("receipt", "Expense analytics", "Spend by category, employee and month."),
        ("download", "Exports", "Payroll register, leave balances and headcount reports to Excel."),
        ("list", "Approvals at a glance", "Pending leave, expenses, loans and payroll approvals in one place."),
        ("info", "Notifications", "Alerts for things that need attention, from information to urgent."),
    ]),
    [], None, None,
    ["payroll", "expenses", "leave"])

# ---------------------------------------------------------------- product overview
PAGES["product"] = {"title": "HR Connect Platform", "desc": "One platform for core HR, payroll, leave, expenses, loans, offboarding, self-service and AI.",
  "blocks": [
    {"type": "hero", "eyebrow": "Platform", "title": "Everything HR, **one connected platform**",
     "lead": "Core HR, payroll, leave, expenses, loans and offboarding share the same employee data, so a change in one place flows everywhere it should.",
     "ctas": [("Book a demo", "/book-a-demo/"), ("See pricing", "/pricing/")], "mock": M_HOME},
    {"type": "cards", "title": "The modules", "lead": "Start with what you need and switch on more modules as you grow.",
     "items": [(ic, n, d, P(s)) for s, n, d, ic in PRODUCTS], "cols": 3},
    {"type": "split", "alt": True, "eyebrow": "Connected", "title": "Payroll at the centre", "text": "Payroll brings in everything that affects pay. You don't re-type numbers between systems.",
     "bullets": ["Approved time off and pro-rating for new hires", "Loan installments and cash advances", "Approved expense claims", "Final settlements for leavers"], "mock": M_PAYROLL},
    {"type": "features", "title": "Built in, not bolted on", "items": [
        ("shield", "Roles & permissions", "Control every module and action per role, with overrides for individual users."),
        ("globe", "Multi-currency", "Separate payroll setups per country, currency or entity."),
        ("sparkles", "AI throughout", "Receipt scanning, policy answers and in-app help."),
    ]},
    CTA]}

# ---------------------------------------------------------------- home
# Solutions slider on the home page. Mock rows: (title, detail, value, pill, initials);
# a pill can be (label, colour) to override its default colour.
SPOTLIGHT = {"type": "spotlight", "eyebrow": "Solutions", "title": "Made for every team that touches HR",
  "lead": "See how HRConnect.AI works for the people who use it every day.",
  "slides": [
    {"tab": "HR Teams", "eyebrow": "For HR Teams", "title": "Less admin, one source of truth",
     "text": "Keep employee records, time off, offboarding and policies in one place, and let employees serve themselves.",
     "bullets": ["Complete employee profiles with documents and org chart", "Time-off requests, balances and carry-over handled for you", "Exit checklists that finish with a final settlement"],
     "cta": ("See HR Teams", "/solutions/hr-teams/"),
     "mock": {"title": "People · Records", "kpis": [("Employees", "128"), ("On leave", "6"), ("Docs expiring", "3")],
              "rows": [("Emily Carter", "Certification expires in 21 days", "", "Renew"),
                       ("Daniel Reyes", "Joined Nov 3 · profile complete", "", "Done"),
                       ("Jessica Lee", "Annual leave · 5 days", "", "Approved")],
              "foot": "All records up to date except **3 documents**"}},
    {"tab": "Finance & Payroll", "eyebrow": "For Finance & Payroll Teams", "title": "Accurate payroll and spend control",
     "text": "Approved payroll runs, expense control and loan tracking in one place, with exports for the bank.",
     "bullets": ["Approval flow from calculation to payment", "Expense claims with AI receipt scanning", "Bank advice files in CSV or XLSX"],
     "cta": ("See Finance Teams", "/solutions/finance-teams/"),
     "mock": {"title": "Finance · November 2026", "kpis": [("Net payroll", "$301K"), ("Expenses", "$9.6K"), ("Loans open", "9")],
              "rows": [("November payroll", "48 employees", "$301,250", "Pending", "PR"),
                       ("Expense claims", "14 claims · AI scanned", "$9,640", "Approved", "EX"),
                       ("Loan installments", "Deducted through payroll", "$4,800", ("Scheduled", ""), "LN")],
              "foot": "Bank file ready once payroll is **approved**"}},
    {"tab": "Business Owners", "eyebrow": "For Business Owners", "title": "Your workforce at a glance",
     "text": "A clear view of headcount, payroll cost and approvals, and the confidence that HR runs properly.",
     "bullets": ["Headcount and payroll cost on one dashboard", "Approvals that never get stuck in someone's inbox", "Policies and records that stay audit-ready"],
     "cta": ("See Business Owners", "/solutions/business-owners/"),
     "mock": {"title": "Owner overview", "kpis": [("Headcount", "128"), ("Payroll cost", "$842K"), ("Approvals", "4")],
              "rows": [("Sales", "34 people · +3 this quarter", "$236K", ("Growing", "ok"), "SL"),
                       ("Operations", "52 people", "$268K", "Stable", "OP"),
                       ("Finance", "11 people", "$104K", "Stable", "FN")],
              "foot": "Payroll cost is **2.1% under budget** this month"}},
    {"tab": "Employees & Managers", "eyebrow": "For Employees & Managers", "title": "Requests and approvals in one portal",
     "text": "Employees see payslips, request leave, claim expenses and get answers. Managers approve from one list.",
     "bullets": ["Payslips and documents employees can download", "Leave and expense requests from any device", "AI answers to policy questions, any time"],
     "cta": ("See Employees & Managers", "/solutions/employees/"),
     "mock": {"title": "My approvals",
              "rows": [("David Kim", "Expense claim · $86.40", "", "Approve"),
                       ("Ashley Martinez", "Annual leave · 3 days", "", "Approve"),
                       ("Chris Nguyen", "Salary advance · $1,000", "", "Approve"),
                       ("Sarah Mitchell", "Remote day · Thursday", "", "Approved")],
              "foot": "**3 requests** waiting for you"}},
    {"tab": "Global Teams", "eyebrow": "For teams in more than one country", "title": "One platform, wherever your people are",
     "text": "Run payroll in each team's currency, set leave rules and weekends per location, and give every employee self-service from any browser.",
     "bullets": ["Separate payroll setups per country, currency or entity", "Leave rules and weekend days set per payroll setup", "Self-service on phones, tablets and computers"],
     "cta": ("See payroll", "/product/payroll/"),
     "mock": {"title": "Entities · Payroll currency",
              "rows": [("United Kingdom", "38 employees", "GBP", "Active", "UK"),
                       ("Germany", "29 employees", "EUR", "Active", "DE"),
                       ("Canada", "19 employees", "CAD", "Active", "CA"),
                       ("Singapore", "42 employees", "SGD", "Active", "SG")],
              "foot": "**4 entities** · one platform"}},
  ]}

PAGES[""] = {"title": "HR Connect | HR, Payroll & Expense Software for Growing Companies",
  "desc": "HR Connect brings core HR, payroll, leave, expenses, loans and offboarding together in one simple platform, with AI built in.",
  "blocks": [
    # Rotating hero: AI slide first (its heading is the page's only <h1>), then one slide per key product.
    {"type": "hero_slider", "interval": 6000, "slides": [
        {"eyebrow": "AI-powered HR", "title": "The AI-powered HR app that **connects everything**",
         "lead": "Records, payroll, leave and expenses share one set of data, and AI does the busywork: reading receipts, answering policy questions and guiding people through the app.",
         "ctas": [("Book a demo", "/book-a-demo/"), ("Meet the AI assistant", P("ai"))],
         "trust": ["Reads receipts", "Answers from your policies", "In-app help"], "visual": AI_HUB},
        {"eyebrow": "Payroll", "title": "Monthly payroll, **approved and paid**",
         "lead": "Loans, expenses, advances and final settlements are pulled into every run. Route it for approval, mark it paid and payslips go out automatically.",
         "ctas": [("Explore payroll", P("payroll")), ("Book a demo", "/book-a-demo/")], "mock": M_PAYROLL},
        {"eyebrow": "Leave management", "title": "Leave requests, **without the back-and-forth**",
         "lead": "Employees see their balance before they ask. Managers approve from one list, working days are counted for you and unused leave carries over.",
         "ctas": [("Explore leave", P("leave")), ("Book a demo", "/book-a-demo/")], "mock": M_LEAVE},
        {"eyebrow": "Expenses & advances", "title": "Snap the receipt. **AI fills in the claim.**",
         "lead": "AI reads the merchant, date and amount from each receipt. Approved claims and cash advances are paid through payroll, so finance has one process.",
         "ctas": [("Explore expenses", P("expenses")), ("Book a demo", "/book-a-demo/")], "mock": M_EXPENSE},
    ]},
    SPOTLIGHT,
    {"type": "cards", "eyebrow": "One platform", "title": "Everything your HR team runs on", "lead": "Each module works on its own and gets better together.",
     "items": [(ic, n, d, P(s)) for s, n, d, ic in PRODUCTS[:6]], "cols": 3},
    {"type": "split", "alt": True, "eyebrow": "Payroll", "title": "Payroll that pulls everything in", "text": "Loans, expenses, advances, new hires and final settlements are all included in the run, then approved, paid and turned into payslips.",
     "bullets": ["Approval flow from calculation to payment", "Bank payment file in CSV or XLSX", "Payslips employees can download"], "mock": M_PAYROLL, "ctas": [("Explore payroll", P("payroll"))]},
    {"type": "split", "rev": True, "eyebrow": "AI built in", "title": "Less typing, fewer questions", "text": "AI reads receipts to fill in expense claims, and answers employee questions from your own company policies.",
     "bullets": ["Receipt scanning for expense claims", "Policy questions answered from your documents", "In-app help when someone gets stuck"], "mock": M_AI, "ctas": [("Meet the HR AI assistant", P("ai"))]},
    {"type": "split", "alt": True, "eyebrow": "Self-service", "title": "Employees help themselves", "text": "Payslips, leave balances, expense claims, loans and policies are all in one place, on any device.",
     "bullets": ["Fewer emails and questions to HR", "Requests tracked from start to finish", "Works in the browser on phones and computers"], "mock": M_SELF, "ctas": [("See self-service", P("self-service"))]},
    {"type": "features", "eyebrow": "Made for growing teams", "title": "Works the way your company works", "lead": "Simple enough for a 20-person startup, organized enough for a 500-person company.", "items": [
        ("globe", "Any currency", "Payroll setups per country, currency or entity, accurate to the smallest unit."),
        ("calendar", "Your leave rules", "Set your own leave types, days per year, weekend days and carry-over."),
        ("user", "Remote-ready", "Employees use self-service from any browser, on any device."),
    ]},
    {"type": "steps", "alt": True, "title": "Up and running in three steps", "items": [
        ("Tell us about your company", "We set up your company, departments and payroll rules with you."),
        ("Add your people", "Add employees and invite them to their self-service workspace."),
        ("Run your first payroll", "Approve leave and expenses, then run payroll and issue payslips.")]},
    CTA]}

# ---------------------------------------------------------------- why HR Connect
PAGES["why-hr-connect"] = {"title": "Why HR Connect", "desc": "Why growing companies choose HR Connect over spreadsheets and disconnected HR tools.",
  "blocks": [
    {"type": "hero", "eyebrow": "Why HR Connect", "title": "Stop stitching HR together **from spreadsheets**",
     "lead": "Most growing companies run HR across spreadsheets, email and a separate payroll tool. HR Connect puts it all in one place, so there is one version of the truth.",
     "ctas": [("Book a demo", "/book-a-demo/"), ("See pricing", "/pricing/")]},
    {"type": "features", "title": "Six reasons teams switch", "items": [
        ("layers", "One connected system", "Leave, loans, expenses and final settlements feed payroll directly. No re-typing."),
        ("globe", "Works across borders", "Payroll setups per country and currency, your own leave rules, and self-service on any device."),
        ("sparkles", "AI that does real work", "Receipts read for you and policy questions answered from your own documents."),
        ("user", "Employees serve themselves", "Payslips, leave balances and requests in their own workspace."),
        ("shield", "Control over who sees what", "Permissions per module and action, with per-user overrides."),
        ("check", "Approvals you can trust", "Every payroll run, leave request, claim and loan has a clear approval trail."),
    ]},
    {"type": "table", "alt": True, "title": "HR Connect vs. spreadsheets", "head": ["", "Spreadsheets & email", "HR Connect"], "rows": [
        ["Payroll calculation", "Manual formulas, easy to break", "✓ Calculated from employee data"],
        ["Loans and expenses in payroll", "Copied in by hand", "✓ Included automatically"],
        ["Leave balances", "Updated by HR", "✓ Updated on approval"],
        ["Approvals", "Email threads", "✓ Tracked in the system"],
        ["Payslips", "Built one by one", "✓ Issued when payroll is paid"],
        ["Employee questions", "Answered by HR", "✓ Self-service and AI assistant"],
        ["Access control", "Shared files", "✓ Role-based permissions"],
    ]},
    CTA]}

# ---------------------------------------------------------------- pricing
BASIC = ["Core HR & employee records", "Payroll with approvals and payslips", "Leave management", "Employee loans", "Offboarding & final pay",
         "Employee self-service", "Company policies & HR AI assistant", "Birthday & anniversary cards", "Dashboards & reports", "Roles & permissions", "Email support"]
PAGES["pricing"] = {"title": "Pricing", "desc": "Simple per-employee pricing for HR Connect. Choose Basic or Premium.",
  "blocks": [
    {"type": "hero", "eyebrow": "Pricing", "title": "Simple pricing, **per employee per month**",
     "lead": "Pay only for the employees you have. Choose the plan with the modules you need and switch up as you grow."},
    {"type": "plans", "plans": [
        {"name": "Basic", "price": "Custom quote", "unit": "Priced per employee, per month", "desc": "Everything you need to run HR and payroll.",
         "items": BASIC, "cta": "Get a quote", "href": "/contact/"},
        {"name": "Premium", "price": "Custom quote", "unit": "Priced per employee, per month", "desc": "Everything in Basic, plus spend management.", "featured": True,
         "items": ["Everything in Basic", "**Expenses & advances**", "**AI receipt scanning**", "Expense analytics"],
         "cta": "Book a demo", "href": "/book-a-demo/"}]},
    {"type": "table", "alt": True, "title": "Compare plans", "head": ["Module", "Basic", "Premium"], "rows":
        [[m, "✓", "✓"] for m in BASIC[:-1]] + [["Expenses & advances", "—", "✓"], ["AI receipt scanning", "—", "✓"], ["Expense analytics", "—", "✓"]]},
    {"type": "faq", "items": [
        ("How is the price calculated?", "You pay a monthly price for each employee in HR Connect. Invoices are sent monthly, plus any taxes that apply, such as VAT or sales tax."),
        ("Can I change plans later?", "Yes. Modules can be switched on for your company at any time."),
        ("Is there a setup fee?", "Contact us and we'll give you a quote based on your company size and needs."),
        ("Does HR Connect handle payroll taxes?", "Not yet. HR Connect runs payroll calculations, approvals and payslips from the earnings and deductions you set up. Tax calculations and filings are handled outside HR Connect, for example by your accountant or tax provider."),
        ("Which currencies do you invoice in?", "Ask us when you request a quote. We'll agree the billing currency with you.")]},
    CTA]}

# ---------------------------------------------------------------- demo / contact
DEMO_FIELDS = [("name", "Full name", "text"), ("email", "Work email", "email"), ("company", "Company", "text"), ("phone", "Phone (optional)", "tel"),
               ("country", "Country", "text"),
               ("size", "Number of employees", "select", ["1–25", "26–100", "101–250", "251–1,000", "1,000+"]),
               ("interest", "What would you like to see? (optional)", "textarea")]
PAGES["book-a-demo"] = {"title": "Book a Demo", "desc": "Book a 30-minute demo of HR Connect, tailored to your company.",
  "blocks": [
    {"type": "hero", "eyebrow": "Book a demo", "title": "See HR Connect **in 30 minutes**", "lead": "Tell us a little about your company and we'll show you the modules that matter to you."},
    {"type": "form", "subject": "Demo request", "button": "Request a demo", "fields": DEMO_FIELDS,
     "aside": '<h2>What to expect</h2><ul class="checks">' + "".join(f'<li><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg><span>{t}</span></li>' for t in
              ["A walkthrough of payroll, leave and expenses, set up like your company", "Answers to your questions about pricing and setup", "No obligation and no hard sell"]) + "</ul>"}]}
PAGES["contact"] = {"title": "Contact Us", "desc": "Contact the HR Connect team about sales, support or partnerships.",
  "blocks": [
    {"type": "hero", "eyebrow": "Contact", "title": "Talk to the **HR Connect team**", "lead": "Questions about pricing, setup or partnerships? Send us a message and we'll reply within one working day."},
    {"type": "form", "subject": "Website enquiry", "button": "Send message",
     "fields": [("name", "Full name", "text"), ("email", "Email", "email"), ("company", "Company (optional)", "text"),
                ("topic", "Topic", "select", ["Sales & pricing", "Product support", "Partnerships", "Other"]), ("message", "Message", "textarea")],
     "aside": f'<h2>Other ways to reach us</h2><p class="lead" style="margin-top:14px;color:var(--muted)">Email us at <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>'
              '<p style="margin-top:14px;color:var(--muted)">Already a customer? Use <b>Support</b> inside HR Connect to raise a ticket, or see the <a href="/help/">Help Center</a>.</p>'}]}

# ---------------------------------------------------------------- about / security
PAGES["about"] = {"title": "About Us", "desc": "HR Connect builds HR and payroll software for growing companies.",
  "blocks": [
    {"type": "hero", "eyebrow": "About HR Connect", "title": "HR software built **for growing teams**",
     "lead": "We're building one connected place for HR, payroll and expenses, so growing companies can look after their people without drowning in admin."},
    {"type": "features", "title": "What we believe", "items": [
        ("layers", "Connected beats complicated", "HR data should live in one place and flow where it's needed."),
        ("user", "Employees deserve self-service", "Nobody should need to email HR for a payslip."),
        ("sparkles", "AI should do the boring work", "Reading receipts and answering policy questions, so people can focus on people."),
    ]},
    {"type": "prose", "alt": True, "html": "<h2>Our story</h2><p>HR Connect started with a simple observation: growing companies were running payroll in spreadsheets, approving time off by email and tracking employee loans in a notebook. Enterprise HR suites were too big and too expensive, and simple tools didn't connect to payroll.</p><p>So we built HR Connect: a modern, connected HR platform for small and mid-sized companies, wherever they operate.</p>",
     "notice": "Placeholder: add the company's founding story, team and office locations before publishing."},
    CTA]}
PAGES["security"] = {"title": "Security & Privacy", "desc": "How HR Connect keeps your company's HR and payroll data separate, secure and under your control.",
  "blocks": [
    {"type": "hero", "eyebrow": "Security & privacy", "title": "Your people data, **protected**",
     "lead": "HR and payroll data is some of the most sensitive data a company holds. Here's how HR Connect protects it."},
    {"type": "features", "title": "How we protect your data", "items": [
        ("building", "Your data stays yours", "Every company's data is kept separate. Each request is tied to your company through your secure sign-in, so one company can never see another's records."),
        ("shield", "Role-based permissions", "Control access per module, per screen and per action, such as view, manage, approve and delete. Override permissions for individual users."),
        ("lock", "Secure sign-in", "Passwords are hashed, never stored in plain text. Sessions use short-lived tokens that refresh securely."),
        ("file", "Secure file storage", "Documents and receipts are stored in secure cloud storage and shared only through short-lived, signed links."),
        ("list", "Audit trail", "Payroll runs and approvals keep a history of who did what and when."),
        ("layers", "Only the modules you use", "Modules can be switched on or off for your company, so data is only collected where you need it."),
    ]},
    {"type": "faq", "alt": True, "items": [
        ("Where is my data stored?", "HR Connect runs on established cloud infrastructure. Contact us for details of hosting regions."),
        ("Is AI trained on my data?", "Your policies and receipts are used to answer your questions and fill in your forms. See our [privacy policy](/privacy/) for details of the AI providers we use."),
        ("How do I report a security issue?", f"Email [{CONTACT_EMAIL}](mailto:{CONTACT_EMAIL}) and we'll respond promptly.")]},
    CTA]}

# ---------------------------------------------------------------- solutions
def solution(slug, h1, lead, pains, mods, mk):
    name = next(n for s, n, d, ic in SOLUTIONS if s == slug)
    return {"title": f"HR Connect {name}", "desc": lead,
      "blocks": [
        {"type": "hero", "crumbs": [("Home", "/"), (name, f"/solutions/{slug}/")], "eyebrow": name, "title": h1, "lead": lead,
         "ctas": [("Book a demo", "/book-a-demo/"), ("See pricing", "/pricing/")], "mock": mk},
        {"type": "table", "title": "From problem to solved", "head": ["The problem", "How HR Connect helps"], "rows": [[a, "✓ " + b] for a, b in pains]},
        related(mods, "The modules you'll use most"), CTA]}

PAGES["solutions/hr-teams"] = solution("hr-teams", "Spend less time on admin, **more time on people**",
    "HR Connect gives HR teams one place for employee records, leave, offboarding and policies, and lets employees serve themselves.",
    [("Employee data spread across spreadsheets", "One directory with profiles, documents and history"),
     ("Chasing time-off approvals by email", "Requests and approvals tracked, balances updated automatically"),
     ("Exits that miss steps", "Offboarding with approval, exit checklist and final settlement"),
     ("The same questions every week", "Self-service and an AI assistant that answers from your policies"),
     ("Missed birthdays and anniversaries", "Cards sent automatically")],
    ["core-hr", "leave", "offboarding", "self-service", "policies", "celebrations"], M_HR)
PAGES["solutions/finance-teams"] = solution("finance-teams", "Payroll and spend **you can sign off with confidence**",
    "HR Connect gives finance teams approved payroll runs, expense control and loan tracking in one place, with exports for the bank.",
    [("Payroll built in fragile spreadsheets", "Payroll calculated from employee data, with an approval flow"),
     ("Expenses and reimbursements paid separately", "Approved claims reimbursed through payroll"),
     ("Loans tracked by hand", "Installments deducted from payroll automatically"),
     ("Typing up bank payment files", "Bank payment file export in CSV or XLSX"),
     ("No visibility of people costs", "Payroll and expense analytics")],
    ["payroll", "expenses", "loans", "reports", "offboarding"], M_PAYROLL)
PAGES["solutions/business-owners"] = solution("business-owners", "Know your people costs **without asking for a report**",
    "HR Connect gives owners and executives a clear view of headcount, payroll and approvals, and the confidence that HR runs properly.",
    [("No clear view of headcount and payroll cost", "Dashboards with headcount, payroll and expense figures"),
     ("Approvals happening outside any system", "Every payroll run, claim and loan approved in HR Connect"),
     ("Worry about who can see salaries", "Role-based permissions down to each action"),
     ("Enterprise HR suites that are too big and too expensive", "One platform priced per employee, with the modules you need")],
    ["reports", "payroll", "expenses"], M_REPORTS)
PAGES["solutions/employees"] = solution("employees", "Everything you need from HR, **in one place**",
    "With HR Connect, employees can see payslips, request leave, claim expenses and get answers without waiting on HR. Managers approve from one list.",
    [("Waiting for HR to send a payslip", "Download any payslip, any time"),
     ("Not knowing your leave balance", "Live balances before you request"),
     ("Paper expense forms", "Snap a receipt and AI fills in the claim"),
     ("Hunting through policy documents", "Ask the AI assistant"),
     ("Approvals lost in email", "Requests tracked from start to finish")],
    ["self-service", "leave", "expenses", "ai"], M_SELF)

# ---------------------------------------------------------------- tools
TOOL_DISCLAIMER = "This calculator gives an estimate for guidance only. It is not legal advice. Check the current law or a qualified adviser before making a payment."
PAGES["tools/leave-balance-calculator"] = {"title": "Leave Balance Calculator",
  "desc": "Free calculator to work out how much annual leave an employee has earned and has left.",
  "blocks": [
    {"type": "hero", "crumbs": [("Tools", "/resources/"), ("Leave Balance Calculator", "/tools/leave-balance-calculator/")], "eyebrow": "Free tool",
     "title": "Leave balance **calculator**", "lead": "Work out how much annual leave an employee has earned so far this year and how much they have left."},
    {"type": "calc", "kind": "leave", "result_label": "Leave balance today", "disclaimer": "Leave is assumed to be earned evenly across a 365-day leave year. Your company policy or local law may differ.", "fields": [
        ("entitlement", "Annual leave entitlement (days per year)", "number", {"min": "0", "step": "0.5", "value": "20"}),
        ("start", "Start of leave year (or joining date if later)", "date", {"value": "2026-01-01"}),
        ("asof", "Calculate balance on", "date", {"today": True}),
        ("carried", "Days carried over from last year", "number", {"min": "0", "step": "0.5", "value": "0"}),
        ("taken", "Days already taken this year", "number", {"min": "0", "step": "0.5", "value": "0"})]},
    {"type": "prose", "alt": True, "html": "<h2>How leave is earned</h2><p>Many companies let employees earn annual leave evenly through the year. For example, an employee with 20 days a year earns about 1.67 days each month.</p>"
     "<p>In HR Connect you set the entitlement, weekend days and carry-over rules once, and balances update automatically as leave is approved. <a href=\"/product/leave/\">See leave management</a>.</p>"},
    CTA]}

# ---------------------------------------------------------------- resources
PAGES["resources"] = {"title": "HR Resources", "desc": "Free HR and payroll resources from HR Connect: calculators, an HR glossary, articles and help guides.",
  "blocks": [
    {"type": "hero", "eyebrow": "Resources", "title": "Free HR and payroll **resources**", "lead": "Calculators, guides and definitions to help you run HR and payroll with confidence."},
    {"type": "cards", "title": "Free tools", "items": [(ic, n, d + ".", f"/tools/{s}/") for s, n, d, ic in TOOLS], "cols": 3},
    {"type": "cards", "alt": True, "title": "Learn", "items": [
        ("list", "HR Glossary", "Plain-language definitions of common HR and payroll terms.", "/glossary/"),
        ("file", "Blog", "Articles on HR, payroll and employment law.", "/blog/"),
        ("message", "Help Center", "Step-by-step guides to using HR Connect.", "/help/")], "cols": 3},
    CTA]}
UPCOMING = [("How to write a leave policy employees understand", "Leave"), ("Running payroll across several countries and currencies", "Payroll"),
            ("Final pay: what to check before an employee leaves", "Offboarding"), ("Employee loans: a fair policy template", "Policies"),
            ("Expense policies that don't slow people down", "Expenses"), ("An offboarding checklist for growing companies", "Offboarding")]
PAGES["blog"] = {"title": "Blog", "desc": "HR, payroll and employment-law articles from the HR Connect team.",
  "blocks": [
    {"type": "hero", "eyebrow": "Blog", "title": "HR and payroll, **explained**", "lead": "Practical articles on payroll, leave, expenses and employment law for growing companies. Our first articles are on the way."},
    {"type": "cards", "title": "Coming soon", "items": [(None, t, f"{c} article.", None, "Coming soon") for t, c in UPCOMING], "cols": 3},
    {"type": "cards", "alt": True, "title": "Useful right now", "items": [(ic, n, d + ".", f"/tools/{s}/") for s, n, d, ic in TOOLS], "cols": 3},
    CTA]}

GLOSSARY = [
    ("Base salary", "The fixed part of an employee's pay, before bonuses, commission and deductions."),
    ("Allowance", "An amount paid on top of base salary for a specific purpose, such as a phone, home-office or commuter stipend."),
    ("Gross pay", "Total earnings for a pay period before any deductions."),
    ("Net pay", "What the employee actually receives after deductions. Also called take-home pay."),
    ("Pay period", "The span of time an employee is paid for in one paycheck, such as a week, two weeks or a month."),
    ("Payroll run", "One month's payroll for a group of employees: calculated, approved and then paid."),
    ("Payslip", "A statement for the employee showing earnings, deductions and net pay for a pay period. Also called a pay stub."),
    ("Bank advice", "A file listing each employee's bank details and net pay, used to pay employees through the bank."),
    ("Pro-rating", "Paying an employee for part of a pay period, for example when they start or leave mid-month."),
    ("One-off payment", "An earning or deduction that applies to a single payroll run, such as a bonus or a reimbursement."),
    ("Multi-currency payroll", "Running payroll for employees paid in different currencies, usually with a separate payroll setup for each currency or country."),
    ("Final settlement", "The last payment to a leaving employee, covering pay to the last day and any other amounts due or owed. Also called final pay or a final paycheck. Many countries set deadlines for paying it."),
    ("Notice period", "The time between an employee or employer giving notice and the last working day."),
    ("Separation", "The end of an employee's employment, for example through resignation, termination, retirement or end of contract."),
    ("Exit checklist", "The list of tasks to complete before an employee leaves, such as returning equipment and handing over work."),
    ("Annual leave", "Paid time off employees earn each year. Also called vacation or paid time off (PTO)."),
    ("Leave accrual", "Earning leave gradually, for example a set number of days for each month worked. Try our [leave balance calculator](/tools/leave-balance-calculator/)."),
    ("Carry-over", "Moving unused leave from one leave year into the next, usually up to a limit. Also called carry-forward or rollover."),
    ("Leave balance", "The leave an employee has left: what they've been allocated plus carry-over, minus what they've taken."),
    ("Cash advance", "Money given to an employee before they spend it, for example for a business trip, and later settled against expense claims."),
    ("Expense claim", "A request by an employee to be paid back for money they spent on company business."),
    ("Employee loan", "Money lent by the employer to an employee and repaid in installments, usually through payroll deductions."),
    ("Installment", "The fixed amount repaid each month on a loan."),
    ("Employee self-service (ESS)", "A portal where employees view their own information and make requests, such as time off or expense claims."),
    ("Org chart", "A diagram showing who reports to whom in a company."),
    ("Headcount", "The number of employees in a company or team at a point in time."),
    ("Role-based access", "Controlling what each user can see and do according to their role, such as employee, HR or admin."),
]
PAGES["glossary"] = {"title": "HR Glossary", "desc": "Plain-language definitions of HR and payroll terms, from base salary to final settlement.",
  "blocks": [
    {"type": "hero", "eyebrow": "HR Glossary", "title": "HR and payroll terms, **in plain language**", "lead": f"{len(GLOSSARY)} terms every HR and payroll team should know."},
    {"type": "glossary", "terms": GLOSSARY},
    CTA]}

HELP = [
    ("Getting started", "layers", [
        ("What are the Me and People workspaces?", ["**Me** is your own workspace: your profile, payslips, leave, loans, expenses and policies.", "**People** is where HR and admins manage the company. You only see the menus your role has permission for."]),
        ("I didn't get my invite email. What should I do?", "Ask your HR team to resend your invite from the employee directory. They can also send you new login details."),
        ("I forgot my password", "On the login page choose **Forgot password**. We'll email you a code to reset it.")]),
    ("Employees", "users", [
        ("How do I add an employee?", "Go to **People → Employees → Directory** and choose **Add employee**. The wizard collects personal, job, pay and bank details, then sends an invite."),
        ("How do I update my own details?", "Go to **Me → My Profile**. What you can edit depends on your role's permissions."),
        ("Where is the org chart?", "Open **Org Chart** from the Employees menu. It's built from each employee's manager.")]),
    ("Leave", "calendar", [
        ("How do I request leave?", "Go to **Me → My Leave**, choose **New request**, pick the type and dates and submit. Business days are counted using your weekend days."),
        ("Can I edit or cancel a request?", "Yes, while it's still pending. Approved requests can't be deleted."),
        ("How do I approve leave?", "Go to **People → Leave Management**, open a pending request and approve, or reject with a reason."),
        ("Where can I see balances?", "Switch to the **Balances** view to see allocated, used, carried-forward and remaining days.")]),
    ("Payroll", "banknote", [
        ("How do I create a payroll setup?", "Go to **People → Payroll → Setup** and choose **New Setup**. Enter name, country and currency, then components, leave rules and final settlement. Once a setup is in use, only its name can change."),
        ("How do I run payroll?", ["Go to **Payroll Runs**, choose **New Payroll Run**, pick the setup and month. The run is calculated straight away.", "Add any one-off earnings or deductions, submit for approval, then mark it paid once approved. Payslips are issued when the run is paid."]),
        ("Why can't I submit a run?", "A run can't be submitted if it has no employees, duplicate lines, zero gross pay or negative net pay."),
        ("How do I get the bank file?", "Open the run and export the **bank advice** as CSV or XLSX. Approvers can see it while the run is pending."),
        ("Where are my payslips?", "Go to **Me → Payslips**, open the month and choose **Download** to save it as PDF.")]),
    ("Loans, expenses & advances", "receipt", [
        ("How do I submit an expense claim?", "Go to **Me → Expenses**, add a claim and upload the receipt. Use **Auto scan** to let AI fill in the details, check them and submit."),
        ("When will I be reimbursed?", "Approved claims are paid in the next payroll run."),
        ("How do I request an advance or a loan?", "Use **Me → Advances** or **Me → Loans**. Once approved, the money is paid through payroll and loan installments are deducted each month.")]),
    ("Offboarding", "logout", [
        ("How do I start a separation?", "From the directory or **Separations**, choose **Initiate separation** and enter type, reason and last working day. Reassign any direct reports first."),
        ("What are the steps?", "Request, approval, exit checklist, final settlement, then exited. The employee is marked exited when the payroll run for their last month is paid.")]),
    ("Settings & permissions", "shield", [
        ("How do I control what people can see?", "Go to **Settings → User Permissions**. Give each role permissions per module and action, and override them for individual users if needed."),
        ("How do I publish a policy?", "Go to **Settings → Policies** and upload the document. Employees see it under **My Policies** and can ask the AI assistant about it.")]),
]
PAGES["help"] = {"title": "Help Center", "desc": "Step-by-step help for using HR Connect: employees, leave, payroll, expenses, offboarding and settings.",
  "blocks": [
    {"type": "hero", "eyebrow": "Help Center", "title": "How can we **help**?", "lead": "Quick answers to common questions about using HR Connect. Inside the app, the AI assistant can help too."},
    {"type": "help", "groups": HELP},
    {"type": "cta", "title": "Still need help?", "text": "Raise a ticket from Support inside HR Connect, or contact us.", "ctas": [("Contact us", "/contact/"), ("Log in", APP_URL)]}]}

# ---------------------------------------------------------------- company
PAGES["careers"] = {"title": "Careers", "desc": "Work at HR Connect and help build HR software for growing companies.",
  "blocks": [
    {"type": "hero", "eyebrow": "Careers", "title": "Help us build **better HR for growing teams**",
     "lead": "We're a small team building HR software that companies actually enjoy using."},
    {"type": "features", "title": "Why join us", "items": [
        ("sparkles", "Real impact", "Your work reaches HR teams and employees every day."),
        ("layers", "Modern stack", "TypeScript, React, NestJS, PostgreSQL and AI."),
        ("users", "Small team", "Ownership from day one."),
    ]},
    {"type": "prose", "alt": True, "html": f"<h2>Open roles</h2><p>We don't have open roles listed right now. If you'd like to work with us, send your CV to <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a> and tell us what you'd like to work on.</p>"}]}
PAGES["partners"] = {"title": "Partners & Referral Program", "desc": "Partner with HR Connect as a reseller or refer companies and earn rewards.",
  "blocks": [
    {"type": "hero", "eyebrow": "Partners", "title": "Grow with **HR Connect**", "lead": "HR consultants, accountants and resellers: partner with us to bring modern HR and payroll to your clients."},
    {"type": "features", "title": "Ways to partner", "items": [
        ("briefcase", "Resellers", "Sell and set up HR Connect for your clients."),
        ("users", "Referral partners", "Introduce companies to HR Connect and earn a reward for each new customer."),
        ("building", "HR & accounting firms", "Run HR and payroll for your clients on one platform."),
    ]},
    {"type": "form", "alt": True, "subject": "Partner enquiry", "button": "Apply to partner",
     "fields": [("name", "Full name", "text"), ("email", "Work email", "email"), ("company", "Company", "text"),
                ("type", "Partnership type", "select", ["Reseller", "Referral partner", "HR or accounting firm", "Other"]),
                ("country", "Country", "text"), ("about", "Tell us about your clients (optional)", "textarea")],
     "aside": "<h2>Apply in two minutes</h2><p class=\"lead\" style=\"margin-top:14px;color:var(--muted)\">Tell us about your business and we'll get in touch to discuss terms.</p>"}]}

# ---------------------------------------------------------------- legal (drafts)
LEGAL_NOTE = "Draft for review: have this page checked by a legal adviser and completed with your company's legal name and address before publishing."
PAGES["privacy"] = {"title": "Privacy Policy", "desc": "How HR Connect collects, uses and protects personal data.",
  "blocks": [
    {"type": "hero", "eyebrow": "Legal", "title": "Privacy policy", "lead": "How we collect, use and protect personal data."},
    {"type": "prose", "notice": LEGAL_NOTE, "html": f"""
<h2>Who we are</h2><p>HR Connect provides HR, payroll and expense software to businesses ("customers"). This policy explains how we handle personal data on this website and in the HR Connect app.</p>
<h2>Our role</h2><p>For employee data that customers put into HR Connect, the customer is the controller and we process it on their behalf. For data collected on this website, such as demo requests, we are the controller.</p>
<h2>Data we process</h2><ul><li><b>Website visitors:</b> details you send us through forms, such as name, work email, company and message.</li><li><b>App users:</b> account details such as name, email and role, plus the HR data customers add, such as job details, compensation, bank details, documents, leave, loans and expense receipts.</li></ul>
<h2>How we use it</h2><ul><li>To provide and support the HR Connect service.</li><li>To respond to enquiries and demo requests.</li><li>To send service emails, such as invites, password resets, notifications and greeting cards set up by the customer.</li><li>To keep the service secure.</li></ul>
<h2>AI features</h2><p>When AI features are used, the relevant content (such as a receipt image or a question about a policy) is sent to our AI service providers to produce the answer. We use AI to help users, not to make decisions about employees.</p>
<h2>Service providers</h2><p>We use trusted providers to run the service, including cloud hosting and file storage, email delivery and AI model providers. They process data only on our instructions.</p>
<h2>Security</h2><p>We separate each customer's data, control access with role-based permissions, hash passwords and store files securely. See <a href="/security/">Security &amp; Privacy</a>.</p>
<h2>Retention</h2><p>We keep customer data for as long as the customer's account is active and as required by law, then delete it.</p>
<h2>Your rights</h2><p>You may have rights to access, correct or delete your personal data. If you are an employee of one of our customers, please contact your employer first. You can also contact us at <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>
<h2>Changes</h2><p>We may update this policy and will post the new version on this page.</p>"""}]}
PAGES["terms"] = {"title": "Terms of Service", "desc": "The terms that apply to using HR Connect.",
  "blocks": [
    {"type": "hero", "eyebrow": "Legal", "title": "Terms of service", "lead": "The terms that apply when you use HR Connect."},
    {"type": "prose", "notice": LEGAL_NOTE, "html": f"""
<h2>1. The service</h2><p>HR Connect is an online HR, payroll and expense management service provided on a subscription basis.</p>
<h2>2. Accounts</h2><p>The customer is responsible for the users it invites, the roles and permissions it gives them, and keeping login details secure.</p>
<h2>3. Fees and billing</h2><p>Fees are charged per employee per month for the plan and modules the customer subscribes to. Invoices are issued monthly, plus applicable taxes.</p>
<h2>4. Customer data</h2><p>The customer owns the data it puts into HR Connect and is responsible for having the right to process it. We process it to provide the service, as described in our <a href="/privacy/">Privacy Policy</a>.</p>
<h2>5. Payroll and calculations</h2><p>HR Connect calculates payroll from the data and rules the customer sets up. The customer is responsible for reviewing and approving payroll and for meeting its legal obligations, including payroll tax withholding and filings, and salary payments.</p>
<h2>6. Acceptable use</h2><p>Don't misuse the service, try to access other customers' data, or use it for anything unlawful.</p>
<h2>7. Availability and support</h2><p>We aim to keep HR Connect available and provide support through in-app tickets and email.</p>
<h2>8. Liability</h2><p>To the extent permitted by law, our liability is limited to the fees paid in the 12 months before the claim.</p>
<h2>9. Termination</h2><p>Either party may end the subscription as set out in the order. On request we will provide an export of the customer's data.</p>
<h2>10. Contact</h2><p>Questions about these terms: <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a>.</p>"""}]}
PAGES["cookies"] = {"title": "Cookie Policy", "desc": "How HR Connect uses cookies on this website and in the app.",
  "blocks": [
    {"type": "hero", "eyebrow": "Legal", "title": "Cookie policy", "lead": "How we use cookies and similar technology."},
    {"type": "prose", "notice": LEGAL_NOTE, "html": f"""
<h2>What are cookies?</h2><p>Cookies are small files stored by your browser that help websites work and remember information.</p>
<h2>Cookies on this website</h2><p>This website does not set advertising or tracking cookies. Fonts are loaded from Google Fonts, which may receive your IP address.</p>
<h2>Cookies in the HR Connect app</h2><p>The app uses essential storage to keep you signed in securely. These are needed for the service to work and can't be switched off.</p>
<h2>Managing cookies</h2><p>You can block or delete cookies in your browser settings. Blocking essential cookies will stop you signing in to the app.</p>
<h2>Contact</h2><p><a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></p>"""}]}

# The solutions/tools hub URLs used in breadcrumbs point at the first child;
# the pages are exactly the keys of PAGES.
NOT_FOUND = {"title": "Page not found", "desc": "This page could not be found.",
  "blocks": [{"type": "hero", "eyebrow": "404", "title": "We couldn't find **that page**", "lead": "It may have moved. Try the home page or the menu above.",
              "ctas": [("Go to the home page", "/"), ("Contact us", "/contact/")]}]}
