<script setup>
import { ref, computed, onUnmounted } from 'vue'

const screen = ref('home')
const seconds = ref(0)
const running = ref(false)
const reducedMotion = ref(false)
const sessionId = ref(null)
const saveError = ref('')
const history = ref([])
const input = ref('')
const conversationId = ref(null)
const messages = ref([])
const chatBusy = ref(false)
const chatMode = ref('')
let interval = null
let lastTick = 0
const phase = computed(() => seconds.value % 10 < 4 ? 'Breathe in' : 'Breathe out')
const phaseRemaining = computed(() => seconds.value % 10 < 4 ? 4 - seconds.value % 10 : 10 - seconds.value % 10)
const api = async (path, options = {}) => {
  const r = await fetch('/api' + path, { headers: { 'Content-Type': 'application/json' }, ...options })
  if (!r.ok) throw new Error('Request failed (' + r.status + ')')
  return r.json()
}
function clearTimer() { if (interval) clearInterval(interval); interval = null; running.value = false }
async function start() {
  clearTimer(); seconds.value = 0; sessionId.value = null; saveError.value = ''
  screen.value = 'exercise'
  try { sessionId.value = (await api('/sessions', { method: 'POST' })).id }
  catch { saveError.value = 'Could not start a saved session. Exercise is still available.' }
  resume()
}
function resume() {
  if (running.value || seconds.value >= 60) return
  running.value = true; lastTick = performance.now()
  interval = setInterval(() => {
    const now = performance.now()
    const elapsed = Math.floor((now - lastTick) / 1000)
    if (elapsed > 0) {
      seconds.value = Math.min(60, seconds.value + elapsed)
      lastTick += elapsed * 1000
      if (seconds.value >= 60) finish('completed')
    }
  }, 100)
}
function pause() { clearTimer() }
async function finish(status) {
  clearTimer(); screen.value = status === 'completed' ? 'finished' : 'home'
  if (sessionId.value) {
    try {
      await api('/sessions/' + sessionId.value, {
        method: 'PATCH', body: JSON.stringify({ status, guided_seconds: seconds.value })
      })
    } catch { saveError.value = 'Session could not be saved. Please check the backend.' }
  }
}
async function showHistory() {
  screen.value = 'history'; saveError.value = ''
  try { history.value = await api('/sessions') }
  catch { saveError.value = 'History unavailable. Check the backend connection.' }
}
async function sendChat() {
  const msg = input.value.trim()
  if (!msg || chatBusy.value) return
  input.value = ''; messages.value.push({ role: 'user', content: msg }); chatBusy.value = true
  try {
    const result = await api('/chat', { method: 'POST', body: JSON.stringify({ message: msg, conversation_id: conversationId.value }) })
    conversationId.value = result.conversation_id; chatMode.value = result.mode
    messages.value.push({ role: 'assistant', content: result.reply })
  } catch {
    chatMode.value = 'error'
    messages.value.push({ role: 'assistant', content: 'Chat unavailable. Breathing and Crisis Support remain accessible.' })
  } finally { chatBusy.value = false }
}
function openCrisis() { screen.value = 'crisis' }
function back() { screen.value = 'home' }
onUnmounted(clearTimer)
</script>

