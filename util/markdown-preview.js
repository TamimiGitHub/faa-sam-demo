// Function to add copy buttons to code blocks
function addCopyButtons() {
  document.querySelectorAll('pre code').forEach((block) => {
    // Skip if button already exists
    if (block.parentElement.querySelector('.copy-button')) {
      return;
    }
    
    const button = document.createElement('button');
    button.textContent = 'Copy';
    button.className = 'copy-button';
    button.setAttribute('aria-label', 'Copy code to clipboard');
    
    button.onclick = async () => {
      try {
        await navigator.clipboard.writeText(block.textContent);
        button.textContent = 'Copied!';
        button.classList.add('copied');
        setTimeout(() => {
          button.textContent = 'Copy';
          button.classList.remove('copied');
        }, 2000);
      } catch (err) {
        console.error('Failed to copy:', err);
        button.textContent = 'Failed';
        setTimeout(() => button.textContent = 'Copy', 2000);
      }
    };
    
    block.parentElement.style.position = 'relative';
    block.parentElement.appendChild(button);
  });
}

// Run on initial load
document.addEventListener('DOMContentLoaded', addCopyButtons);

// Re-run when content updates (for dynamic content)
const observer = new MutationObserver((mutations) => {
  addCopyButtons();
});

// Observe document for changes
if (document.body) {
  observer.observe(document.body, {
    childList: true,
    subtree: true
  });
}