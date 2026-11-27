/* HRConnect.AI promo video (60 seconds, 11 scenes), from research/video-storyboard.html.
   Every frame is a pure function of time, so the video can play, pause, seek and loop.
   Usage: <div class="pv" data-demo-href="./book-a-demo/index.html"></div> + this script. */
(() => {
'use strict';

/* ---------- Timing and easing ---------- */
const IN = 0.7, OUT = 0.55, GAP = 0.12;
const clamp = (v, a = 0, b = 1) => Math.min(b, Math.max(a, v));
const eOut = t => 1 - Math.pow(1 - t, 3);
const eIn = t => t * t * t;
const eBack = t => t <= 0 ? 0 : 1 + 2.7 * Math.pow(t - 1, 3) + 1.7 * Math.pow(t - 1, 2);
const eIO = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const prog = (lt, a, b) => clamp((lt - a) / (b - a));
const pulse = (lt, at, len = .9) => { const p = (lt - at) / len; return p < 0 || p > 1 ? 0 : Math.sin(Math.PI * p); };
const money = n => '$' + Math.round(n).toLocaleString('en-US');
const fmt = s => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, '0')}`;

/* Motion presets: [dx, dy, scale, rotate, rotateX] for entering (i) and leaving (o) */
const PRE = {
  up: { i: [0, 46], o: [0, -46] }, down: { i: [0, -46], o: [0, 46] },
  left: { i: [-110, 0], o: [110, 0] }, right: { i: [110, 0], o: [-110, 0] },
  pop: { i: [0, 0, .7], o: [0, 0, 1.1] }, zoom: { i: [0, 0, 1.25], o: [0, 0, .9] },
  blur: { i: [0, 26], o: [0, -26], b: 12 }, fade: { i: [0, 0], o: [0, 0] },
  flip: { i: [0, 40, .95, 0, -75], o: [0, -30, .98, 0, 40] }
};
const vec = (a, s) => { const v = (s ? s.split(',').map(Number) : a) || []; return [v[0] || 0, v[1] || 0, v[2] ?? 1, v[3] || 0, v[4] || 0]; };

/* ---------- Markup helpers ---------- */
const P = {
  users: '<path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
  pay: '<rect x="2" y="6" width="20" height="12" rx="2"/><circle cx="12" cy="12" r="2.5"/><path d="M6 12h.01M18 12h.01"/>',
  cal: '<rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
  receipt: '<path d="M4 2v20l2-1 2 1 2-1 2 1 2-1 2 1 2-1 2 1V2l-2 1-2-1-2 1-2-1-2 1-2-1-2 1Z"/><path d="M8 8h8M8 12h8M8 16h5"/>',
  coins: '<circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18M7 6h1v4M16.71 13.88l.7.71-2.82 2.82"/>',
  file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M16 13H8M16 17H8M10 9H8"/>',
  exit: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4M16 17l5-5-5-5M21 12H9"/>',
  self: '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="10" r="3"/><path d="M7 20.66V19a2 2 0 0 1 2-2h6a2 2 0 0 1 2 2v1.66"/>',
  spark: '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9z"/><path d="M19 3v4M17 5h4"/>',
  case: '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
  mail: '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/>',
  sheet: '<rect x="3" y="3" width="18" height="18" rx="2"/><path d="M3 9h18M3 15h18M9 3v18"/>',
  check: '<path d="M20 6 9 17l-5-5"/>',
  arrow: '<path d="M5 12h14M12 5l7 7-7 7"/>'
};
const ico = (k, size, bg, fg, r) => `<span class="pv-ico" style="width:${size}px;height:${size}px;border-radius:${r ?? Math.round(size * .28)}px;background:${bg};color:${fg}"><svg viewBox="0 0 24 24">${P[k]}</svg></span>`;
const mark = (size, onDark) => `<svg viewBox="0 0 48 48" width="${size}" height="${size}" style="flex:none;display:block"><rect width="48" height="48" rx="13" fill="${onDark ? '#fff' : '#6C3845'}"/><path d="M14 13V35M34 13V35M14 24H34" fill="none" stroke="${onDark ? '#6C3845' : '#fff'}" stroke-width="2.4" stroke-linecap="round"/><circle cx="14" cy="13" r="3.4" fill="${onDark ? '#6C3845' : '#fff'}"/><circle cx="14" cy="35" r="3.4" fill="${onDark ? '#6C3845' : '#fff'}"/><circle cx="34" cy="13" r="3.4" fill="${onDark ? '#6C3845' : '#fff'}"/><circle cx="34" cy="35" r="3.4" fill="${onDark ? '#6C3845' : '#fff'}"/><circle cx="24" cy="24" r="4.4" fill="${onDark ? '#B97A8A' : '#D9C8CC'}"/></svg>`;
const brand = (size, onDark) => `<span style="display:inline-flex;align-items:center;gap:${size * .42}px;font-size:${size}px;font-weight:700;letter-spacing:-.02em;line-height:1;color:${onDark ? '#fff' : '#1B1620'}">${mark(size * 1.45, onDark)}<span style="font-family:Sora,Inter,sans-serif">HRConnect<span style="color:${onDark ? '#D9C8CC' : '#6C3845'}">.AI</span></span></span>`;
/* Animated element: absolute at scene level, or nested (relative) inside another */
const A = (a, d, style, html, k = '') => `<div class="pv-a" ${a.includes(',') ? `data-in="${a.split('|')[0]}" data-out="${a.split('|')[1] || ''}"` : `data-a="${a}"`} data-d="${d}"${k ? ` data-k="${k}"` : ''} style="position:absolute;${style}">${html}</div>`;
const N = (a, d, html, style = '', k = '') => `<div class="pv-a" data-a="${a}" data-d="${d}"${k ? ` data-k="${k}"` : ''} style="position:relative;${style}">${html}</div>`;
const W = 'rgba(255,255,255,';
const wm = onDark => A('fade', .2, 'right:28px;top:24px;opacity:.9', brand(15, onDark));
const caption = (ey, title, onDark) =>
  A('left', .1, `left:56px;top:96px;width:300px`, `<div class="pv-ey" style="font-size:13px;color:${onDark ? '#D9C8CC' : '#6C3845'}">${ey}</div>`) +
  A('left', .25, `left:56px;top:124px;width:310px;--hl:${onDark ? '#D9C8CC' : '#6C3845'}`, `<div class="pv-h ${onDark ? 'pv-gt' : ''}" style="font-size:40px;color:${onDark ? '#fff' : '#1B1620'}">${title}</div>`);

/* ---------- Scenes ---------- */
const CHAPTERS = ['Introduction', 'Products', 'Services', 'Book a demo'];
const S = [];

/* 01 · The problem */
S.push({ ch: 0, dur: 4, bg: 'paper', vo: 'Spreadsheets, email threads, five different tools.',
  html: (() => {
    const wins = [
      ['sheet', 'Leave_tracker_FINAL_v3.xlsx', 70, 70, -5, '#0F8A5F', '3', '-340,-40,1,-14|245,130,.25,10'],
      ['mail', 'Re: Re: Fwd: expense receipts', 490, 48, 4, '#3B6FB6', '12', '340,-70,1,14|-175,150,.25,-10'],
      ['sheet', 'Payroll_Oct_check.xlsx', 110, 280, 3, '#0F8A5F', '!', '-360,70,1,10|205,-80,.25,-8'],
      ['file', 'Policy handbook 2019.pdf', 540, 262, -4, '#B3261E', '2', '360,60,1,-10|-225,-60,.25,8']];
    return wins.map(([k, t, x, y, r, c, n, mv], i) => A(mv, .05 + i * .15, `left:${x}px;top:${y}px;width:330px`,
      `<div class="pv-card" style="transform:rotate(${r}deg);border-radius:12px">
        <span class="pv-badge">${n}</span>
        <div style="display:flex;align-items:center;gap:8px;padding:10px 12px;background:#F4F1F2;border-bottom:1px solid #E5DFE1;border-radius:12px 12px 0 0;font-size:13px;font-weight:600">${ico(k, 22, c, '#fff', 6)}${t}</div>
        <div style="padding:12px;display:grid;gap:7px">${[90, 70, 82, 55].map(w => `<span style="display:block;height:9px;width:${w}%;background:#ECE6E8;border-radius:4px"></span>`).join('')}</div>
      </div>`)).join('') +
      A('0,0,.4,-20|0,0,.2,25', .85, 'left:392px;top:200px;width:186px', `<div style="transform:rotate(-6deg);background:#FFE58A;color:#5B4A00;font-size:17px;font-weight:700;line-height:1.3;padding:16px;box-shadow:0 12px 26px rgba(0,0,0,.2)">Who approved Jordan's leave??</div>`) +
      A('up', 1.2, 'left:0;right:0;bottom:0;padding:26px 56px 75px;text-align:center;background:linear-gradient(0deg,rgba(27,22,32,.9),rgba(27,22,32,0))', `<div class="pv-h" style="font-size:36px;color:#fff">Too many tools. Too much admin.</div>`);
  })() });

