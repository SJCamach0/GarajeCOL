// GarajeCOL AI Traffic Code Chatbot (Ley 769 / MinTransporte Colombia)

document.addEventListener('DOMContentLoaded', () => {
  setupChatbot();
});

function setupChatbot() {
  const openBtn = document.getElementById('openChatbotBtn');
  const closeBtn = document.getElementById('closeChatbotBtn');
  const drawer = document.getElementById('chatbotDrawer');
  const form = document.getElementById('chatForm');
  const input = document.getElementById('chatInput');
  const messagesBox = document.getElementById('chatMessages');

  if (!drawer || !openBtn) return;

  openBtn.addEventListener('click', () => {
    drawer.classList.remove('translate-x-full');
    if (input) input.focus();
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      drawer.classList.add('translate-x-full');
    });
  }

  // Quick prompt buttons
  document.querySelectorAll('.quick-prompt-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.textContent.trim();
      if (input) input.value = text;
      handleSendMessage(text);
    });
  });

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const text = input.value.trim();
      if (!text) return;
      input.value = '';
      handleSendMessage(text);
    });
  }

  async function handleSendMessage(userText) {
    // 1. Append user message
    appendMessage('user', userText);

    // 2. Typing indicator
    const typingId = 'typing_' + Date.now();
    const typingEl = document.createElement('div');
    typingEl.id = typingId;
    typingEl.className = 'flex gap-2.5 items-start text-xs';
    typingEl.innerHTML = `
      <div class="w-6 h-6 rounded bg-limeBrand text-black flex-shrink-0 flex items-center justify-center text-[10px] font-bold">G</div>
      <div class="bg-[#1c1e26] border border-neutral-700/60 rounded-xl p-3 text-neutral-400">
        <i class="fa-solid fa-circle-notch fa-spin text-limeBrand mr-1.5"></i> Consultando Código Nacional de Tránsito y MinTransporte...
      </div>
    `;
    messagesBox.appendChild(typingEl);
    messagesBox.scrollTop = messagesBox.scrollHeight;

    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userText })
      });
      const data = await res.json();

      // Remove typing indicator
      const currentTyping = document.getElementById(typingId);
      if (currentTyping) currentTyping.remove();

      // Format response text (Markdown simple bold & bullets)
      let formatted = data.reply || 'Sin respuesta';
      formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
      formatted = formatted.replace(/\n/g, '<br>');

      // Build bot message bubble
      appendMessage('bot', formatted, data.official_source);

    } catch (err) {
      console.error(err);
      const currentTyping = document.getElementById(typingId);
      if (currentTyping) currentTyping.remove();
      appendMessage('bot', 'Hubo un error de conexión con la base de datos de normas de tránsito.');
    }
  }

  function appendMessage(sender, htmlContent, source = null) {
    const row = document.createElement('div');
    row.className = sender === 'user' ? 'flex justify-end' : 'flex gap-2.5 items-start';

    if (sender === 'user') {
      row.innerHTML = `
        <div class="bg-limeBrand text-black font-semibold rounded-xl px-3.5 py-2.5 max-w-[85%] leading-relaxed shadow-sm">
          ${htmlContent}
        </div>
      `;
    } else {
      let sourceBadge = '';
      if (source) {
        sourceBadge = `
          <div class="mt-3 pt-2.5 border-t border-neutral-700/80 flex items-center justify-between text-[10px] text-neutral-400">
            <span><i class="fa-solid fa-landmark text-limeBrand mr-1"></i> ${source.norm || source.name}</span>
            <a href="${source.url}" target="_blank" rel="noopener noreferrer" class="text-limeBrand font-bold hover:underline">
              Portal Oficial <i class="fa-solid fa-arrow-up-right-from-square text-[9px]"></i>
            </a>
          </div>
        `;
      }

      row.innerHTML = `
        <div class="w-6 h-6 rounded bg-limeBrand text-black flex-shrink-0 flex items-center justify-center text-[10px] font-bold">
          G
        </div>
        <div class="bg-[#1c1e26] border border-neutral-700/60 rounded-xl p-3.5 text-neutral-200 leading-relaxed max-w-[88%] shadow-sm">
          <div>${htmlContent}</div>
          ${sourceBadge}
        </div>
      `;
    }

    messagesBox.appendChild(row);
    messagesBox.scrollTop = messagesBox.scrollHeight;
  }
}
