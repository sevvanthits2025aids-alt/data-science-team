const vaccineForm = document.getElementById('vaccine-form');
const diseaseInput = document.getElementById('disease-input');
const vaccineResult = document.getElementById('vaccine-result');

function renderVaccineInfo(data) {
  // If vaccine is not available
  if (data.available === false) {
    let html = `
      <div class="result-card glass-card vaccine-unavailable">
        <div class="vaccine-info-structured">
          <div class="info-block">
            <span class="label">Disease:</span>
            <span class="value">${data.disease}</span>
          </div>
          
          <div class="info-block">
            <span class="label">Vaccine Status:</span>
            <span class="value status-badge">⚠️ ${data.vaccine_status || 'Not Available'}</span>
          </div>
          
          <div class="info-block reason-section">
            <span class="label">Reason:</span>
            <div class="reason-content">
              <p class="reason-statement"><strong>${data.reason_unavailable}</strong></p>
              <p class="scientific-explanation">${data.scientific_reason}</p>
    `;
    
    if (data.alternative) {
      html += `<p class="alternative-section"><strong>Alternative Prevention/Management:</strong> ${data.alternative}</p>`;
    }
    
    html += `
            </div>
          </div>
        </div>
      </div>
    `;
    return html;
  }
  
  // If vaccine is available
  if (data.available) {
    return `
      <div class="result-card glass-card vaccine-available">
        <h3>${data.disease}</h3>
        <p class="available-badge">✅ Vaccine Available</p>
        
        <div class="vaccine-details">
          <div class="detail-row">
            <strong>Vaccine Name:</strong>
            <p>${data.vaccine_name}</p>
          </div>
          
          <div class="detail-row">
            <strong>Number of Doses:</strong>
            <p>${data.doses}</p>
          </div>
          
          <div class="detail-row">
            <strong>Dosage Details:</strong>
            <p>${data.dosage_details}</p>
          </div>
          
          <div class="detail-row">
            <strong>Vaccination Schedule:</strong>
            <p>${data.schedule}</p>
          </div>
          
          <div class="detail-row">
            <strong>Recommendation:</strong>
            <p>${data.recommendation}</p>
          </div>
          
          <div class="detail-row side-effects">
            <strong>Possible Side Effects:</strong>
            <p>${data.side_effects}</p>
          </div>
        </div>
      </div>
    `;
  }
  
  // If disease not found
  return `
    <div class="result-card glass-card">
      <p class="error-message">${data.message || 'Disease not found.'}</p>
      ${data.suggestion ? `<p><em>${data.suggestion}</em></p>` : ''}
    </div>
  `;
}

vaccineForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  vaccineResult.innerHTML = '<div class="result-card glass-card"><p>Loading vaccine information...</p></div>';

  const disease = diseaseInput.value.trim();
  if (!disease) {
    vaccineResult.innerHTML = '<div class="result-card glass-card"><p>Please enter a disease name.</p></div>';
    return;
  }

  try {
    const response = await fetch('/vaccine-info', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ disease }),
    });

    if (!response.ok) {
      vaccineResult.innerHTML = '<div class="result-card glass-card error-message"><p>❌ Unable to retrieve vaccine information. Please try again.</p></div>';
      return;
    }

    const data = await response.json();
    vaccineResult.innerHTML = renderVaccineInfo(data);
    diseaseInput.value = '';
  } catch (err) {
    vaccineResult.innerHTML = '<div class="result-card glass-card error-message"><p>❌ Network error. Please try again.</p></div>';
  }
});