/* 02 · Logo reveal */
S.push({ ch: 0, dur: 4, bg: 'dark', vo: 'There\'s a simpler way. Meet HRConnect.AI.',
  html: A('0,0,.3|0,0,1.4', 1.05, 'left:300px;top:20px;width:360px;height:360px;border-radius:50%;background:radial-gradient(circle,rgba(240,170,195,.55),rgba(240,170,195,0) 65%)', '', 'burst') +
    A('0,0|0,-30', .05, 'left:370px;top:60px', `<svg class="pv-glowf" data-k="h" width="220" height="220" viewBox="0 0 48 48" style="display:block;overflow:visible"><path data-k="v0" d="M14 13V35" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><path data-k="v1" d="M34 13V35" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><path data-k="b0" d="M14 24H24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><path data-k="b1" d="M34 24H24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/><circle data-k="n0" cx="14" cy="13" r="3.4" fill="#fff" style="transform-box:fill-box;transform-origin:center;transform:scale(0)"/><circle data-k="n1" cx="34" cy="13" r="3.4" fill="#fff" style="transform-box:fill-box;transform-origin:center;transform:scale(0)"/><circle data-k="n2" cx="14" cy="35" r="3.4" fill="#fff" style="transform-box:fill-box;transform-origin:center;transform:scale(0)"/><circle data-k="n3" cx="34" cy="35" r="3.4" fill="#fff" style="transform-box:fill-box;transform-origin:center;transform:scale(0)"/><circle data-k="c" cx="24" cy="24" r="4.4" fill="#D9C8CC" style="transform-box:fill-box;transform-origin:center;transform:scale(0)"/></svg>`) +
    A('fade', 1.15, 'left:0;width:960px;top:300px;text-align:center', `<span data-k="word" class="pv-gt" style="display:inline-block;clip-path:inset(0 100% 0 0);font-size:60px;font-weight:800;letter-spacing:-.03em">HRConnect<span style="color:#D9C8CC">.AI</span></span>`) +
    A('blur', 1.95, 'left:0;width:960px;top:392px;text-align:center;font-size:22px;color:rgba(255,255,255,.78)', 'There\'s a simpler way.') });

/* 03 · The promise */
S.push({ ch: 0, dur: 6, bg: 'dark', vo: 'The AI-powered HR app where records, payroll, leave and expenses share one set of data.',
  html: wm(true) +
    A('blur', .15, 'left:64px;top:104px', `<div class="pv-ey" style="font-size:15px;color:#E6CFD5">AI-powered HR</div>`) +
    A('blur', .35, 'left:64px;top:140px;white-space:nowrap', `<div class="pv-h" style="font-size:64px">The AI-powered HR app</div>`) +
    A('blur', .55, 'left:64px;top:212px;white-space:nowrap', `<div class="pv-h" style="font-size:64px">that <b class="pv-gt">connects everything</b></div>`) +
    A('up', .8, 'left:64px;top:304px;font-size:22px;color:rgba(255,255,255,.8)', 'Records, payroll, leave and expenses share one set of data.') +
    (() => {
      const chips = [['Records', 124], ['Payroll', 118], ['Leave', 100], ['Expenses', 134]];
      let x = 64, out = '';
      chips.forEach(([t, w], i) => {
        const hot = t === 'Payroll';
        out += A('pop', 1.2 + i * .28, `left:${x}px;top:382px;width:${w}px`, `<div class="pv-glow" ${hot ? 'data-k="hot"' : ''} style="text-align:center;font-size:18px;font-weight:700;padding:11px 0;border-radius:999px;background:${hot ? '#fff' : W + '.1)'};color:${hot ? '#4A2530' : '#fff'};border:1px solid ${W}.22)">${t}</div>`);
        if (i < chips.length - 1) out += A('fade', 1.35 + i * .28, `left:${x + w + 6}px;top:405px;width:28px;height:2px`, `<span data-k="c${i}" style="display:block;height:2px;background:rgba(255,255,255,.55);transform-origin:left;transform:scaleX(0)"></span>`);
        x += w + 40;
      });
      return out;
    })() });

