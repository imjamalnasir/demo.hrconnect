/* Background music for the HRConnect.AI promo video (research/promo-video.html only).

   Source and license: an original composition made for HRConnect.AI and synthesised live in the
   browser with the Web Audio API. It uses no audio files, samples or third-party music, so there
   is nothing to license and it can be used commercially.

   Track: light, uplifting, about 96 BPM in C major, C-G-Am-F (one bar each), 24 bars = 60 seconds.
   A soft pad, a sine bass, a bell arpeggio from bar 3, a light shaker from bar 9, and a held C chord
   on the end card. The music follows the video's own clock (root.pv.time), so it pauses, seeks and
   restarts with the video. Browsers block audio until the viewer interacts, so it starts on the
   first click or key press in the player (Play, the sound button, a chapter, and so on).

   This file doesn't change assets/js/promo-video.js, which the public home page also uses. */
(() => {
'use strict';

const AC = window.AudioContext || window.webkitAudioContext;
const root = document.querySelector('.pv[data-auto]');
if (!AC || !root || !root.pv) return;

/* ---------- Composition ---------- */
const BPM = 96, EIGHTH = 60 / BPM / 2, STEPS = 192; // 24 bars x 8 eighths = 60 s
const VOLUME = 0.32;                                // master level when audible (kept low)
const CHORDS = [ // pad voicing, bass root, arpeggio tones
  { pad: [60, 64, 67], bass: 36, arp: [72, 76, 79, 84] }, // C
  { pad: [59, 62, 67], bass: 43, arp: [71, 74, 79, 83] }, // G
  { pad: [57, 60, 64], bass: 45, arp: [69, 72, 76, 81] }, // Am
  { pad: [57, 60, 65], bass: 41, arp: [69, 72, 77, 81] }  // F
];
const ARP = [0, 1, 2, 1, 3, 2, 1, 2];
const END_BAR = 22; // the end card: one held C chord
const mtof = m => 440 * Math.pow(2, (m - 69) / 12);

/* ---------- State ---------- */
let ctx = null, master, bus, delaySend, analyser, noise;
let unlocked = false, muted = false, running = false, timer = 0, stopTimer = 0;
let anchorVt = 0, anchorCt = 0, nextStep = 0, scheduled = 0;

function ensureCtx() {
  if (ctx) { if (ctx.state === 'suspended' && running) ctx.resume(); return; }
  ctx = new AC();
  master = ctx.createGain(); master.gain.value = 0;
  analyser = ctx.createAnalyser(); analyser.fftSize = 1024;
  const comp = ctx.createDynamicsCompressor();
  master.connect(comp).connect(analyser).connect(ctx.destination);
  // gentle feedback delay for space
  const delay = ctx.createDelay(1), fb = ctx.createGain(), wet = ctx.createGain(), tone = ctx.createBiquadFilter();
  delay.delayTime.value = EIGHTH * 3; fb.gain.value = .32; wet.gain.value = .35;
  tone.type = 'lowpass'; tone.frequency.value = 2600;
  delaySend = ctx.createGain();
  delaySend.connect(delay); delay.connect(tone).connect(fb).connect(delay); tone.connect(wet).connect(master);
  // one second of noise for the shaker
  noise = ctx.createBuffer(1, ctx.sampleRate, ctx.sampleRate);
  const d = noise.getChannelData(0); for (let i = 0; i < d.length; i++) d[i] = Math.random() * 2 - 1;
  newBus();
}

/* Every jump in time gets a fresh bus, so notes already scheduled can be faded out together. */
function newBus() {
  if (bus) {
    const old = bus, n = ctx.currentTime;
    old.gain.cancelScheduledValues(n); old.gain.setValueAtTime(old.gain.value, n); old.gain.linearRampToValueAtTime(0, n + .12);
    setTimeout(() => old.disconnect(), 400);
  }
  bus = ctx.createGain(); bus.connect(master);
}

/* ---------- Instruments ---------- */
function env(g, t, peak, a, len, r) {
  g.gain.setValueAtTime(0, t);
  g.gain.linearRampToValueAtTime(peak, t + a);
  g.gain.setValueAtTime(peak, t + len);
  g.gain.linearRampToValueAtTime(0, t + len + r);
}
function pad(notes, t, len) {
  const lp = ctx.createBiquadFilter(); lp.type = 'lowpass'; lp.frequency.value = 1150; lp.Q.value = .4;
  const g = ctx.createGain(); env(g, t, .05, .6, len, 1.0);
  lp.connect(g).connect(bus);
  notes.forEach(m => [-6, 6].forEach(cents => {
    const o = ctx.createOscillator(); o.type = 'triangle'; o.frequency.value = mtof(m); o.detune.value = cents;
    o.connect(lp); o.start(t); o.stop(t + len + 1.1);
  }));
}
function bass(m, t, len = .55, peak = .2) {
  const o = ctx.createOscillator(), g = ctx.createGain();
  o.type = 'sine'; o.frequency.value = mtof(m);
  g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + .02); g.gain.exponentialRampToValueAtTime(.001, t + len);
  o.connect(g).connect(bus); o.start(t); o.stop(t + len + .05);
}
function bell(m, t, peak = .06) {
  const g = ctx.createGain();
  g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(peak, t + .008); g.gain.exponentialRampToValueAtTime(.0008, t + .9);
  g.connect(bus); g.connect(delaySend);
  [[1, 1], [3, .12]].forEach(([mul, lvl]) => {
    const o = ctx.createOscillator(), og = ctx.createGain();
    o.type = 'sine'; o.frequency.value = mtof(m) * mul; og.gain.value = lvl;
    o.connect(og).connect(g); o.start(t); o.stop(t + .95);
  });
}
function shaker(t, peak) {
  const s = ctx.createBufferSource(), hp = ctx.createBiquadFilter(), g = ctx.createGain();
  s.buffer = noise; hp.type = 'highpass'; hp.frequency.value = 7000;
  g.gain.setValueAtTime(peak, t); g.gain.exponentialRampToValueAtTime(.0005, t + .07);
  s.connect(hp).connect(g).connect(bus); s.start(t, Math.random() * .8, .09);
}

/* One eighth-note step of the score, played at audio time t */
function step(s, t) {
  const bar = Math.floor(s / 8), pos = s % 8;
  if (bar >= END_BAR) {
    if (s === END_BAR * 8) { // end card: held C chord, a bell flourish, low C
      pad([60, 64, 67, 72], t, 3.6); bass(36, t, 3.5, .16);
      [72, 76, 79, 84].forEach((m, i) => bell(m, t + i * EIGHTH, .05));
    }
    return;
  }
  const c = CHORDS[bar % 4];
  if (pos === 0) pad(c.pad, t, EIGHTH * 8 - .3);
  if (pos === 0 || pos === 4) bass(c.bass, t);
  if (bar >= 2) bell(c.arp[ARP[pos]], t, pos === 0 ? .065 : .045);
  if (bar >= 8 && bar < 21 && pos % 2) shaker(t, pos === 3 || pos === 7 ? .045 : .028);
}

/* ---------- Scheduler, driven by the video's clock ---------- */
const videoNow = () => anchorVt + (ctx.currentTime - anchorCt);
function anchor(vt) {
  anchorVt = vt; anchorCt = ctx.currentTime;
  nextStep = Math.ceil(vt / EIGHTH - 1e-6);
  // landing mid-bar: bring the bar's pad and bass in straight away
  const s = Math.floor(vt / EIGHTH), bar = Math.floor(s / 8);
  if (bar < END_BAR && s % 8 !== 0 && vt > 0) {
    const c = CHORDS[bar % 4], left = (bar + 1) * 8 * EIGHTH - vt;
    if (left > .4) { pad(c.pad, ctx.currentTime + .02, left - .3); bass(c.bass, ctx.currentTime + .02); }
  }
}
function tick() {
  const vt = root.pv.time;
  if (Math.abs(vt - videoNow()) > .25) { newBus(); anchor(vt); } // seek, chapter or a stalled frame
  const horizon = videoNow() + .15;
  while (nextStep < STEPS && nextStep * EIGHTH < horizon) {
    const t = anchorCt + (nextStep * EIGHTH - anchorVt);
    step(nextStep, Math.max(t, ctx.currentTime + .005));
    nextStep++; scheduled++;
  }
}

function ramp(to, secs) {
  const n = ctx.currentTime;
  master.gain.cancelScheduledValues(n); master.gain.setValueAtTime(master.gain.value, n);
  master.gain.linearRampToValueAtTime(to, n + secs);
}
const audible = () => unlocked && !muted;

function start() {
  if (!audible()) return;
  clearTimeout(stopTimer);
  ctx.resume();
  if (!running) { newBus(); anchor(root.pv.time); running = true; timer = setInterval(tick, 25); tick(); }
  ramp(VOLUME, .5);
}
function stop(fade, suspend = true) {
  if (!ctx) return;
  running = false; clearInterval(timer);
  ramp(0, fade);
  clearTimeout(stopTimer);
  if (suspend) stopTimer = setTimeout(() => { if (!running) ctx.suspend(); }, fade * 1000 + 150);
}
const isPlaying = () => root.classList.contains('playing');

function sync() {
  if (isPlaying()) { if (audible()) start(); else if (running) stop(.15); }
  else if (root.classList.contains('ended')) stop(2);
  else stop(.15);
  paint();
}
new MutationObserver(sync).observe(root, { attributes: true, attributeFilter: ['class'] });

/* ---------- Sound button and unlocking ---------- */
const ICON_ON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="M15.5 8.5a5 5 0 0 1 0 7M19 5a10 10 0 0 1 0 14"/></svg>';
const ICON_OFF = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 5 6 9H2v6h4l5 4V5z"/><path d="m22 9-6 6M16 9l6 6"/></svg>';
const btn = document.createElement('button');
btn.type = 'button'; btn.className = 'pv-btn'; btn.dataset.snd = '';
const bar = root.querySelector('.pv-bar');
bar.insertBefore(btn, bar.querySelector('[data-cc]'));
function paint() {
  const on = audible();
  btn.innerHTML = on ? ICON_ON : ICON_OFF;
  btn.setAttribute('aria-pressed', String(!on));
  btn.setAttribute('aria-label', on ? 'Mute music' : 'Turn music on');
  btn.title = on ? 'Mute music (m)' : 'Turn music on (m)';
}
function unlock() { ensureCtx(); unlocked = true; }
function toggleSound() {
  if (!unlocked) { unlock(); muted = false; } else muted = !muted;
  sync();
}
btn.addEventListener('click', e => { e.stopPropagation(); toggleSound(); });

// Any other gesture in the player (or a chapter button) unlocks audio, unless the viewer muted it.
// If the video is autoplaying silently, the first click on the picture turns the sound on instead of pausing.
let swallowClick = false;
const gesture = e => {
  if (e.target.closest && e.target.closest('[data-snd]')) return;
  if (!unlocked && !muted) {
    swallowClick = e.type === 'pointerdown' && isPlaying() && !!e.target.closest('.pv-stage');
    unlock(); sync();
  }
};
root.addEventListener('pointerdown', gesture, true);
root.addEventListener('click', e => { if (swallowClick) { swallowClick = false; e.stopPropagation(); } }, true);
root.addEventListener('keydown', e => {
  if (e.key === 'm' && !e.metaKey && !e.ctrlKey && !e.altKey) { toggleSound(); return; }
  gesture(e);
}, true);
const chapters = root.parentElement && root.parentElement.querySelector('.pv-chapters');
if (chapters) chapters.addEventListener('pointerdown', gesture, true);

paint();

// For debugging in the console: document.querySelector('.pv').pvMusic
root.pvMusic = {
  get state() { return { ctx: ctx ? ctx.state : 'none', unlocked, muted, running, gain: ctx ? +master.gain.value.toFixed(3) : 0, nextStep, scheduled }; },
  level() { if (!analyser) return 0; const a = new Float32Array(analyser.fftSize); analyser.getFloatTimeDomainData(a); return Math.sqrt(a.reduce((s, v) => s + v * v, 0) / a.length); }
};
})();
