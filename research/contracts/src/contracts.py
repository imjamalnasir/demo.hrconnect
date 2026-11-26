"""Text of the HRConnect.AI sample contracts.

One source for the PDF and the DOCX. build_contracts.py turns it into both.

Each contract is a dict:
  slug, file      output names
  group           "client" (HR Connect and a customer) or "people" (a company and an employee or contractor)
  title, purpose  shown on the document and on research/contracts.html
  parties         paragraphs before clause 1
  clauses         list of (heading, items); items are numbered 1.1, 1.2 ... unless the contract sets numbered=False
  schedules       list of (heading, items), printed after the signatures
  signatures      party labels for the signature block

Item types inside a clause or schedule:
  "text"               a paragraph (numbered in clauses)
  "- text"             a bullet, never numbered
  "> text"             a plain paragraph, never numbered
  {"table": rows}      a table; the first row is the header
  {"kv": rows}         a two-column label / value table with no header

Anything in [square brackets] is a placeholder to fill in; both formats highlight it.
Keep the text country-neutral (see README): no country-specific laws, holidays or tax terms.
"""

HRC = "[HR Connect legal entity name]"

def company_party(n, name, label, kind="a company"):
    return (f"({n}) {name}, {kind} registered in [country] under number [company number], "
            f"whose registered office is at [registered address] (“{label}”)")

GENERAL_LAW = ("This Agreement is governed by the laws of [governing law jurisdiction]. The courts of "
               "[jurisdiction for disputes] have exclusive jurisdiction over any dispute arising out of or in connection with it, "
               "unless the parties agree in writing to resolve a dispute by [mediation / arbitration under named rules].")