/* 04 · Payroll */
S.push({ ch: 1, dur: 6, bg: 'soft', vo: 'Run payroll with approvals. Loans, expenses and final settlements flow into every run.',
  html: caption('Payroll', 'Monthly payroll, <b>approved and paid</b>', false) + wm(false) +
    A('up', .35, 'left:390px;top:62px;width:520px', `<div class="pv-card" style="padding:22px 24px">
      ${N('fade', .5, `<div style="display:flex;justify-content:space-between;align-items:center"><div style="font-size:17px;font-weight:700">Payroll run · October 2026</div><span class="pv-pill pv-pend pv-glow" data-k="status">In review</span></div>`)}
      <div style="margin-top:14px;display:grid;grid-template-columns:repeat(3,1fr);gap:10px">
        ${[['Employees', 'k0'], ['Gross pay', 'k1'], ['Net pay', 'k2']].map(([l, k], i) => N('up', .6 + i * .1, `<div class="pv-kpi"><small>${l}</small><strong data-k="${k}">0</strong></div>`)).join('')}
      </div>
      <div style="margin-top:8px">
        ${[['SM', 'Sarah Mitchell', 'Base salary + bonus', '$9,200'], ['AM', 'Ashley Martinez', 'Joined Oct 12 · pro-rated', '$3,980'], ['CN', 'Chris Nguyen', 'Loan installment deducted', '$6,150']].map(([i, n, d, v], j) =>
          N('right', 1.0 + j * .18, `<div class="pv-li"><span class="pv-av">${i}</span><div style="flex:1"><div style="font-size:15px;font-weight:700">${n}</div><div style="font-size:12.5px;color:#6B6470">${d}</div></div><div style="font-size:15px;font-weight:700">${v}</div><span class="pv-pill pv-pend pv-glow" data-k="p${j}">Pending</span></div>`)).join('')}
      </div></div>`) +
    A('pop', 3.4, 'left:64px;top:318px', `<div class="pv-callout">Loans, expenses and final pay flow in</div>`) +
    A('pop', 3.8, 'left:104px;top:366px', `<div class="pv-callout plum">Payslips go out when marked paid</div>`) });

/* 05 · Leave */
S.push({ ch: 1, dur: 5, bg: 'soft', vo: 'Employees see their balance before they ask. Managers approve from one list.',
  html: caption('Leave', 'Leave requests, <b>without the back-and-forth</b>', false) + wm(false) +
    A('up', .3, 'left:390px;top:62px;width:520px', `<div class="pv-card" style="padding:22px 24px">
      ${N('fade', .45, `<div style="font-size:17px;font-weight:700">Time-off requests</div>`)}
      <div style="margin-top:14px;display:grid;grid-template-columns:repeat(3,1fr);gap:10px">
        ${[['Annual left', 'k0'], ['Sick used', 'k1'], ['Carried over', 'k2']].map(([l, k], i) => N('up', .55 + i * .1, `<div class="pv-kpi"><small>${l}</small><strong data-k="${k}">0</strong></div>`)).join('')}
      </div>
      <div style="margin-top:8px">
        ${N('right', .95, `<div class="pv-li"><span class="pv-av">MB</span><div style="flex:1"><div style="font-size:15px;font-weight:700">Michael Brooks</div><div style="font-size:12.5px;color:#6B6470">Annual leave · 4 working days</div></div><span data-k="btn" class="pv-pill pv-glow" style="background:#6C3845;color:#fff;padding:6px 14px;font-size:12.5px">Approve</span></div>`)}
        ${N('right', 1.12, `<div class="pv-li"><span class="pv-av">EC</span><div style="flex:1"><div style="font-size:15px;font-weight:700">Emily Carter</div><div style="font-size:12.5px;color:#6B6470">Bereavement leave · 3 working days</div></div><span class="pv-pill pv-ok">Approved</span></div>`)}
        ${N('right', 1.29, `<div class="pv-li"><span class="pv-av">JL</span><div style="flex:1"><div style="font-size:15px;font-weight:700">Jordan Lee</div><div style="font-size:12.5px;color:#6B6470">Sick leave · 1 working day</div></div><span class="pv-pill pv-ok">Approved</span></div>`)}
      </div></div>`) +
    A('fade', 1.5, 'left:0;top:0;width:0;height:0', `<div data-k="cursor" style="position:absolute;left:0;top:0;width:26px;height:26px"><span data-k="ripple" style="position:absolute;left:-18px;top:-18px;width:36px;height:36px;border-radius:50%;border:3px solid #B97A8A;opacity:0"></span><svg width="26" height="26" viewBox="0 0 24 24" style="display:block;filter:drop-shadow(0 3px 6px rgba(0,0,0,.35))"><path d="M4 2l16 9-7 2-3 7z" fill="#1B1620" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg></div>`) +
    A('pop', 3.2, 'left:64px;top:318px', `<div class="pv-callout">Balance shown before they ask</div>`) +
    A('pop', 3.5, 'left:104px;top:366px', `<div class="pv-callout plum">Manager taps Approve</div>`) });

