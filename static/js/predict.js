const predictionForm = document.getElementById('prediction-form');
const predictionInput = document.getElementById('symptoms-input');
const predictionResult = document.getElementById('prediction-result');

function getRiskColor(riskLevel) {
  const colors = {
    'Low': '#10b981',
    'Medium': '#f59e0b',
    'High': '#ef4444',
  };
  return colors[riskLevel] || '#6b7280';
}

function getSeverityIcon(severity) {
  const icons = {
    'Mild': '🟢',
    'Mild-Moderate': '🟡',
    'Moderate': '🟡',
    'Moderate-Severe': '🟠',
    'Severe': '🔴',
  };
  return icons[severity] || '⚪';
}

function renderPredictions(data) {
  const symptomsText = data.input_symptoms.join(', ') || 'None detected';
  
  let html = `
    <div class="predictions-container">
      <div class="symptoms-info glass-card">
        <p class="info-label">📋 Analyzed Symptoms:</p>
        <p class="symptoms-text">${symptomsText}</p>
        ${data.confidence_note ? `<p class="confidence-note" style="margin-top: 10px; color: #6b7280; font-size: 0.9em;">ℹ️ ${data.confidence_note}</p>` : ''}
      </div>
  `;

  if (data.urgency_level) {
    html += `
      <div class="urgency-info glass-card" style="background-color: rgba(239, 68, 68, 0.1); border-left: 4px solid #ef4444;">
        <p style="margin: 0;">${data.urgency_level}</p>
      </div>
    `;
  }
  
  data.predictions.forEach((prediction, index) => {
    const riskColor = getRiskColor(prediction.risk_level);
    const severityIcon = getSeverityIcon(prediction.severity);
    const matchedCount = prediction.matched_symptoms.length;
    
    html += `
      <div class="result-card glass-card prediction-rank-${index + 1}">
        <div class="rank-header" style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px;">
          <div>
            <span class="rank-badge">#${prediction.rank}</span>
            <span style="margin-left: 10px; font-weight: 300; color: #9ca3af;">${prediction.category}</span>
          </div>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span class="risk-badge" style="background-color: ${riskColor}; padding: 4px 12px; border-radius: 4px; font-size: 0.85em;">
              Risk: ${prediction.risk_level}
            </span>
            <span style="padding: 4px 12px; background-color: rgba(99, 102, 241, 0.1); border-radius: 4px; font-size: 0.9em;">
              ${severityIcon} ${prediction.severity}
            </span>
            <span class="confidence-score" style="padding: 4px 12px; background-color: rgba(99, 102, 241, 0.2); border-radius: 4px;">${prediction.confidence}%</span>
          </div>
        </div>
        
        <h3 class="disease-name" style="margin: 12px 0 8px 0; color: #1f2937; font-size: 1.25em;">${prediction.disease}</h3>
        
        <div class="prediction-details">
          <div style="background-color: rgba(99, 102, 241, 0.05); padding: 12px; border-radius: 6px; margin-bottom: 12px;">
            <p style="margin: 0 0 6px 0;">
              <strong>🔬 Medical Analysis:</strong>
            </p>
            <p style="margin: 0; color: #374151; line-height: 1.6; font-size: 0.95em;">
              ${prediction.medical_reasoning}
            </p>
          </div>

          <p style="margin: 8px 0;"><strong>✓ Matched Symptoms:</strong> <span style="color: #10b981;">${matchedCount > 0 ? prediction.matched_symptoms.join(', ') : 'No specific matches'}</span></p>
          
          ${prediction.unmatched_primary_symptoms && prediction.unmatched_primary_symptoms.length > 0 ? `
            <p style="margin: 8px 0;"><strong>? Additional supporting symptoms:</strong> <span style="color: #6b7280; font-size: 0.9em;">${prediction.unmatched_primary_symptoms.join(', ')}</span></p>
          ` : ''}
          
          <div style="background-color: rgba(34, 197, 94, 0.05); padding: 12px; border-radius: 6px; margin: 12px 0; border-left: 4px solid #22c55e;">
            <p style="margin: 0 0 6px 0; color: #15803d;">
              <strong>💊 Recommendations:</strong>
            </p>
            <p style="margin: 0; color: #374151; line-height: 1.6; font-size: 0.95em;">
              ${prediction.recommendations}
            </p>
          </div>
        </div>
      </div>
    `;
  });
  
  html += `</div>`;
  predictionResult.innerHTML = html;
}

predictionForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  predictionResult.innerHTML = '<div class="result-card glass-card"><p style="text-align: center;">⏳ Analyzing symptoms...</p></div>';
  const prompt = predictionInput.value.trim();

  if (!prompt) {
    predictionResult.innerHTML = '<div class="result-card glass-card error-message"><p>❌ Please enter at least one symptom.</p></div>';
    return;
  }

  try {
    const response = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ text: prompt }),
    });

    const data = await response.json();
    
    if (!response.ok || data.error) {
      const errorMsg = data.message || data.error || 'Unable to predict disease. Please try again with more specific symptoms.';
      predictionResult.innerHTML = `<div class="result-card glass-card error-message" style="border-left: 4px solid #ef4444; padding-left: 12px;"><p>❌ ${errorMsg}</p></div>`;
      return;
    }

    renderPredictions(data);
    predictionInput.value = '';
  } catch (err) {
    console.error('Error:', err);
    predictionResult.innerHTML = `<div class="result-card glass-card error-message"><p>❌ Network error. Please try again.</p></div>`;
  }
});
