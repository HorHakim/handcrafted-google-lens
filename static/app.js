const input = document.getElementById('image-input');
const preview = document.getElementById('preview-image');
const previewContainer = document.getElementById('preview-container');
const analyzeBtn = document.getElementById('analyze-btn');
const clearBtn = document.getElementById('clear-btn');
const uploadLabel = document.getElementById('upload-label');
const resultContainer = document.getElementById('result-container');

input.addEventListener('change', () => {
  const file = input.files[0];
  if (!file) return;

  const url = URL.createObjectURL(file);
  preview.src = url;
  preview.onload = () => URL.revokeObjectURL(url);

  previewContainer.hidden = false;
  analyzeBtn.disabled = false;
  uploadLabel.classList.add('has-image');
});

clearBtn.addEventListener('click', resetForm);

function resetForm() {
  input.value = '';
  preview.src = '';
  previewContainer.hidden = true;
  analyzeBtn.disabled = true;
  uploadLabel.classList.remove('has-image');
  resultContainer.innerHTML = '';
  resultContainer.hidden = true;
}

// HTMX ne swape pas le contenu sur les réponses 4xx/5xx par défaut
document.body.addEventListener('htmx:responseError', (evt) => {
  const fragment = evt.detail.xhr.responseText;
  resultContainer.innerHTML = fragment;
  resultContainer.hidden = false;
  resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
});

// Faire défiler jusqu'au résultat après un swap réussi
document.body.addEventListener('htmx:afterSwap', (evt) => {
  if (evt.detail.target.id === 'result-container') {
    resultContainer.hidden = false;
    resultContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
});