/* 06 · Expenses with AI */
S.push({ ch: 1, dur: 5, bg: 'dark', vo: 'Snap a receipt, and AI fills in the claim.',
  html: caption('Expenses', 'Snap the receipt. <b>AI fills in the claim.</b>', true) + wm(true) +
    A('up', .25, 'left:404px;top:40px', `<div style="width:230px;height:460px;border-radius:34px;background:#111;padding:10px;box-shadow:0 30px 60px rgba(0,0,0,.5),0 0 0 2px rgba(255,255,255,.08)">
      <div style="position:relative;height:100%;border-radius:26px;background:#2b2b2b;overflow:hidden;display:grid;place-items:center">
        <div style="position:absolute;inset:14px;border:2px solid rgba(255,255,255,.35);border-radius:14px"></div>
        <div style="width:150px;background:#FFFDF7;color:#333;padding:16px 14px;font:11px/1.6 ui-monospace,Menlo,monospace;transform:rotate(-2deg)">
          <div style="text-align:center;font-weight:700;font-size:12px">UNION STREET GRILL</div><div style="text-align:center">Nov 8</div>
          <div style="border-top:1px dashed #bbb;margin:8px 0"></div><div>2x Lunch ..... 72.00</div><div>Drinks ....... 14.40</div>
          <div style="border-top:1px dashed #bbb;margin:8px 0"></div><div style="font-weight:700">TOTAL ....... 86.40</div>
        </div>
        <div class="pv-scan" data-k="scan" style="top:0;opacity:0"></div>
      </div></div>`) +
    A('right', .55, 'left:670px;top:132px;width:250px', `<div class="pv-card" style="padding:18px">
      <div style="display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;color:#6C3845"><span class="pv-spin" style="display:inline-grid">${ico('spark', 24, '#F6EEF0', '#6C3845', 7)}</span>Read by AI</div>
      ${[['Merchant', 'Union Street Grill'], ['Date', 'Nov 8'], ['Amount', '$86.40'], ['Category', 'Meals & entertainment']].map(([a, b], i) => `<div style="margin-top:10px"><div style="font-size:11.5px;color:#6B6470">${a}</div><div class="pv-glow" data-k="f${i}" data-v="${b}" style="font-size:15px;font-weight:700;background:#FBF8F9;border-radius:8px;padding:6px 9px;margin-top:3px;min-height:31px"></div></div>`).join('')}
    </div>`) });

/* 07 · HR AI assistant */
const ANSWER = 'Under your company\'s Leave Policy you get 3 working days of bereavement leave. Want me to start a request?';
S.push({ ch: 1, dur: 6, bg: 'soft', vo: 'Got a policy question? The HR assistant answers from your own policies.',
  html: caption('HR AI assistant', 'Answers from <b>your own policies</b>', false) + wm(false) +
    A('up', .25, 'left:390px;top:66px;width:520px', `<div class="pv-card" style="padding:22px;min-height:330px;display:flex;flex-direction:column;gap:14px">
      ${N('fade', .4, `<div style="display:flex;align-items:center;gap:10px;font-size:15px;font-weight:700">${ico('spark', 32, '#6C3845', '#fff', 10)}HR assistant <span style="margin-left:auto;font-size:12px;font-weight:600;color:#0F8A5F">● Online</span></div>`)}
      ${N('right', .65, `<div style="max-width:78%;margin-left:auto;background:#6C3845;color:#fff;border-radius:16px 16px 4px 16px;padding:12px 15px;font-size:15.5px">How much bereavement leave do I get?</div>`)}
      <div data-k="typing" class="pv-dots" style="display:none;align-self:flex-start;background:#F6EEF0;border-radius:16px;padding:12px 14px"><span></span><span></span><span></span></div>
      <div data-k="ansbox" style="display:none;max-width:88%;background:#F6EEF0;border-radius:16px 16px 16px 4px;padding:13px 15px;font-size:15.5px;line-height:1.45">
        <span data-k="ans"></span>
        ${N('pop', 3.7, `<div style="margin-top:10px;display:inline-flex;align-items:center;gap:6px;font-size:12px;font-weight:600;color:#6B6470;background:#fff;border-radius:999px;padding:4px 10px">${ico('file', 18, 'transparent', '#6C3845', 4)}Source: Leave Policy</div>`)}
      </div>
      ${N('up', 4.0, `<div style="display:flex;gap:8px"><span class="pv-pill pv-glow" data-k="cta" style="background:#6C3845;color:#fff;font-size:13px;padding:8px 14px">Start leave request</span><span class="pv-pill" style="background:#fff;border:1px solid #ECE4E7;color:#1B1620;font-size:13px;padding:8px 14px">Read the policy</span></div>`)}
    </div>`) });

/* 08 · For every team */
S.push({ ch: 2, dur: 7, bg: 'white', vo: 'Built for every team that touches HR: HR, finance, business owners and every employee.',
  html: A('down', 0, 'left:0;top:0;width:960px;height:150px;background:linear-gradient(140deg,#7A4150,#4A2530)', '') +
    A('blur', .2, 'left:56px;top:40px', `<div class="pv-ey" style="font-size:13px;color:#F1DDE2">Solutions</div>`) +
    A('blur', .35, 'left:56px;top:66px;white-space:nowrap;--hl:#F1DDE2', `<div class="pv-h pv-gt" style="font-size:40px;color:#fff">Made for every team <b>that touches HR</b></div>`) +
    A('fade', .2, 'right:28px;top:24px;opacity:.9', brand(15, true)) +
    [['users', 'HR Teams', 'Less admin, one source of truth'], ['pay', 'Finance & Payroll', 'Accurate payroll and spend control'], ['case', 'Business Owners', 'Your workforce at a glance'], ['self', 'Employees & Managers', 'Requests and approvals in one portal']].map(([k, t, d], i) =>
      A('flip', .9 + i * .7, `left:${i % 2 ? 488 : 56}px;top:${i < 2 ? 182 : 322}px;width:416px;height:124px`, `<div style="height:100%;display:flex;align-items:center;gap:20px;background:#fff;border:1px solid #ECE4E7;border-radius:20px;padding:24px;box-shadow:0 14px 34px -16px rgba(46,24,32,.3)">
        <span class="pv-glow" data-k="i${i}" style="border-radius:18px">${ico(k, 64, '#F6EEF0', '#6C3845', 18)}</span>
        <div><div style="font-size:22px;font-weight:800;letter-spacing:-.02em;color:#1B1620">${t}</div><div style="margin-top:4px;font-size:15.5px;color:#6C3845;font-weight:600">${d}</div></div></div>`)).join('') });

