const fetchBtn = document.getElementById("fetchBtn");
const compareBtn = document.getElementById("compareBtn");
const weatherCard = document.getElementById("weatherCard");
const compareResults = document.getElementById("compareResults");

fetchBtn.addEventListener("click", async () => {
  const city = document.getElementById("cityInput").value.trim();
  if (!city) return;

  try {
    const base = window.location.origin || "http://localhost:5000";
    const res = await fetch(`${base}/api/weather?city=${encodeURIComponent(city)}`);
    const text = await res.text();
    let result;
    try {
      result = JSON.parse(text);
    } catch (parseError) {
      throw new Error(`API no devolvió JSON válido (estado ${res.status}): ${text.slice(0, 200)}`);
    }

    if (res.ok) {
      if (result.status === "ambiguous") {
        showAmbiguousChoices(result.choices, city);
      } else {
        showWeather(result);
      }
    } else {
      showError(result.error || `No se pudo obtener el clima (status ${res.status})`);
    }
  } catch (err) {
    showError(err.message);
  }
});

function showAmbiguousChoices(choices, queryCity) {
  weatherCard.classList.remove("hidden");
  if (!Array.isArray(choices) || !choices.length) {
    weatherCard.innerHTML = "<p>No hay opciones disponibles.</p>";
    return;
  }

  const optionsHtml = choices
    .map(
      (c, i) =>
        `<option value='${i}'>${c.name}, ${c.country} (${c.latitude.toFixed(4)}, ${c.longitude.toFixed(4)})</option>`
    )
    .join("");

  weatherCard.innerHTML = `
    <p>Se encontraron múltiples coincidencias para "${queryCity}". Seleccione una:</p>
    <select id="ambiguousSelect">${optionsHtml}</select>
    <button id="ambiguousConfirmBtn">Ver clima</button>
  `;

  document.getElementById("ambiguousConfirmBtn").addEventListener("click", async () => {
    const selectedIndex = parseInt(document.getElementById("ambiguousSelect").value, 10);
    const choice = choices[selectedIndex];
    if (!choice) {
      showError("Selección inválida");
      return;
    }

    try {
      const base = window.location.origin || "http://localhost:5000";
      const weatherRes = await fetch(
        `${base}/api/weather-by-coords?latitude=${encodeURIComponent(choice.latitude)}&longitude=${encodeURIComponent(choice.longitude)}&city=${encodeURIComponent(choice.name)}`
      );
      const weatherText = await weatherRes.text();
      const weatherData = JSON.parse(weatherText);

      if (weatherRes.ok && weatherData.status === "ok") {
        showWeather(weatherData);
      } else {
        showError(weatherData.error || "No se pudo obtener el clima de la opción seleccionada.");
      }
    } catch (err) {
      showError(err.message);
    }
  });
}

compareBtn.addEventListener("click", async () => {
  const input = prompt("Ciudades separadas por coma ('London, Paris')");
  if (!input) return;
  const cities = input.split(",").map((c) => c.trim()).filter(Boolean);

  try {
    const res = await fetch("/api/compare", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ cities }),
    });
    const result = await res.json();
    if (res.ok) {
      showComparison(result);
    } else {
      showError(result.error || "Error comparando ciudades");
    }
  } catch (err) {
    showError(err.message);
  }
});

function showWeather(data) {
  weatherCard.classList.remove("hidden");
  if (!data || !data.city) {
    weatherCard.innerHTML = "<p>Clima no disponible</p>";
    return;
  }

  weatherCard.innerHTML = `
    <div class="weather-header">
      <h2 class="weather-title">${data.city}</h2>
      <p>${data.condition || "---"}</p>
    </div>
    <div class="weather-temp">${data.temperature}°C</div>
    <p>Humedad: ${data.humidity}% • Viento: ${data.wind_speed} km/h</p>
  `;
}

function showComparison(rows) {
  compareResults.innerHTML = "";
  if (!Array.isArray(rows)) {
    showError("Sin resultados comparativos");
    return;
  }

  for (const item of rows) {
    const block = document.createElement("article");
    block.className = "city-block";
    block.innerHTML = `
      <h3>${item.city}</h3>
      <p>Status: ${item.status}</p>
      <p>Temp: ${item.temp}</p>
      <p>Humedad: ${item.humidity}</p>
      <p>Viento: ${item.wind}</p>
      <p>Condición: ${item.condition}</p>
    `;
    compareResults.appendChild(block);
  }
}

function showError(message) {
  weatherCard.classList.remove("hidden");
  weatherCard.innerHTML = `<p style="color: #ff4757;">${message}</p>`;
}