CONTRACTS = [
# ---------------------------------------------------------------- client contracts
{
    "slug": "master-subscription-agreement",
    "file": "HRConnect-AI-Master-Subscription-Agreement",
    "group": "client",
    "title": "Master Subscription Agreement",
    "short": "MSA",
    "purpose": "The main terms for every customer: the service, fees, customer data, liability and termination. Each Order Form sits under it.",
    "parties": [
        "This Master Subscription Agreement (the “Agreement”) is made on [date] between:",
        company_party(1, HRC, "HR Connect"),
        company_party(2, "[Customer legal name]", "Customer"),
        "Each a “party” and together the “parties”. The parties agree as follows.",
    ],
    "clauses": [
        ("Definitions", [
            "In this Agreement:",
            "- “Services” means the HRConnect.AI cloud HR and payroll software described in an Order Form, including updates, and related support.",
            "- “Order Form” means an ordering document signed by both parties that refers to this Agreement.",
            "- “Users” means the Customer's employees, contractors and administrators who are given access to the Services.",
            "- “Customer Data” means all data, including personal data, that the Customer or its Users enter into or upload to the Services.",
            "- “Documentation” means HR Connect's then-current user guides and help articles for the Services.",
            "- “Subscription Term” means the period stated in the Order Form, including any renewals.",
        ]),
        ("The Services", [
            "HR Connect will make the Services available to the Customer during the Subscription Term in line with this Agreement, the Order Form and the Documentation.",
            "The Customer may allow its Users to access the Services for its internal business purposes. The Customer is responsible for its Users' acts and omissions.",
            "HR Connect may update the Services from time to time. It will not make an update that materially reduces the overall functionality of the Services the Customer has subscribed to during the Subscription Term.",
            "Support and service levels are set out in the Service Level Agreement, if one is attached to the Order Form.",
        ]),
        ("Customer responsibilities", [
            "The Customer will: (a) keep the data it enters accurate and up to date; (b) keep login details secure and tell HR Connect promptly of any unauthorised access; and (c) use the Services only in line with applicable law and the Documentation.",
            "The Customer will not: (a) resell, sublicense or make the Services available to third parties; (b) copy, modify, reverse engineer or attempt to access the source code of the Services; (c) use the Services to store or send unlawful or malicious content; or (d) interfere with the security or performance of the Services.",
            "The Services help the Customer run HR and payroll administration. They do not provide legal, tax, financial or employment advice. The Customer remains responsible for its employment decisions, for checking payroll results before approving them, and for making salary payments and tax filings. The Services produce a bank payment file; they do not send payments.",
        ]),
        ("Fees and payment", [
            "The Customer will pay the fees set out in the Order Form. Fees are priced per employee per month and invoiced [monthly / annually] in advance, unless the Order Form says otherwise.",
            "Invoices are due within [30] days of the invoice date, in the currency stated in the Order Form.",
            "Fees exclude taxes. The Customer will pay any applicable sales, value-added or similar taxes, other than taxes on HR Connect's income.",
            "If an undisputed invoice is more than [15] days overdue, HR Connect may, after giving at least [10] days' written notice, suspend the Services until payment is received.",
            "HR Connect may change its fees with effect from the start of a renewal term by giving at least [60] days' written notice before that renewal.",
        ]),
        ("Customer Data", [
            "The Customer owns all Customer Data. The Customer grants HR Connect a limited right to process Customer Data only as needed to provide, secure and support the Services and as otherwise set out in this Agreement.",
            "Where HR Connect processes personal data on the Customer's behalf, the Data Processing Agreement between the parties applies and forms part of this Agreement.",
            "HR Connect will keep appropriate technical and organisational measures in place to protect Customer Data, as described in the Data Processing Agreement.",
            "The Customer can export its Customer Data from the Services at any time during the Subscription Term.",
            "After this Agreement ends, HR Connect will keep Customer Data available for export for [30] days and will then delete it within [90] days, unless law requires HR Connect to keep it.",
        ]),
        ("AI features", [
            "The Services include AI features, such as an assistant that answers questions and drafts content. AI output may be incomplete or inaccurate. The Customer is responsible for reviewing AI output before relying on it or acting on it.",
            "AI features only use the data that the requesting User is allowed to see under the Customer's permission settings.",
            "HR Connect will not use Customer Data to train AI models that are made available to other customers [unless the Customer agrees in writing].",
        ]),
        ("Confidentiality", [
            "“Confidential Information” means information disclosed by one party to the other that is marked as confidential or that a reasonable person would understand to be confidential. Customer Data is the Customer's Confidential Information.",
            "Each party will use the other's Confidential Information only to perform this Agreement, will protect it with at least reasonable care, and will disclose it only to its employees, contractors and advisers who need to know it and are bound by similar duties.",
            "These duties do not apply to information that is or becomes public through no fault of the receiving party, was already known to it, is received lawfully from a third party, or is independently developed. A party may disclose Confidential Information where required by law, after giving the other party notice where lawful.",
        ]),
        ("Intellectual property", [
            "HR Connect and its licensors own all rights in the Services, the Documentation and any improvements to them. No rights are granted to the Customer other than those expressly set out in this Agreement.",
            "If the Customer gives feedback or suggestions about the Services, HR Connect may use them without restriction or payment.",
        ]),
        ("Warranties", [
            "Each party warrants that it has the authority to enter into this Agreement.",
            "HR Connect warrants that the Services will perform materially in line with the Documentation. If they do not, the Customer's remedy is for HR Connect to use reasonable efforts to correct the failure, or, if it cannot do so within a reasonable time, for either party to terminate the affected Order Form and for HR Connect to refund any prepaid fees for the rest of the Subscription Term.",
            "Except as stated in this Agreement, the Services are provided “as is” and HR Connect gives no other warranties, to the extent permitted by law.",
        ]),
        ("Indemnities", [
            "HR Connect will defend the Customer against any third-party claim that the Services infringe that third party's intellectual property rights, and will pay any damages finally awarded or agreed in settlement.",
            "The Customer will defend HR Connect against any third-party claim arising from Customer Data or from the Customer's use of the Services in breach of this Agreement or the law, and will pay any damages finally awarded or agreed in settlement.",
            "The indemnified party must notify the other party promptly of the claim, let it control the defence and settlement, and give reasonable help at its cost.",
        ]),
        ("Limitation of liability", [
            "Neither party is liable for any indirect or consequential loss, or for loss of profits, revenue, goodwill or data, however caused.",
            "Each party's total liability under or in connection with this Agreement in any 12-month period is limited to the fees paid and payable by the Customer under this Agreement in the 12 months before the event giving rise to the claim.",
            "Nothing in this Agreement limits liability for fraud, for death or personal injury caused by negligence, for the Customer's payment obligations, for the indemnities in clause 10, or for anything else that cannot be limited by law.",
        ]),
        ("Term and termination", [
            "This Agreement starts on the date above and continues while any Order Form is in force.",
            "Each Order Form renews automatically for successive periods equal to its initial term, unless either party gives at least [30] days' written notice of non-renewal before the end of the current term.",
            "Either party may terminate this Agreement or an Order Form by written notice if the other party: (a) commits a material breach that is not remedied within [30] days of written notice; or (b) becomes insolvent or ceases to do business.",
            "When this Agreement ends: the Customer's access to the Services ends, the Customer pays any fees due up to the end date, and clause 5.5 (data export and deletion) applies. Clauses that by their nature should survive termination will survive.",
        ]),
        ("General", [
            GENERAL_LAW,
            "Notices must be in writing and sent to the addresses in the Order Form, or to another address a party notifies. Notices by email are valid when sent to the contact named in the Order Form.",
            "Neither party may assign this Agreement without the other's written consent, which will not be unreasonably withheld, except to a successor in a merger or sale of all or substantially all of its business.",
            "Neither party is liable for a delay or failure caused by events beyond its reasonable control.",
            "This Agreement, the Order Forms and the Data Processing Agreement are the entire agreement between the parties on their subject. If they conflict, the order of precedence is: (a) the Order Form; (b) the Data Processing Agreement; (c) this Agreement; (d) the Documentation.",
            "Changes to this Agreement must be in writing and signed by both parties. This Agreement may be signed electronically and in counterparts.",
        ]),
    ],
    "signatures": ["HR Connect", "Customer"],
},
{
    "slug": "order-form",
    "file": "HRConnect-AI-Order-Form",
    "group": "client",
    "title": "Order Form",
    "short": "Order",
    "purpose": "What the customer is buying: modules, employee count, fees, term and start date. Signed for each new subscription or upgrade.",
    "numbered": False,
    "parties": [
        "Order Form number: [OF-0001]  ·  Date: [date]",
        "This Order Form is made under the Master Subscription Agreement between [HR Connect legal entity name] (“HR Connect”) and the Customer named below, dated [date] (the “Agreement”). Terms defined in the Agreement have the same meaning here.",
    ],
    "clauses": [
        ("Customer details", [
            {"kv": [
                ("Customer legal name", "[Customer legal name]"),
                ("Registered address", "[address]"),
                ("Company number", "[company number]"),
                ("Tax registration number", "[if applicable]"),
                ("Billing contact", "[name, email]"),
                ("Notices contact", "[name, email]"),
                ("Account owner (admin)", "[name, email]"),
            ]},
        ]),
        ("Subscription", [
            {"kv": [
                ("Plan", "☐ Basic   ☐ Premium"),
                ("Modules included", "Basic: core HR, payroll, leave, loans, offboarding, employee self-service, company policies, AI assistant, celebrations, reports and permissions. Premium adds expenses and advances, AI receipt scanning and expense analytics."),
                ("Number of employees", "[number] active employee records"),
                ("Legal entities and locations", "[number of entities / locations]"),
                ("Start date", "[date]"),
                ("Initial term", "[12] months from the start date"),
                ("Renewal", "Renews automatically for the same period unless either party gives [30] days' notice"),
                ("Service Level Agreement", "☐ Standard   ☐ Attached"),
            ]},
        ]),
        ("Fees", [
            {"table": [
                ("Item", "Quantity", "Unit price", "Billing", "Total"),
                ("Platform subscription", "[number] employees", "$[0.00] per employee per month", "[Monthly in advance]", "$[0.00]"),
                ("Onboarding and data migration", "1", "$[0.00]", "One-off, on signature", "$[0.00]"),
                ("Training sessions", "[number]", "$[0.00]", "One-off", "$[0.00]"),
                ("Discount", "", "", "", "−$[0.00]"),
                ("Total for the initial term", "", "", "", "$[0.00]"),
            ]},
            "> Additional employees above the number in this Order Form are charged at the same unit price, pro rata, and invoiced [monthly / quarterly] in arrears.",
            "> Payment terms: invoices are due within [30] days. Currency: [USD]. Fees exclude taxes.",
        ]),
        ("Special terms", [
            "> [Any agreed changes to the Agreement, such as a price lock, a pilot period or custom onboarding. Write “None” if there are none.]",
        ]),
    ],
    "signatures": ["HR Connect", "Customer"],
},
{
    "slug": "data-processing-agreement",
    "file": "HRConnect-AI-Data-Processing-Agreement",
    "group": "client",
    "title": "Data Processing Agreement",
    "short": "DPA",
    "purpose": "How HR Connect handles the customer's employee data as a processor: security, sub-processors, breaches, deletion and audits.",
    "parties": [
        "This Data Processing Agreement (“DPA”) is made on [date] between:",
        company_party(1, "[Customer legal name]", "Customer"),
        company_party(2, HRC, "HR Connect"),
        "It forms part of the Master Subscription Agreement between the parties (the “Agreement”).",
    ],
    "clauses": [
        ("Definitions and roles", [
            "“Data Protection Law” means all data protection and privacy laws that apply to the processing of personal data under the Agreement. “Personal data”, “processing”, “controller”, “processor” and “data subject” have the meanings given in Data Protection Law, or their nearest equivalents.",
            "The Customer is the controller of the personal data in Customer Data and HR Connect is its processor. Annex 1 describes the processing.",
            "The Customer is responsible for having a lawful basis for the processing and for giving data subjects any required notices.",
        ]),
        ("Instructions", [
            "HR Connect will process personal data only on the Customer's documented instructions, including with regard to transfers, unless law requires otherwise. The Agreement, this DPA and the Customer's use and configuration of the Services are the Customer's instructions.",
            "HR Connect will tell the Customer if, in its opinion, an instruction breaks Data Protection Law.",
        ]),
        ("Confidentiality of personnel", [
            "HR Connect will ensure that people authorised to process personal data are bound by confidentiality duties and only access it as needed to provide the Services.",
        ]),
        ("Security", [
            "HR Connect will implement and maintain the technical and organisational measures in Annex 2, appropriate to the risk of the processing.",
            "HR Connect may update these measures, as long as the update does not reduce the overall level of protection.",
        ]),
        ("Sub-processors", [
            "The Customer gives general authorisation for HR Connect to use sub-processors. The current list is in Annex 3.",
            "HR Connect will give the Customer at least [30] days' notice before adding or replacing a sub-processor. The Customer may object on reasonable data protection grounds within that period. If the parties cannot resolve the objection, the Customer may terminate the affected Services and receive a refund of prepaid fees for the remaining term.",
            "HR Connect will impose data protection terms on each sub-processor that are no less protective than this DPA and remains responsible for its sub-processors' performance.",
        ]),
        ("Data subject requests and assistance", [
            "Taking into account the nature of the processing, HR Connect will help the Customer respond to requests from data subjects to exercise their rights, mainly through features of the Services that let the Customer view, correct, export and delete personal data.",
            "If HR Connect receives a request directly from a data subject, it will pass it to the Customer and will not respond itself unless the Customer instructs it to.",
            "HR Connect will give reasonable help with data protection impact assessments and consultations with regulators, where these relate to the Services.",
        ]),
        ("Personal data breaches", [
            "HR Connect will notify the Customer without undue delay, and in any case within [48] hours, after becoming aware of a personal data breach affecting Customer Data.",
            "The notice will describe, as far as known, the nature of the breach, the categories and approximate number of data subjects and records concerned, the likely consequences and the measures taken or proposed. HR Connect will provide further information as it becomes available.",
        ]),
        ("International transfers", [
            "HR Connect will host Customer Data in [hosting region]. HR Connect will transfer personal data to another country only where Data Protection Law allows it, using any safeguards that law requires.",
        ]),
        ("Deletion and return", [
            "When the Agreement ends, the Customer can export its personal data as set out in the Agreement. HR Connect will then delete it, including copies, within [90] days, unless law requires it to keep some of it. Backups are deleted on their normal cycle of no more than [35] days.",
        ]),
        ("Audits", [
            "HR Connect will make available the information reasonably needed to show compliance with this DPA, including [security questionnaires, policies and third-party audit reports, where available].",
            "If that information is not enough, the Customer may carry out an audit no more than once a year, on at least [30] days' notice, during business hours, at its own cost, and under confidentiality terms. Audits must not disrupt HR Connect's business or access other customers' data.",
        ]),
        ("Liability and term", [
            "Each party's liability under this DPA is subject to the limitations and exclusions in the Agreement.",
            "This DPA lasts as long as HR Connect processes personal data for the Customer under the Agreement.",
        ]),
    ],
    "schedules": [
        ("Annex 1. Details of the processing", [
            {"kv": [
                ("Subject matter", "Providing the HRConnect.AI HR and payroll software to the Customer."),
                ("Duration", "The term of the Agreement plus the deletion period in clause 9."),
                ("Nature and purpose", "Storing, organising, displaying and calculating HR records; running payroll calculations and producing payslips and bank payment files; managing leave, expenses, loans and offboarding; generating reports; answering User questions through the AI assistant; support."),
                ("Data subjects", "The Customer's current and former employees and contractors, their emergency contacts and dependants, and the Customer's Users."),
                ("Categories of personal data", "Identity and contact details; job, department, manager and employment history; compensation, payroll, bank and loan details; leave and attendance records; expense claims and receipts; documents such as IDs, contracts and certificates; offboarding records; login and usage data."),
                ("Special categories", "[Only where the Customer chooses to store them, for example health information in sick leave notes or medical certificates.]"),
                ("Frequency", "Continuous, while the Services are in use."),
            ]},
        ]),
        ("Annex 2. Technical and organisational measures", [
            "- Separation of each customer's data from other customers' data.",
            "- Role-based permissions per module, screen and action, set by the Customer.",
            "- Passwords stored as salted hashes, short-lived login sessions and [multi-factor authentication available for Users].",
            "- Uploaded files stored securely and shared only through signed, time-limited links.",
            "- [Encryption of data in transit using TLS and encryption of data at rest.]",
            "- Audit trail of payroll runs and approvals, recording who did what and when.",
            "- Regular backups and a tested restore process [state frequency].",
            "- Staff access to production data limited to named people who need it, and logged.",
            "- Vulnerability management, security patching and [annual penetration testing].",
            "- An incident response process, including the breach notice in clause 7.",
        ]),
        ("Annex 3. Sub-processors", [
            {"table": [
                ("Sub-processor", "Purpose", "Location"),
                ("[Cloud hosting provider]", "Hosting and storage", "[region]"),
                ("[Email delivery provider]", "Sending system emails", "[region]"),
                ("[AI model provider]", "Powering the AI assistant", "[region]"),
                ("[Support tool provider]", "Customer support tickets", "[region]"),
            ]},
        ]),
    ],
    "signatures": ["Customer", "HR Connect"],
},
{
    "slug": "service-level-agreement",
    "file": "HRConnect-AI-Service-Level-Agreement",
    "group": "client",
    "title": "Service Level Agreement",
    "short": "SLA",
    "purpose": "Uptime target, support hours, response times by severity and service credits if HR Connect misses the target.",
    "parties": [
        "This Service Level Agreement (“SLA”) is made on [date] between " + HRC + " (“HR Connect”) and [Customer legal name] (“Customer”). It forms part of the Master Subscription Agreement between the parties (the “Agreement”).",
    ],
    "clauses": [
        ("Availability", [
            "HR Connect will make the Services available [99.5]% of the time in each calendar month (the “Availability Target”).",
            "Availability is calculated as: (total minutes in the month − minutes of Downtime) ÷ total minutes in the month × 100. “Downtime” means time when Users cannot log in to or use the core features of the Services, as confirmed by HR Connect's monitoring.",
        ]),
        ("Exclusions", [
            "Downtime does not include time caused by:",
            "- scheduled maintenance announced at least [48] hours in advance and carried out within [the maintenance window, for example 22:00–04:00 in the Customer's time zone], up to [4] hours a month;",
            "- emergency security maintenance;",
            "- the Customer's systems, internet connection, configuration or misuse of the Services;",
            "- events beyond HR Connect's reasonable control, as described in the Agreement;",
            "- features labelled beta, preview or trial.",
        ]),
        ("Support", [
            "Support is available by [in-app chat and email to support@hrconnect.ai] during [Monday to Friday, 09:00–18:00 in the Customer's main time zone], excluding public holidays at [location] (“Business Hours”). Severity 1 issues are handled [24/7].",
            "HR Connect will respond to support requests within the times below, measured from when the request is received:",
            {"table": [
                ("Severity", "Meaning", "First response", "Updates"),
                ("1 – Critical", "Services unavailable for all Users, or a payroll run is blocked close to the pay date", "[1 hour]", "Every [2] hours until resolved"),
                ("2 – High", "A major feature does not work and there is no workaround", "[4 Business Hours]", "Every [business day]"),
                ("3 – Normal", "A feature does not work as expected but there is a workaround", "[1 business day]", "As progress is made"),
                ("4 – Low", "Questions, how-to requests and feature suggestions", "[3 business days]", "As needed"),
            ]},
            "The Customer will give the information reasonably needed to reproduce and diagnose an issue, and will name up to [3] people as support contacts.",
        ]),
        ("Service credits", [
            "If availability in a month falls below the Availability Target, the Customer may claim a service credit, calculated as a percentage of the monthly subscription fee for that month:",
            {"table": [
                ("Monthly availability", "Service credit"),
                ("Below [99.5]% but at least [99.0]%", "[5]%"),
                ("Below [99.0]% but at least [98.0]%", "[10]%"),
                ("Below [98.0]%", "[20]%"),
            ]},
            "The Customer must claim a credit in writing within [30] days after the end of the month concerned. Credits are applied to the next invoice and are not paid in cash.",
            "Service credits in any month are capped at [20]% of that month's subscription fee. Service credits are the Customer's sole remedy for failing to meet the Availability Target, except where the Customer terminates under clause 5.",
        ]),
        ("Chronic failure", [
            "If availability is below [98.0]% in any [three] months in a rolling twelve-month period, the Customer may terminate the affected Order Form by written notice within [30] days and receive a refund of prepaid fees for the remaining term.",
        ]),
        ("Status and reporting", [
            "HR Connect will publish service status and planned maintenance at [status page URL] and, on request, give the Customer a monthly availability report.",
        ]),
    ],
    "signatures": ["HR Connect", "Customer"],
},
# ---------------------------------------------------------------- employee and contractor contracts
{
    "slug": "offer-letter",
    "file": "HRConnect-AI-Offer-Letter",
    "group": "people",
    "title": "Offer Letter",
    "short": "Offer",
    "purpose": "A short letter that offers a candidate the job with the key terms, ahead of the full employment contract.",
    "numbered": False,
    "letter": True,
    "parties": [
        "[Company name]\n[Company address]",
        "[Date]",
        "Private and confidential\n[Candidate full name]\n[Candidate address]",
        "Dear [Candidate first name],",
    ],
    "clauses": [
        ("Offer of employment", [
            "> We are delighted to offer you the role of [job title] at [Company name]. We enjoyed getting to know you during the interviews and believe you will make a strong addition to the [department] team.",
            "> The main terms of the offer are below. Your full terms will be set out in your employment contract, which we will send you to sign.",
        ]),
        ("Key terms", [
            {"kv": [
                ("Job title", "[job title]"),
                ("Department", "[department]"),
                ("Reports to", "[manager name, job title]"),
                ("Place of work", "[office address / remote / hybrid]"),
                ("Start date", "[date]"),
                ("Employment type", "[Full-time / part-time], [permanent / fixed term until date]"),
                ("Monthly gross salary", "$[0.00], paid monthly in arrears"),
                ("Probation period", "[3] months"),
                ("Working hours", "[40] hours a week, [Monday to Friday]"),
                ("Annual leave", "[20] working days a year plus public holidays"),
                ("Benefits", "[health insurance / allowances / bonus scheme / none]"),
                ("Notice period", "[1] week during probation, [1] month after"),
            ]},
        ]),
        ("Conditions", [
            "> This offer is conditional on:",
            "- satisfactory references from [number] previous employers;",
            "- proof of your identity and your right to work in [country];",
            "- [satisfactory background checks / confirmation of qualifications], where lawful; and",
            "- your signing the employment contract before your start date.",
        ]),
        ("Next steps", [
            "> To accept, please sign and return this letter by [date]. We will then send your employment contract and an invitation to set up your HR Connect self-service account, where you can add your personal and bank details before your first day.",
            "> If you have any questions, please contact [name] at [email].",
            "> We look forward to welcoming you to the team.",
            "> Yours sincerely,",
        ]),
    ],
    "signatures": ["Company", "Candidate acceptance"],
    "signature_note": "I accept this offer on the terms above.",
},
{
    "slug": "employment-contract",
    "file": "HRConnect-AI-Employment-Contract",
    "group": "people",
    "title": "Employment Contract",
    "short": "Employment",
    "purpose": "The full terms for a full-time employee: duties, probation, hours, salary, leave, confidentiality, IP and notice.",
    "parties": [
        "This Employment Contract (the “Contract”) is made on [date] between:",
        company_party(1, "[Company name]", "Company"),
        "(2) [Employee full name] of [employee address] (“Employee”).",
    ],
    "clauses": [
        ("Start of employment", [
            "The Employee's employment starts on [start date]. [The Employee's previous employment with [previous employer] does not count towards continuous employment.]",
            "This is a [permanent / fixed-term] contract. [If fixed term: it ends on [end date] unless terminated earlier under clause 16 or extended in writing.]",
        ]),
        ("Job title and duties", [
            "The Employee is employed as [job title] in the [department] department, reporting to [manager job title].",
            "The Employee will carry out the duties set out in the job description and any other reasonable duties the Company assigns that fit the Employee's skills and role.",
            "The Employee will follow the Company's lawful and reasonable instructions and policies, and will act in good faith in the Company's interests.",
        ]),
        ("Place of work", [
            "The Employee's normal place of work is [office address / remote / hybrid, at least [number] days a week at the office]. The Company may require reasonable business travel.",
        ]),
        ("Probation", [
            "The first [3] months of employment are a probation period. The Company may extend it by up to [3] months by written notice before it ends.",
            "During probation, either party may end the employment by giving [1] week's written notice.",
        ]),
        ("Working hours", [
            "The Employee's normal working hours are [40] hours a week, [09:00 to 18:00, Monday to Friday], with [1] hour unpaid break each day.",
            "The Employee may need to work additional hours to perform the role. [Overtime is paid at [rate] / is not separately paid and is reflected in the salary], subject to applicable law.",
        ]),
        ("Salary", [
            "The Employee's gross salary is $[0.00] per month ($[0.00] per year).",
            "Salary is paid monthly in arrears on or before [the last working day] of each month, by bank transfer to the account the Employee records in the Company's HR system.",
            "The Company will make any deductions required by law and any deductions the Employee agrees to in writing, such as repayments of a salary advance or loan.",
            "Payslips are available to the Employee through the self-service area of the Company's HR system.",
            "Salary is reviewed [annually]. A review does not guarantee an increase.",
        ]),
        ("Bonus and benefits", [
            "The Employee [is / is not] eligible for the [bonus scheme name], under its rules in force from time to time. Any bonus is discretionary unless the scheme rules say otherwise.",
            "The Employee is entitled to the following benefits: [health insurance, allowances, pension or retirement plan, other]. The Company may change benefit providers or terms on reasonable notice.",
        ]),
        ("Expenses", [
            "The Company will reimburse reasonable expenses the Employee properly incurs for work, in line with the Company's expense policy. Claims must be submitted through the Company's HR system with receipts within [30] days.",
        ]),
        ("Annual leave", [
            "The Employee is entitled to [20] working days' paid annual leave in each leave year, plus public holidays observed at [location]. The leave year runs from [1 January to 31 December].",
            "Leave is requested and approved through the Company's HR system. Up to [5] days of unused leave may be carried over to the next leave year [and must be used within [3] months].",
            "On termination, the Employee will be paid for accrued but untaken leave, or the Company will deduct pay for leave taken in excess of accrual, as allowed by law.",
        ]),
        ("Sick leave and other leave", [
            "If the Employee is unable to work because of illness, they must tell their manager as early as possible on the first day of absence and record the absence in the HR system. A medical certificate is required for absences of more than [2] consecutive days.",
            "The Employee is entitled to [number] days' paid sick leave a year, and to statutory sick pay where it applies.",
            "The Employee is entitled to parental, bereavement and other leave as required by law and as set out in the Company's leave policy.",
        ]),
        ("Confidentiality", [
            "During and after employment, the Employee will not use or disclose any confidential information about the Company, its customers, suppliers or employees, except as needed to do their job or as required by law.",
            "Confidential information includes business plans, finances, customer lists, pricing, product designs, source code, personnel and salary information, and any information marked or treated as confidential.",
        ]),
        ("Intellectual property", [
            "All intellectual property created by the Employee in the course of their employment belongs to the Company. To the extent it does not belong to the Company automatically, the Employee assigns it to the Company.",
            "The Employee will sign any documents reasonably needed to confirm the Company's ownership, during or after employment.",
        ]),
        ("Outside activities and conflicts", [
            "During employment, the Employee will not take on other paid work or any activity that conflicts with the Company's interests without the Company's prior written consent, which will not be unreasonably withheld.",
            "The Employee will tell the Company promptly of any actual or potential conflict of interest.",
        ]),
        ("Restrictions after employment", [
            "For [6] months after employment ends, the Employee will not solicit or try to hire any employee of the Company with whom they worked in the last [12] months of employment.",
            "For [6] months after employment ends, the Employee will not solicit business from any customer of the Company with whom they dealt in the last [12] months of employment.",
            "[Include any non-compete only where enforceable in the relevant jurisdiction, and limit it in time, area and scope.]",
        ]),
        ("Personal data", [
            "The Company processes the Employee's personal data for employment purposes, as described in its employee privacy notice. The Employee will keep their personal details in the HR system up to date.",
        ]),
        ("Notice and termination", [
            "After probation, either party may end the employment by giving [1] month's written notice, or the longer notice required by law.",
            "The Company may pay the Employee's basic salary in lieu of all or part of the notice period, or require the Employee not to attend work during all or part of it while continuing to receive salary and benefits.",
            "The Company may end the employment immediately without notice or pay in lieu in case of gross misconduct or a serious breach of this Contract, as allowed by law.",
            "[End-of-service or severance payments are made as required by applicable law.]",
        ]),
        ("Return of property", [
            "When employment ends, or earlier if asked, the Employee will return all Company property, including equipment, access cards, documents and data, and will not keep any copies.",
        ]),
        ("Disciplinary and grievance", [
            "The Company's disciplinary and grievance procedures are set out in the employee handbook. They do not form part of this Contract.",
        ]),
        ("General", [
            "This Contract, together with the Company's policies as amended from time to time, is the entire agreement between the parties about the employment. Where a policy conflicts with this Contract, this Contract prevails.",
            "Changes to this Contract must be agreed in writing, except for minor changes to policies that the Company notifies to the Employee.",
            "This Contract is governed by the laws of [country / state], and its courts have exclusive jurisdiction.",
        ]),
    ],
    "signatures": ["Company", "Employee"],
},
{
    "slug": "contractor-agreement",
    "file": "HRConnect-AI-Independent-Contractor-Agreement",
    "group": "people",
    "title": "Independent Contractor Agreement",
    "short": "Contractor",
    "purpose": "For freelancers and consultants: the services, fees and invoicing, independent status and IP assignment, with a statement of work.",
    "parties": [
        "This Independent Contractor Agreement (the “Agreement”) is made on [date] between:",
        company_party(1, "[Company name]", "Company"),
        "(2) [Contractor name / Contractor company name] of [address], [company number if a company] (“Contractor”).",
    ],
    "clauses": [
        ("Services", [
            "The Contractor will provide the services described in the Statement of Work in Schedule 1 (the “Services”). The parties may add further Statements of Work by signing them.",
            "The Contractor will provide the Services with reasonable skill and care, in line with good industry practice and any agreed timetable.",
        ]),
        ("Term", [
            "This Agreement starts on [start date] and continues until [end date / completion of the Services], unless terminated earlier under clause 12.",
        ]),
        ("Fees and invoicing", [
            "The Company will pay the Contractor the fees in Schedule 1, which are [$[0.00] per hour / $[0.00] per day / a fixed fee of $[0.00] payable on the milestones in Schedule 1].",
            "The Contractor will invoice [monthly in arrears / on completion of each milestone], with a summary of the time spent or deliverables completed. The Company will pay undisputed invoices within [30] days.",
            "The Company will reimburse reasonable expenses only if approved in writing in advance and supported by receipts.",
            "The Contractor is responsible for its own taxes, social contributions, insurance and registrations in connection with the fees. [Fees exclude any applicable sales or value-added tax, which the Contractor will show on its invoices.]",
        ]),
        ("Independent contractor status", [
            "The Contractor is an independent contractor and not an employee, worker, partner or agent of the Company. Nothing in this Agreement creates an employment relationship.",
            "The Contractor decides how, when and where to perform the Services, subject to meeting agreed deadlines and reasonable site and security rules. The Contractor provides its own equipment unless agreed otherwise.",
            "The Contractor is not entitled to salary, paid leave, benefits or any other employee rights from the Company.",
            "The Contractor may work for other clients during this Agreement, as long as this does not conflict with its duties under it.",
            "[The Contractor may send a suitably qualified substitute, with the Company's prior approval, which will not be unreasonably withheld. The Contractor remains responsible for the substitute.]",
        ]),
        ("Deliverables and acceptance", [
            "Where Schedule 1 lists deliverables, the Company will review each one within [10] business days of delivery and either accept it or explain in writing how it does not meet the agreed requirements. The Contractor will fix any such issues at no extra cost.",
        ]),
        ("Intellectual property", [
            "All intellectual property in the deliverables and anything else the Contractor creates for the Company under this Agreement (“Work Product”) is assigned to the Company on creation, or on payment of the related fees [if preferred].",
            "The Contractor keeps ownership of tools, know-how and materials it owned before this Agreement or creates independently of it (“Contractor Materials”). If Contractor Materials are included in Work Product, the Contractor grants the Company a perpetual, royalty-free, worldwide licence to use them as part of the Work Product.",
            "The Contractor will not include third-party or open-source materials in Work Product without telling the Company first.",
        ]),
        ("Confidentiality", [
            "The Contractor will keep the Company's confidential information secret, use it only to provide the Services, and return or delete it when this Agreement ends. This duty continues after the Agreement ends.",
        ]),
        ("Data protection", [
            "If the Contractor processes personal data on the Company's behalf, it will do so only on the Company's instructions, keep it secure, and comply with applicable data protection law.",
        ]),
        ("Warranties", [
            "The Contractor warrants that it has the right to enter into this Agreement, that the Work Product will be its original work, and that the Company's use of the Work Product will not infringe any third party's rights.",
        ]),
        ("Insurance", [
            "[The Contractor will maintain professional indemnity insurance of at least $[0.00] and public liability insurance of at least $[0.00] during this Agreement, and provide evidence on request.]",
        ]),
        ("Liability", [
            "Neither party is liable for indirect or consequential loss. Each party's total liability under this Agreement is limited to [the total fees paid and payable under it], except for breaches of clauses 6 and 7, fraud, and liability that cannot be limited by law.",
        ]),
        ("Termination", [
            "Either party may end this Agreement by giving [14] days' written notice.",
            "Either party may end it immediately by written notice if the other commits a material breach that is not remedied within [7] days of being notified.",
            "On termination, the Company will pay for Services properly performed up to the termination date, and the Contractor will deliver all Work Product in progress and return the Company's property and information.",
        ]),
        ("Non-solicitation", [
            "For [12] months after this Agreement ends, neither party will directly solicit for employment any employee of the other party with whom it dealt under this Agreement, without the other party's consent. General job adverts are allowed.",
        ]),
        ("General", [
            GENERAL_LAW,
            "This Agreement and its Schedules are the entire agreement between the parties about its subject. Changes must be in writing and signed by both parties. Neither party may assign it without the other's consent.",
        ]),
    ],
    "schedules": [
        ("Schedule 1. Statement of Work", [
            {"kv": [
                ("Project name", "[project name]"),
                ("Description of the Services", "[what the Contractor will do]"),
                ("Deliverables", "[list each deliverable]"),
                ("Milestones and dates", "[milestone – date]"),
                ("Fees", "[$0.00 per hour / day, or fixed fee and payment per milestone]"),
                ("Estimated hours or cap", "[for example, up to 80 hours a month without written approval]"),
                ("Company contact", "[name, email]"),
                ("Location and working arrangements", "[remote / on site at address, days]"),
            ]},
        ]),
    ],
    "signatures": ["Company", "Contractor"],
},
{
    "slug": "mutual-nda",
    "file": "HRConnect-AI-Mutual-NDA",
    "group": "people",
    "title": "Mutual Non-Disclosure Agreement",
    "short": "NDA",
    "purpose": "Two-way confidentiality for early conversations with prospects, partners, candidates or contractors before sharing sensitive details.",
    "parties": [
        "This Mutual Non-Disclosure Agreement (the “Agreement”) is made on [date] between:",
        company_party(1, "[Party A legal name]", "Party A"),
        company_party(2, "[Party B legal name]", "Party B"),
        "Each a “party”. A party disclosing information is the “Discloser” and a party receiving it is the “Recipient”.",
    ],
    "clauses": [
        ("Purpose", [
            "The parties wish to share information to [evaluate a possible business relationship concerning HR software / discuss a possible engagement] (the “Purpose”).",
        ]),
        ("Confidential Information", [
            "“Confidential Information” means any information, in any form, that the Discloser shares with the Recipient in connection with the Purpose and that is marked confidential or that a reasonable person would consider confidential. It includes business plans, finances, customer and employee information, product plans, software, pricing and the fact that the parties are in discussions.",
        ]),
        ("Exclusions", [
            "Confidential Information does not include information that the Recipient can show:",
            "- is or becomes public through no fault of the Recipient;",
            "- was lawfully known to the Recipient before disclosure, without a duty of confidentiality;",
            "- is lawfully received from a third party without a duty of confidentiality; or",
            "- is independently developed by the Recipient without using the Confidential Information.",
        ]),
        ("Obligations", [
            "The Recipient will: (a) use Confidential Information only for the Purpose; (b) protect it with at least the care it uses for its own confidential information, and no less than reasonable care; and (c) disclose it only to its employees, officers, contractors and professional advisers who need to know it for the Purpose and are bound by confidentiality duties at least as protective as this Agreement.",
            "The Recipient is responsible for any breach of this Agreement by the people it shares Confidential Information with.",
            "The Recipient will tell the Discloser promptly if it becomes aware of any unauthorised use or disclosure.",
        ]),
        ("Disclosure required by law", [
            "The Recipient may disclose Confidential Information if required by law, regulation or a court, as long as it gives the Discloser prompt notice, where lawful, and discloses only what is required.",
        ]),
        ("Return and destruction", [
            "On the Discloser's written request, the Recipient will promptly return or destroy the Discloser's Confidential Information. The Recipient may keep copies that are required by law or held in routine backups, which remain subject to this Agreement.",
        ]),
        ("No licence or warranty", [
            "All Confidential Information remains the property of the Discloser. No licence or other rights are granted under this Agreement, except the right to use Confidential Information for the Purpose.",
            "Confidential Information is provided “as is”. Neither party is obliged to enter into any further agreement or transaction.",
        ]),
        ("Term", [
            "This Agreement covers information disclosed in the [2] years after the date above. The Recipient's duties for each item of Confidential Information last for [3] years after its disclosure, or, for trade secrets, for as long as they remain trade secrets.",
        ]),
        ("Remedies", [
            "Each party acknowledges that damages alone may not be an adequate remedy for a breach of this Agreement, and that the Discloser may seek an injunction or other equitable relief in addition to any other remedy.",
        ]),
        ("General", [
            GENERAL_LAW,
            "This Agreement is the entire agreement between the parties about its subject. Changes must be in writing and signed by both parties. It may be signed electronically and in counterparts.",
        ]),
    ],
    "signatures": ["Party A", "Party B"],
},
]

GROUPS = [
    ("client", "Client contracts", "Between HR Connect and a customer. Use the MSA as the base, add an Order Form for each purchase, and attach the DPA and SLA."),
    ("people", "Employee and contractor contracts", "Templates a company uses with the people who work for it. Customers can adapt them for their own hires, and HR Connect can use them for its own team."),
]
