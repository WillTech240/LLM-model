// Sample data
const SAMPLE_DATA = {
    date: "2025-11-28",
    total_screen_time_minutes: 540,
    apps: [
        { name: "VS Code", category: "productivity", minutes: 240 },
        { name: "Chrome", category: "productivity", minutes: 120 },
        { name: "Instagram", category: "social", minutes: 90 },
        { name: "YouTube", category: "entertainment", minutes: 60 },
        { name: "Slack", category: "productivity", minutes: 30 }
    ],
    sessions: [
        { start_hour: 9, end_hour: 12, minutes: 180 },
        { start_hour: 14, end_hour: 18, minutes: 240 },
        { start_hour: 22, end_hour: 23, minutes: 60 }
    ]
};

// DOM
const jsonInput = document.getElementById("jsonInput");
const loadSampleBtn = document.getElementById("loadSampleBtn");
const analyzeBtn = document.getElementById("analyzeBtn");
const errorMessage = document.getElementById("errorMessage");
const resultsSection = document.getElementById("resultsSection");

// Events
loadSampleBtn.addEventListener("click", loadSampleData);
analyzeBtn.addEventListener("click", analyzeData);

function loadSampleData() {
    jsonInput.value = JSON.stringify(SAMPLE_DATA, null, 2);
    hideError();

    jsonInput.style.animation = "none";
    setTimeout(() => {
        jsonInput.style.animation = "fadeInUp 0.5s ease";
    }, 10);
}

async function analyzeData() {
    hideError();

    let data;
    try {
        data = JSON.parse(jsonInput.value);
    } catch {
        showError("Invalid JSON format.");
        return;
    }

    if (!data.total_screen_time_minutes || !data.apps || !data.sessions) {
        showError("Missing required fields: total_screen_time_minutes, apps, or sessions.");
        return;
    }

    analyzeBtn.disabled = true;
    analyzeBtn.textContent = "Analyzing...";

    try {
        const response = await fetch("http://localhost:5000/analyze", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();
        displayResults(result);

    } catch (error) {
        showError(`Error: ${error.message}. Ensure server is running.`);
    } finally {
        analyzeBtn.disabled = false;
        analyzeBtn.textContent = "Analyze";
    }
}

function displayResults(result) {
    resultsSection.style.display = "block";
    resultsSection.scrollIntoView({ behavior: "smooth" });

    displayOverallScore(result.overall_score);
    displayBreakdown(result.breakdown);
    displayTags(result.tags);
    displayPatterns(result.patterns);
    displayInsight(result.llm_insight);
    displayMetrics(result.metrics);
}

function displayOverallScore(score) {
    const scoreElement = document.getElementById("overallScore");
    const statusElement = document.getElementById("scoreStatus");

    animateValue(scoreElement, 0, score, 1000);

    let status;
    let gradient;

    if (score >= 80) {
        status = "Excellent";
        gradient = "var(--gradient-success)";
    } else if (score >= 60) {
        status = "Good";
        gradient = "var(--gradient-primary)";
    } else if (score >= 40) {
        status = "Needs Improvement";
        gradient = "var(--gradient-warning)";
    } else {
        status = "Concerning";
        gradient = "var(--gradient-danger)";
    }

    statusElement.textContent = status;
    document.querySelector(".score-circle").style.background = gradient;
}

function displayBreakdown(breakdown) {
    const grid = document.getElementById("breakdownGrid");
    grid.innerHTML = "";

    const labels = {
        screen_time: "Screen Time",
        diversity: "App Diversity",
        timing: "Usage Timing",
        balance: "Category Balance",
        breaks: "Break Patterns"
    };

    Object.entries(breakdown).forEach(([key, value], index) => {
        const item = document.createElement("div");
        item.className = "breakdown-item";
        item.innerHTML = `
            <div class="breakdown-label">${labels[key]}</div>
            <div class="breakdown-value">${value}</div>
        `;
        item.style.animation = "fadeInUp 0.5s ease";
        item.style.animationDelay = `${index * 0.1}s`;
        grid.appendChild(item);
    });
}

function displayTags(tags) {
    const container = document.getElementById("tagsContainer");
    container.innerHTML = "";

    tags.forEach((tag, index) => {
        const tagElement = document.createElement("span");
        tagElement.className = "tag";
        tagElement.textContent = tag;
        tagElement.style.animationDelay = `${index * 0.1}s`;
        container.appendChild(tagElement);
    });
}

function displayPatterns(patterns) {
    const list = document.getElementById("patternsList");
    list.innerHTML = "";

    if (patterns.length === 0) {
        list.innerHTML = "<li>No significant patterns detected</li>";
        return;
    }

    patterns.forEach((pattern, index) => {
        const item = document.createElement("li");
        item.textContent = pattern;
        item.style.animationDelay = `${index * 0.1}s`;
        list.appendChild(item);
    });
}

function displayInsight(insight) {
    const content = document.getElementById("insightContent");
    content.innerHTML = `<p>${insight}</p>`;
    content.style.animation = "fadeIn 1s ease";
}

function displayMetrics(metrics) {
    const grid = document.getElementById("metricsGrid");
    grid.innerHTML = "";

    const metricData = [
        { label: "Screen Time", value: `${metrics.total_screen_time_hours}h` },
        { label: "Apps Used", value: metrics.app_count },
        { label: "Sessions", value: metrics.session_count }
    ];

    metricData.forEach((metric, index) => {
        const item = document.createElement("div");
        item.className = "metric-item";
        item.innerHTML = `
            <span class="metric-value">${metric.value}</span>
            <span class="metric-label">${metric.label}</span>
        `;
        item.style.animation = "fadeInUp 0.5s ease";
        item.style.animationDelay = `${index * 0.1}s`;
        grid.appendChild(item);
    });
}

function animateValue(element, start, end, duration) {
    const range = end - start;
    const increment = range / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= end) {
            element.textContent = Math.round(end * 10) / 10;
            clearInterval(timer);
        } else {
            element.textContent = Math.round(current * 10) / 10;
        }
    }, 16);
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = "block";
    errorMessage.scrollIntoView({ behavior: "smooth" });
}

function hideError() {
    errorMessage.style.display = "none";
}