/* 09 · One connected platform */
const HUB = [[500, 130, 'users', 'Core HR'], [780, 130, 'cal', 'Leave'], [470, 290, 'receipt', 'Expenses'], [810, 290, 'coins', 'Loans'], [520, 440, 'exit', 'Offboarding'], [760, 440, 'spark', 'AI assistant']];
S.push({ ch: 2, dur: 6, bg: 'dark', vo: 'Start with what you need, and switch on more modules as you grow.',
  html: caption('One connected platform', 'Start with what you need. <b>Add more as you grow.</b>', true) + wm(true) +
    A('fade', .3, 'left:0;top:0;width:960px;height:540px', `<svg width="960" height="540" style="display:block">
      ${HUB.map(([x, y], i) => `<line data-k="l${i}" x1="${x}" y1="${y}" x2="640" y2="290" stroke="rgba(255,255,255,.35)" stroke-width="2"/>`).join('')}
      ${HUB.map((_, i) => `<circle data-k="d${i}" r="5" fill="#F2B8C9" style="filter:drop-shadow(0 0 6px #F2B8C9)" opacity="0"/>`).join('')}
    </svg>`) +
    A('pop', .2, 'left:570px;top:226px;width:140px;height:128px', `<div class="pv-glow" data-k="core" style="height:100%;border-radius:24px;background:#fff;color:#4A2530;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;box-shadow:0 0 0 10px rgba(255,255,255,.08),0 20px 50px rgba(0,0,0,.4)">${ico('pay', 46, '#F6EEF0', '#6C3845', 13)}<div style="font-size:16px;font-weight:800">Payroll</div></div>`) +
    HUB.map(([x, y, k, t], i) => A('pop', .7 + i * .15, `left:${x - 64}px;top:${y - 24}px;width:128px`, `<div class="pv-glow" data-k="m${i}" style="display:flex;align-items:center;gap:8px;background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.22);border-radius:14px;padding:8px 10px;backdrop-filter:blur(4px)">${ico(k, 28, '#fff', '#6C3845', 8)}<span style="font-size:13.5px;font-weight:700;white-space:nowrap">${t}</span></div>`)).join('') });

/* 10 · Book a demo */
S.push({ ch: 3, dur: 6, bg: 'soft', vo: 'See it with your own team\'s data. Book a 30-minute demo.',
  html: wm(false) +
    A('left', .1, 'left:56px;top:96px', `<div class="pv-ey" style="font-size:13px;color:#6C3845">Book a demo</div>`) +
    A('left', .25, 'left:56px;top:124px;width:400px;--hl:#6C3845', `<div class="pv-h" style="font-size:46px;color:#1B1620">See it with <b>your own team's data</b></div>`) +
    A('left', .45, 'left:56px;top:250px;width:390px;font-size:18px;line-height:1.45;color:#6B6470', 'In 30 minutes, we\'ll show you payroll, leave and expenses set up the way your company works.') +
    A('up', .4, 'left:500px;top:80px;width:410px', `<div class="pv-card" style="padding:22px">
      <div style="display:flex;justify-content:space-between;align-items:center"><div style="font-size:17px;font-weight:700">30-minute demo</div><span style="font-size:13px;color:#6B6470">December</span></div>
      <div style="margin-top:14px;display:grid;grid-template-columns:repeat(5,1fr);gap:6px;text-align:center;font-size:12px;color:#6B6470">${['Mon', 'Tue', 'Wed', 'Thu', 'Fri'].map(d => `<span>${d}</span>`).join('')}
        ${Array.from({ length: 10 }, (_, i) => `<span class="pv-glow" data-k="c${i}" style="padding:9px 0;border-radius:9px;font-size:14px;font-weight:600;background:#FBF8F9;color:#1B1620;transition:background .25s,color .25s">${i + 1}</span>`).join('')}
      </div>
      <div style="margin-top:14px;display:grid;grid-template-columns:repeat(3,1fr);gap:8px">${['10:00', '11:30', '14:00'].map((t, i) => `<span class="pv-glow" data-k="t${i}" style="text-align:center;padding:9px 0;border-radius:9px;font-size:14px;font-weight:700;border:1.5px solid #ECE4E7;color:#1B1620;transition:border-color .25s,color .25s">${t}</span>`).join('')}</div>
      <div class="pv-glow" data-k="confirm" style="margin-top:16px;text-align:center;background:#6C3845;color:#fff;border-radius:999px;padding:12px;font-size:15px;font-weight:700;transition:background .3s">Confirm demo</div>
    </div>`) });

/* 11 · End card */
S.push({ ch: 3, dur: 5, bg: 'dark', hold: true, vo: 'HRConnect.AI. The HR app that connects everything.',
  html: A('0,0,.7', .15, 'left:0;width:960px;top:146px;text-align:center', `<span class="pv-glowf" data-k="logo" style="display:inline-block">${brand(52, true)}</span>`) +
    A('blur', .6, 'left:0;width:960px;top:236px;text-align:center;font-size:26px;font-weight:600;color:rgba(255,255,255,.88)', 'The AI-powered HR app that connects everything') +
    A('up', 1.0, 'left:0;width:960px;top:300px;text-align:center', `<span class="pv-shine pv-glow" data-k="cta" style="display:inline-flex;align-items:center;gap:10px;background:#fff;color:#4A2530;border-radius:999px;padding:15px 28px;font-size:20px;font-weight:800">Book a 30-minute demo ${ico('arrow', 22, 'transparent', '#4A2530', 0)}</span>`) +
    A('fade', 1.4, 'left:0;width:960px;top:384px;text-align:center;font-size:19px;font-weight:600;color:rgba(255,255,255,.75)', 'hrconnect.ai/book-a-demo') });