<template>
  <main>
    <header><h1>Mindful Minute</h1><button class="support" @click="openCrisis">Crisis Support</button></header>
    <p class="disclaimer">Coursework skills prototype only. Not therapy, diagnosis, or monitored support. Test with fictional scenarios only.</p>
    <section v-if="screen === 'home'" class="panel">
      <h2>One minute of paced breathing</h2>
      <p>Inhale for four seconds and exhale for six seconds. You can stop at any time.</p>
      <button @click="start">Start breathing</button>
      <button class="secondary" @click="showHistory">Session history</button>
      <button class="secondary" @click="screen = 'chat'">Optional AI chat</button>
    </section>
    <section v-else-if="screen === 'exercise'" class="panel center">
      <h2>{{ running ? phase : 'Paused' }}</h2>
      <div class="orb" :class="{ expand: running && phase === 'Breathe in', still: reducedMotion || !running }" aria-hidden="true"></div>
      <p v-if="running">Change in {{ phaseRemaining }} seconds</p>
      <p class="timer">{{ seconds }} / 60 seconds</p>
      <label><input type="checkbox" v-model="reducedMotion" /> Reduce motion</label>
      <div class="actions">
        <button v-if="running" @click="pause">Pause</button>
        <button v-else @click="resume">Resume</button>
        <button class="secondary" @click="finish('interrupted')">Exit without penalty</button>
      </div>
    </section>
    <section v-else-if="screen === 'finished'" class="panel">
      <h2>Exercise finished</h2><p>You can repeat it or leave.</p>
      <button @click="start">Repeat</button><button class="secondary" @click="back">Home</button>
    </section>
    <section v-else-if="screen === 'history'" class="panel">
      <h2>Session history</h2>
      <p v-if="!history.length">No saved sessions yet.</p>
      <ul><li v-for="s in history" :key="s.id">{{ new Date(s.started_at).toLocaleString() }} — {{ s.skill }} — {{ s.status }} ({{ s.guided_seconds }}s)</li></ul>
      <button @click="back">Home</button>
    </section>
    <section v-else-if="screen === 'chat'" class="panel">
      <h2>Optional AI chat</h2>
      <p>Not a counselor or emergency service. No personal information is needed.</p>
      <div v-for="(m,i) in messages" :key="i" class="message"><strong>{{ m.role }}:</strong> {{ m.content }}</div>
      <p v-if="chatMode === 'fallback'">Live AI not configured; showing a saved fallback response.</p>
      <form @submit.prevent="sendChat"><input v-model="input" maxlength="500" placeholder="Try a fictional scenario" aria-label="Chat message" /><button :disabled="chatBusy">Send</button></form>
      <button class="secondary" @click="back">Home</button>
    </section>
    <section v-else-if="screen === 'crisis'" class="panel">
      <h2>Crisis Support Information</h2>
      <p>This prototype does not provide emergency support or monitor messages.</p>
      <p>In the United States, call or text <a href="tel:988">988</a> for the Suicide & Crisis Lifeline. For immediate danger, call <a href="tel:911">911</a>. Outside the US, contact local emergency or crisis services.</p>
      <button @click="back">Return home</button>
      <button v-if="sessionId !== null && seconds < 60" class="secondary" @click="screen = 'exercise'">Return to exercise</button>
    </section>
    <p v-if="saveError" role="alert">{{ saveError }}</p>
  </main>
</template>

<style>
*{box-sizing:border-box}body{margin:0;background:#f4f7f6;color:#203b3b;font-family:system-ui,Arial,sans-serif}main{max-width:720px;margin:0 auto;padding:24px}header{display:flex;justify-content:space-between;align-items:center;gap:16px}h1{font-size:1.6rem}h2{font-size:1.45rem}.disclaimer{font-size:.85rem;color:#536c69}.panel{background:white;border:1px solid #dce7e4;border-radius:18px;padding:28px;margin-top:28px;box-shadow:0 4px 20px #143d3910}.center{text-align:center}button{background:#246c65;color:white;border:0;border-radius:9px;padding:12px 16px;cursor:pointer;margin:6px 8px 6px 0;font:inherit}button.secondary{background:#e4efed;color:#214e49}button.support{background:#fff;color:#195e58;border:2px solid #195e58;font-weight:650}button:focus-visible,a:focus-visible{outline:3px solid #c27d26}button:disabled{opacity:.5}.orb{width:140px;height:140px;border-radius:50%;background:#8dbbb4;margin:25px auto;transform:scale(.75);transition:transform 4s ease-in-out}.orb.expand{transform:scale(1.2);transition-duration:4s}.orb.still{transition:none;transform:scale(.9)}.timer{font-weight:700;font-size:1.25rem}.actions{margin-top:18px}.message{padding:10px;border-bottom:1px solid #e5eeec;overflow-wrap:anywhere}form{display:flex;gap:8px;flex-wrap:wrap;margin:14px 0}form input{flex:1;min-width:200px;padding:10px;border:1px solid #9eafac;border-radius:8px}li{margin-bottom:10px}@media(prefers-reduced-motion:reduce){.orb{transition:none!important}}
</style>