/* ---------- Per-scene effects (driven by local time lt) ---------- */
const FX = [
  null,
  (lt, k) => { // logo: the Neural H builds node by node, then the name types on
    for (let i = 0; i < 4; i++) k['n' + i].style.transform = `scale(${eBack(prog(lt, .1 + i * .1, .45 + i * .1))})`;
    const v = 1 - eIO(prog(lt, .45, .95)), b = 1 - eOut(prog(lt, .85, 1.15));
    k.v0.style.strokeDashoffset = v; k.v1.style.strokeDashoffset = v;
    k.b0.style.strokeDashoffset = b; k.b1.style.strokeDashoffset = b;
    k.c.style.transform = `scale(${eBack(prog(lt, 1.05, 1.4))})`;
    k.h.style.setProperty('--g', pulse(lt, 1.05, 1.1));
    k.word.style.clipPath = `inset(0 ${(1 - eIO(prog(lt, 1.2, 1.95))) * 100}% 0 0)`;
  },
  (lt, k) => { // promise
    for (let i = 0; i < 3; i++) k['c' + i].style.transform = `scaleX(${eOut(prog(lt, 1.45 + i * .28, 1.85 + i * .28))})`;
    k.hot.style.setProperty('--g', lt > 2.4 ? .55 + .45 * Math.sin((lt - 2.4) * 4) : 0);
  },
  (lt, k) => { // payroll
    const c = eOut(prog(lt, .8, 1.9));
    k.k0.textContent = Math.round(48 * c); k.k1.textContent = money(398400 * c); k.k2.textContent = money(301250 * c);
    for (let j = 0; j < 3; j++) flip(k['p' + j], lt >= 2.1 + j * .35, 'Approved', 'Pending', pulse(lt, 2.1 + j * .35, .8));
    flip(k.status, lt >= 3.25, 'Approved · ready to pay', 'In review', pulse(lt, 3.25, 1));
  },
  (lt, k, root, s) => { // leave
    const c = eOut(prog(lt, .75, 1.7));
    k.k0.textContent = (14.5 * c).toFixed(1) + ' days'; k.k1.textContent = Math.round(3 * c) + ' days'; k.k2.textContent = Math.round(5 * c) + ' days';
    const done = lt >= 2.85;
    k.btn.textContent = done ? 'Approved' : 'Approve';
    k.btn.style.background = done ? '#E5F6EF' : '#6C3845'; k.btn.style.color = done ? '#0F8A5F' : '#fff';
    k.btn.style.setProperty('--g', done ? pulse(lt, 2.85, .9) : 0);
    // cursor glides from the bottom right to the Approve button
    const st = root.getBoundingClientRect(), b = k.btn.getBoundingClientRect();
    const tx = (b.left + b.width * .55 - st.left) / s, ty = (b.top + b.height * .6 - st.top) / s;
    const m = eIO(prog(lt, 1.7, 2.6));
    const press = lt > 2.7 && lt < 2.95 ? .85 : 1;
    k.cursor.style.transform = `translate(${880 + (tx - 880) * m}px,${500 + (ty - 500) * m}px) scale(${press})`;
    const r = prog(lt, 2.8, 3.4);
    k.ripple.style.opacity = r > 0 && r < 1 ? 1 - r : 0; k.ripple.style.transform = `scale(${.5 + r * 1.6})`;
  },
  (lt, k) => { // receipt
    const sp = prog(lt, 1.0, 2.2);
    k.scan.style.top = (8 + sp * 84) + '%'; k.scan.style.opacity = sp > 0 && sp < 1 ? 1 : 0;
    for (let i = 0; i < 4; i++) {
      const el = k['f' + i], v = el.dataset.v, p = prog(lt, 1.7 + i * .3, 2.0 + i * .3);
      el.textContent = v.slice(0, Math.round(v.length * p));
      el.style.setProperty('--g', pulse(lt, 1.85 + i * .3, .7));
    }
  },
  (lt, k) => { // assistant
    k.typing.style.display = lt >= 1.15 && lt < 1.9 ? 'block' : 'none';
    k.ansbox.style.display = lt >= 1.9 ? 'block' : 'none';
    const p = prog(lt, 1.95, 3.5), n = Math.round(ANSWER.length * p);
    k.ans.innerHTML = p >= 1 ? ANSWER.replace('3 working days', '<b style="color:#6C3845;font-weight:700">3 working days</b>') : ANSWER.slice(0, n) + (p > 0 ? '<span style="opacity:.5">▍</span>' : '');
    k.cta.style.setProperty('--g', lt > 4.5 ? .5 + .5 * Math.sin((lt - 4.5) * 4) : 0);
  },
  (lt, k) => { for (let i = 0; i < 4; i++) k['i' + i].style.setProperty('--g', pulse(lt, 1.5 + i * .7, 1)); },
  (lt, k) => { // hub
    k.core.style.setProperty('--g', .45 + .4 * Math.sin(lt * 3.2));
    HUB.forEach(([x, y], i) => {
      const len = Math.hypot(640 - x, 290 - y), line = k['l' + i];
      line.style.strokeDasharray = len; line.style.strokeDashoffset = len * (1 - eOut(prog(lt, .6 + i * .12, 1.3 + i * .12)));
      const d = k['d' + i], ph = lt < 1.6 ? -1 : ((lt - 1.6) * .75 + i / 6) % 1;
      d.setAttribute('cx', x + (640 - x) * Math.max(ph, 0)); d.setAttribute('cy', y + (290 - y) * Math.max(ph, 0));
      d.setAttribute('opacity', ph < 0 ? 0 : Math.sin(Math.PI * ph));
      k['m' + i].style.setProperty('--g', ph > .9 ? 0 : pulse(lt, .95 + i * .15, .7));
    });
  },
  (lt, k) => { // demo
    const day = lt >= 1.7, time = lt >= 2.5, booked = lt >= 3.35;
    k.c7.style.background = day ? '#6C3845' : '#FBF8F9'; k.c7.style.color = day ? '#fff' : '#1B1620'; k.c7.style.setProperty('--g', pulse(lt, 1.7, .8));
    k.t1.style.borderColor = time ? '#6C3845' : '#ECE4E7'; k.t1.style.color = time ? '#6C3845' : '#1B1620'; k.t1.style.setProperty('--g', pulse(lt, 2.5, .8));
    k.confirm.style.transform = lt > 3.1 && lt < 3.35 ? 'scale(.96)' : 'scale(1)';
    k.confirm.style.background = booked ? '#0F8A5F' : '#6C3845';
    k.confirm.textContent = booked ? 'Demo booked ✓' : 'Confirm demo';
    k.confirm.style.setProperty('--g', booked ? Math.max(pulse(lt, 3.35, 1), .35) : 0);
  },
  (lt, k) => { // end card
    k.logo.style.setProperty('--g', .5 + .5 * Math.sin(lt * 2.2));
    k.cta.style.setProperty('--g', lt > 1.6 ? .45 + .4 * Math.sin((lt - 1.6) * 3) : 0);
  }
];
function flip(el, on, yes, no, g) {
  el.textContent = on ? yes : no;
  el.classList.toggle('pv-ok', on); el.classList.toggle('pv-pend', !on);
  el.style.setProperty('--g', g);
}

/* ---------- Player ---------- */
let t0 = 0;
S.forEach(s => { s.start = t0; t0 += s.dur; s.end = t0; });
const TOTAL = t0;
const ICON = {
  play: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5.5v13a1 1 0 0 0 1.5.86l10.5-6.5a1 1 0 0 0 0-1.72L9.5 4.64A1 1 0 0 0 8 5.5z"/></svg>',
  pause: '<svg viewBox="0 0 24 24" fill="currentColor"><rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/></svg>',
  replay: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></svg>',
  cc: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><rect x="2" y="5" width="20" height="14" rx="3"/><path d="M10 10.5a2.5 2.5 0 1 0 0 3M17 10.5a2.5 2.5 0 1 0 0 3"/></svg>',
  fs: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M8 3H5a2 2 0 0 0-2 2v3M21 8V5a2 2 0 0 0-2-2h-3M3 16v3a2 2 0 0 0 2 2h3M16 21h3a2 2 0 0 0 2-2v-3"/></svg>'
};

function init(root) {
  const demoHref = root.dataset.demoHref || '/book-a-demo/';
  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  root.tabIndex = 0;
  root.setAttribute('role', 'region');
  root.setAttribute('aria-label', 'HRConnect.AI in 60 seconds, video');
  root.innerHTML = `
    <div class="pv-stage" aria-hidden="true">
      ${['dark', 'soft', 'paper', 'white'].map(b => `<div class="pv-bg ${b}">${b === 'dark' || b === 'soft' ? '<span class="pv-orb" style="left:-120px;top:240px;width:420px;height:420px"></span><span class="pv-orb" style="left:620px;top:-160px;width:460px;height:460px;animation-delay:-6s"></span>' : ''}</div>`).join('')}
      ${S.map(s => `<div class="pv-scene">${s.html}</div>`).join('')}
      <div class="pv-grain"></div>
      <div class="pv-cc"></div>
    </div>
    <div class="pv-ui">
      <button class="pv-big" type="button" aria-label="Play video">${ICON.play}</button>
      <div class="pv-end"><button type="button" data-replay>${ICON.replay.replace('<svg', '<svg width="18" height="18"')}Watch again</button><a href="${demoHref}">Book a demo</a></div>
      <div class="pv-bar">
        <button class="pv-btn" type="button" data-pp aria-label="Play">${ICON.play}</button>
        <span class="pv-time">0:00 / ${fmt(TOTAL)}</span>
        <div class="pv-track">
          <div class="pv-segs">${CHAPTERS.map((c, ci) => { const d = S.filter(s => s.ch === ci).reduce((a, s) => a + s.dur, 0); return `<span class="pv-seg" style="flex:${d}" title="${c}"><i></i></span>`; }).join('')}</div>
          <input class="pv-range" type="range" min="0" max="${TOTAL}" step="0.1" value="0" aria-label="Seek">
          <span class="pv-focus"></span>
        </div>
        <button class="pv-btn" type="button" data-cc aria-label="Captions" aria-pressed="false">${ICON.cc}</button>
        <button class="pv-btn" type="button" data-fs aria-label="Full screen">${ICON.fs}</button>
      </div>
    </div>`;

  const stage = root.querySelector('.pv-stage');
  const bgs = Object.fromEntries([...stage.querySelectorAll('.pv-bg')].map(b => [b.classList[1], b]));
  const scenes = [...stage.querySelectorAll('.pv-scene')].map((el, i) => {
    const els = [...el.querySelectorAll('.pv-a')].map((e, j) => {
      const pre = PRE[e.dataset.a] || {};
      return { el: e, d: +e.dataset.d, od: Math.min(j * .03, .2), i: vec(pre.i, e.dataset.in), o: vec(pre.o, e.dataset.out || (e.dataset.in ? '0,0' : '')), b: pre.b || 0 };
    });
    const k = {}; el.querySelectorAll('[data-k]').forEach(n => k[n.dataset.k] = n);
    return { el, els, k, s: S[i] };
  });
  const cc = stage.querySelector('.pv-cc'), big = root.querySelector('.pv-big'), pp = root.querySelector('[data-pp]'),
        range = root.querySelector('.pv-range'), time = root.querySelector('.pv-time'), fills = [...root.querySelectorAll('.pv-seg i')];
  let scale = 1, t = 0, playing = false, last = 0, raf = 0, cur = -1, userPaused = false, started = false;

  const layout = () => {
    const w = root.clientWidth, h = root.clientHeight;
    scale = Math.min(w / 960, h / 540);
    root.style.setProperty('--pv-s', scale);
    root.style.setProperty('--pv-x', (w - 960 * scale) / 2 + 'px');
    root.style.setProperty('--pv-y', (h - 540 * scale) / 2 + 'px');
    render(t);
  };

  function apply(e, lt, dur, hold) {
    const pin = eOut(clamp((lt - e.d) / IN));
    const pout = hold ? 0 : eIn(clamp((lt - (dur - OUT - GAP - e.od)) / OUT));
    const k = 1 - pin, I = e.i, O = e.o;
    const s = (1 + (I[2] - 1) * k) * (1 + (O[2] - 1) * pout);
    e.el.style.transform = `perspective(900px) translate(${I[0] * k + O[0] * pout}px,${I[1] * k + O[1] * pout}px) scale(${s}) rotate(${I[3] * k + O[3] * pout}deg) rotateX(${I[4] * k + O[4] * pout}deg)`;
    e.el.style.opacity = pin * (1 - pout);
    if (e.b) e.el.style.filter = `blur(${(k + pout) * e.b}px)`;
  }

  function render(time_) {
    const tt = clamp(time_, 0, TOTAL - .001);
    let i = S.findIndex(s => tt < s.end); if (i < 0) i = S.length - 1;
    const sc = scenes[i], s = sc.s, lt = tt - s.start;
    if (i !== cur) { scenes.forEach((x, j) => x.el.classList.toggle('on', j === i)); cur = i; cc.textContent = s.vo; }
    // background crossfade
    const prev = i > 0 ? S[i - 1].bg : s.bg, mix = eIO(prog(lt, 0, .45));
    for (const [name, el] of Object.entries(bgs)) el.style.opacity = name === s.bg ? (prev === s.bg ? 1 : mix) : name === prev ? 1 - mix : 0;
    for (const e of sc.els) apply(e, lt, s.dur, s.hold);
    if (FX[i]) FX[i](lt, sc.k, stage, scale);
    // UI
    const shown = time_;
    time.textContent = `${fmt(shown)} / ${fmt(TOTAL)}`;
    if (document.activeElement !== range) range.value = shown;
    let acc = 0;
    CHAPTERS.forEach((_, ci) => {
      const d = S.filter(x => x.ch === ci).reduce((a, x) => a + x.dur, 0);
      fills[ci].style.width = clamp((shown - acc) / d) * 100 + '%'; acc += d;
    });
    root.dispatchEvent(new CustomEvent('pv:time', { detail: { t: shown, chapter: s.ch } }));
  }

  function loop(now) {
    if (!playing) return;
    t += Math.min((now - last) / 1000, .1); last = now;
    if (t >= TOTAL) { t = TOTAL; render(t); setState('ended'); return; }
    render(t);
    raf = requestAnimationFrame(loop);
  }
  function setState(st) {
    playing = st === 'playing';
    root.classList.toggle('playing', playing);
    root.classList.toggle('paused', st === 'paused');
    root.classList.toggle('ended', st === 'ended');
    pp.innerHTML = playing ? ICON.pause : ICON.play;
    pp.setAttribute('aria-label', playing ? 'Pause' : 'Play');
    big.setAttribute('aria-label', st === 'ended' ? 'Replay video' : 'Play video');
    if (playing) { last = performance.now(); cancelAnimationFrame(raf); raf = requestAnimationFrame(loop); }
  }
  const play = () => { if (t >= TOTAL) t = 0; started = true; setState('playing'); };
  const pause = () => setState(started ? 'paused' : 'idle');
  const toggle = () => { if (playing) { userPaused = true; pause(); } else { userPaused = false; play(); } };
  const seek = v => { t = clamp(v, 0, TOTAL); started = true; if (!playing) setState(t >= TOTAL ? 'ended' : 'paused'); render(t); };

  big.addEventListener('click', () => { userPaused = false; play(); });
  pp.addEventListener('click', toggle);
  root.querySelector('[data-replay]').addEventListener('click', () => { t = 0; userPaused = false; play(); });
  range.addEventListener('input', () => seek(+range.value));
  root.querySelector('[data-cc]').addEventListener('click', e => {
    const on = root.classList.toggle('cc-on'); e.currentTarget.setAttribute('aria-pressed', on);
  });
  root.querySelector('[data-fs]').addEventListener('click', () => {
    if (document.fullscreenElement) document.exitFullscreen(); else root.requestFullscreen?.();
  });
  stage.addEventListener('click', toggle);
  root.addEventListener('keydown', e => {
    if (e.target.closest('a')) return;
    if (e.key === ' ' || e.key === 'k') { e.preventDefault(); toggle(); }
    else if (e.key === 'ArrowRight' && e.target !== range) seek(t + 5);
    else if (e.key === 'ArrowLeft' && e.target !== range) seek(t - 5);
    else if (e.key === 'c') root.querySelector('[data-cc]').click();
    else if (e.key === 'f') root.querySelector('[data-fs]').click();
  });

  new ResizeObserver(layout).observe(root);
  // Autoplay (muted video convention) when half visible, unless the viewer prefers less motion or paused it
  if (!reduced && 'IntersectionObserver' in window) {
    new IntersectionObserver(([en]) => {
      if (en.isIntersecting && en.intersectionRatio >= .5) { if (!userPaused && !playing && t < TOTAL) play(); }
      else if (playing) pause();
    }, { threshold: [0, .5] }).observe(root);
  }
  document.addEventListener('visibilitychange', () => { if (document.hidden && playing) pause(); });

  // Poster: show the promise scene fully built until the video starts
  t = 0; render(S[2].start + 3); time.textContent = `0:00 / ${fmt(TOTAL)}`; range.value = 0; fills.forEach(f => f.style.width = 0);
  setState('idle');

  return {
    play: () => { userPaused = false; play(); },
    pause: () => { userPaused = true; pause(); },
    seek, get time() { return t; }, duration: TOTAL,
    chapters: CHAPTERS.map((c, ci) => ({ title: c, start: S.find(s => s.ch === ci).start }))
  };
}

window.HRCPromoVideo = { init, scenes: S, chapters: CHAPTERS };
function chapters(el) {
  const box = el.parentElement && el.parentElement.querySelector('.pv-chapters');
  if (!box) return;
  box.innerHTML = el.pv.chapters.map((c, i) => `<button type="button" data-i="${i}">${c.title} <small>${fmt(c.start)}</small></button>`).join('');
  const btns = [...box.children];
  box.addEventListener('click', e => { const b = e.target.closest('button'); if (!b) return; el.pv.seek(el.pv.chapters[+b.dataset.i].start); el.pv.play(); });
  el.addEventListener('pv:time', e => btns.forEach((b, i) => b.setAttribute('aria-current', i === e.detail.chapter)));
}
document.querySelectorAll('.pv[data-auto]').forEach(el => { el.pv = init(el); chapters(el); });
})();
