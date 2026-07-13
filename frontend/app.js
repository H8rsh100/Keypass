// DOM Elements
const passwordInput = document.getElementById("password-input");
const algoSelect = document.getElementById("algo-select");
const hashOutput = document.getElementById("hash-output");
const copyHashBtn = document.getElementById("btn-copy-hash");

// Preset Buttons
const btnWeak = document.getElementById("btn-generate-weak");
const btnMed = document.getElementById("btn-generate-med");
const btnStrong = document.getElementById("btn-generate-strong");

// Attack Actions
const btnDict = document.getElementById("btn-attack-dict");
const btnBf = document.getElementById("btn-attack-bf");
const btnRt = document.getElementById("btn-attack-rt");
const btnBench = document.getElementById("btn-attack-bench");

// Brute Force Settings
const cbLower = document.getElementById("cb-lower");
const cbUpper = document.getElementById("cb-upper");
const cbDigits = document.getElementById("cb-digits");
const cbSymbols = document.getElementById("cb-symbols");
const bfLenRange = document.getElementById("bf-len-range");
const bfLenVal = document.getElementById("bf-len-val");
const bfWarning = document.getElementById("bf-warning");

// Rainbow Table Settings
const btnPrecompute = document.getElementById("btn-precompute");
const precomputeProgressContainer = document.getElementById("precompute-progress-container");
const precomputeProgressFill = document.getElementById("precompute-progress-fill");
const precomputeProgressText = document.getElementById("precompute-progress-text");

// Live Cracking Panel
const activeAttackBadge = document.getElementById("active-attack-badge");
const consoleOutput = document.getElementById("console-output");
const btnClearConsole = document.getElementById("btn-clear-console");

// Stats Readouts
const statElapsed = document.getElementById("stat-elapsed");
const statSpeed = document.getElementById("stat-speed");
const statAttempts = document.getElementById("stat-attempts");
const statCandidate = document.getElementById("stat-candidate");

// Insights
const entropyBits = document.getElementById("entropy-bits");
const entropyStrength = document.getElementById("entropy-strength");
const entropyPoolSize = document.getElementById("entropy-pool-size");
const entropyPoolDesc = document.getElementById("entropy-pool-desc");
const entropyCombinations = document.getElementById("entropy-combinations");
const entropyCrackTime = document.getElementById("entropy-crack-time");

// Benchmark Rows
const rowRainbow = document.getElementById("row-rainbow");
const rowDictionary = document.getElementById("row-dictionary");
const rowBruteforce = document.getElementById("row-bruteforce");

// Global WebSocket Variable
let socket = null;
let activeAttackType = null;

// Presets lists
const WEAK_PRESETS = ["password", "123456", "dragon", "letmein", "monkey", "admin"];
const MED_PRESETS = ["Tr0ub4dor&3", "J4ck$0n!", "nascar99!", "cheese123", "blue1992"];
const STRONG_PRESETS = ["K8s#p@ss_W0rd!", "c@t_On_A_k3yb0@rd", "XyZ#987!vW", "7%wR_#9pLm!z"];

// Helper: Format large numbers
function formatNumber(num) {
    if (num >= 1e12) return (num / 1e12).toFixed(2) + "T";
    if (num >= 1e9) return (num / 1e9).toFixed(2) + "B";
    if (num >= 1e6) return (num / 1e6).toFixed(2) + "M";
    if (num >= 1e3) return (num / 1e3).toFixed(2) + "K";
    return num.toString();
}

// Helper: Format Time
function formatTime(seconds) {
    if (seconds === 0) return "0.00s";
    if (seconds < 0.001) return "< 1ms";
    if (seconds < 1) return (seconds * 1000).toFixed(0) + "ms";
    if (seconds < 60) return seconds.toFixed(2) + "s";
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    return `${minutes}m ${remainingSeconds.toFixed(1)}s`;
}

// Helper: Format estimated crack time (real world)
function formatEstimatedTime(seconds) {
    if (seconds === 0) return "0s";
    if (seconds < 1) return "instant (less than 1s)";
    
    const minutes = seconds / 60;
    if (minutes < 60) return `${Math.round(minutes)} minutes`;
    
    const hours = minutes / 60;
    if (hours < 24) return `${Math.round(hours)} hours`;
    
    const days = hours / 24;
    if (days < 365) return `${Math.round(days)} days`;
    
    const years = days / 365;
    if (years < 1000) return `${Math.round(years)} years`;
    if (years < 1e6) return `${Math.round(years / 1000)}K years`;
    if (years < 1e9) return `${Math.round(years / 1e6)}M years`;
    return "centuries";
}

// Write to Live Log
function logToConsole(message, type = "system") {
    const line = document.createElement("div");
    line.className = `console-line ${type}-line`;
    
    const timestamp = new Date().toLocaleTimeString('en-US', { hour12: false });
    line.textContent = `[${timestamp}] ${message}`;
    
    consoleOutput.appendChild(line);
    // Limit console output size
    while (consoleOutput.childNodes.length > 500) {
        consoleOutput.removeChild(consoleOutput.firstChild);
    }
    consoleOutput.scrollTop = consoleOutput.scrollHeight;
}

// Fetch Hashed value from api
async function updateHash() {
    const password = passwordInput.value;
    const algorithm = algoSelect.value;
    
    if (!password) {
        hashOutput.value = "";
        return;
    }
    
    try {
        const response = await fetch("/api/hash", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password, algorithm })
        });
        
        if (response.ok) {
            const data = await response.json();
            hashOutput.value = data.hash;
        } else {
            const errData = await response.json();
            hashOutput.value = `Error: ${errData.detail}`;
        }
    } catch (err) {
        hashOutput.value = `Connection error`;
    }
}

// Copy Hash
copyHashBtn.addEventListener("click", () => {
    if (hashOutput.value && !hashOutput.value.startsWith("Error") && !hashOutput.value.startsWith("Connection")) {
        navigator.clipboard.writeText(hashOutput.value);
        logToConsole("Hash copied to clipboard.", "system");
    }
});

// Preset event listeners
btnWeak.addEventListener("click", () => {
    const rand = WEAK_PRESETS[Math.floor(Math.random() * WEAK_PRESETS.length)];
    passwordInput.value = rand;
    updateHash();
});

btnMed.addEventListener("click", () => {
    const rand = MED_PRESETS[Math.floor(Math.random() * MED_PRESETS.length)];
    passwordInput.value = rand;
    updateHash();
});

btnStrong.addEventListener("click", () => {
    const rand = STRONG_PRESETS[Math.floor(Math.random() * STRONG_PRESETS.length)];
    passwordInput.value = rand;
    updateHash();
});

passwordInput.addEventListener("input", updateHash);
algoSelect.addEventListener("change", updateHash);

// Brute Force Warning check
function checkBfWarning() {
    let count = 0;
    if (cbLower.checked) count++;
    if (cbUpper.checked) count++;
    if (cbDigits.checked) count++;
    if (cbSymbols.checked) count++;
    
    const length = parseInt(bfLenRange.value);
    bfLenVal.textContent = length;
    
    if (length >= 5 && count >= 3) {
        bfWarning.style.display = "block";
    } else if (length >= 6) {
        bfWarning.style.display = "block";
    } else {
        bfWarning.style.display = "none";
    }
}

[cbLower, cbUpper, cbDigits, cbSymbols, bfLenRange].forEach(el => {
    el.addEventListener("change", checkBfWarning);
    el.addEventListener("input", checkBfWarning);
});

// Precompute Rainbow Table websocket trigger
btnPrecompute.addEventListener("click", () => {
    if (socket) return;
    
    btnPrecompute.disabled = true;
    precomputeProgressContainer.style.display = "block";
    precomputeProgressFill.style.style = "0%";
    precomputeProgressText.textContent = "Connecting to database generator...";
    
    logToConsole("Initializing precomputation of SQLite rainbow table...", "system");
    
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    socket = new WebSocket(`${protocol}//${window.location.host}/api/ws/crack`);
    
    socket.onopen = () => {
        socket.send(JSON.stringify({ action: "precompute" }));
    };
    
    socket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        if (payload.error) {
            logToConsole(`Precomputation failed: ${payload.error}`, "error");
            btnPrecompute.disabled = false;
            socket.close();
            return;
        }
        
        const progress = payload.data;
        if (progress.status === "in_progress") {
            precomputeProgressFill.style.width = `${progress.percent}%`;
            precomputeProgressText.textContent = `Processing: ${progress.processed}/${progress.total} (${progress.percent}%)`;
            if (progress.processed % 2000 === 0) {
                logToConsole(`Indexed ${progress.processed} words in database...`, "system");
            }
        } else if (progress.status === "complete") {
            precomputeProgressFill.style.width = "100%";
            precomputeProgressText.textContent = "Complete";
            logToConsole("Rainbow table precomputation complete! SQLite cached successfully.", "success");
            btnPrecompute.disabled = false;
            socket.close();
        }
    };
    
    socket.onclose = () => {
        socket = null;
    };
    
    socket.onerror = (err) => {
        logToConsole(`Generator error: ${err.message}`, "error");
        btnPrecompute.disabled = false;
    };
});

// Function to handle Attack Websockets
function startStreamingAttack(actionType) {
    if (socket) {
        logToConsole("Another process is currently active. Aborting start.", "error");
        return;
    }
    
    const targetHash = hashOutput.value;
    const algorithm = algoSelect.value;
    
    if (!targetHash || targetHash.startsWith("Error")) {
        logToConsole("Invalid target hash. Make sure hash field is populated.", "error");
        return;
    }
    
    // UI states
    activeAttackType = actionType;
    activeAttackBadge.textContent = actionType.replace("_", " ").toUpperCase();
    activeAttackBadge.className = "badge badge-active";
    disableInputs(true);
    
    statElapsed.textContent = "0.00s";
    statSpeed.textContent = "0 h/s";
    statAttempts.textContent = "0";
    statCandidate.textContent = "...";
    
    logToConsole(`Starting ${actionType.replace("_", " ")} attack against ${algorithm} hash...`, "system");
    logToConsole(`Target: ${targetHash}`, "system");

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    socket = new WebSocket(`${protocol}//${window.location.host}/api/ws/crack`);
    
    socket.onopen = () => {
        const config = {
            action: actionType,
            target_hash: targetHash,
            algorithm: algorithm
        };
        
        if (actionType === "brute_force") {
            const charsetTypes = [];
            if (cbLower.checked) charsetTypes.push("lowercase");
            if (cbUpper.checked) charsetTypes.push("uppercase");
            if (cbDigits.checked) charsetTypes.push("digits");
            if (cbSymbols.checked) charsetTypes.push("symbols");
            
            config.charset_types = charsetTypes;
            config.max_length = parseInt(bfLenRange.value);
        }
        
        socket.send(JSON.stringify(config));
    };
    
    socket.onmessage = (event) => {
        const payload = JSON.parse(event.data);
        if (payload.error) {
            logToConsole(`Attack error: ${payload.error}`, "error");
            socket.close();
            return;
        }
        
        const data = payload.data;
        statElapsed.textContent = `${data.elapsed.toFixed(2)}s`;
        statAttempts.textContent = formatNumber(data.attempts);
        statSpeed.textContent = `${formatNumber(data.attempts_per_second)} h/s`;
        statCandidate.textContent = data.current_candidate || "N/A";
        
        // Print progress line
        if (data.current_candidate) {
            logToConsole(`Trying candidate: ${data.current_candidate} | Attempts: ${data.attempts}`, "attempt");
        }
        
        if (data.found) {
            logToConsole(`CRACK SUCCESS! Plaintext: "${data.plaintext}"`, "success");
            logToConsole(`Time taken: ${data.elapsed.toFixed(3)}s | Total attempts: ${data.attempts}`, "success");
            socket.close();
        } else if (data.plaintext === null) {
            logToConsole(`Attack finished. Target hash was NOT cracked.`, "error");
            socket.close();
        }
    };
    
    socket.onclose = () => {
        socket = null;
        activeAttackType = null;
        activeAttackBadge.textContent = "IDLE";
        activeAttackBadge.className = "badge badge-inactive";
        disableInputs(false);
    };
    
    socket.onerror = (err) => {
        logToConsole(`Socket connection error: ${err.message}`, "error");
        disableInputs(false);
    };
}

// Rainbow Table Lookup (Instant, non-websocket or short socket check)
async function startRainbowLookup() {
    const targetHash = hashOutput.value;
    const algorithm = algoSelect.value;
    
    if (!targetHash) return;
    
    logToConsole(`Starting Rainbow Table index lookup for ${targetHash}...`, "system");
    
    activeAttackBadge.textContent = "RAINBOW LOOKUP";
    activeAttackBadge.className = "badge badge-active";
    
    const start = performance.now();
    
    // Connect short socket or fetch? Let's use a websocket config
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const rtSocket = new WebSocket(`${protocol}//${window.location.host}/api/ws/crack`);
    
    rtSocket.onopen = () => {
        // We will emulate database lookup or benchmark trigger.
        // Wait, main.py Websocket doesn't have a direct "rainbow" lookup, but it is fast, 
        // actually we can trigger a short connection or run it via the benchmark route.
        // Let's run a GET request or benchmark trigger since lookup_hash is instant.
        // Or wait, let's just query the /api/benchmark route to get the details!
        // Yes, querying `/api/benchmark` runs it in the backend and returns the side-by-side.
        // Let's query `/api/benchmark` directly.
        fetchBenchmarkData();
        rtSocket.close();
    };
    
    rtSocket.onclose = () => {
        activeAttackBadge.textContent = "IDLE";
        activeAttackBadge.className = "badge badge-inactive";
    };
}

// Disable/enable form inputs during attacks
function disableInputs(disabled) {
    passwordInput.disabled = disabled;
    algoSelect.disabled = disabled;
    btnWeak.disabled = disabled;
    btnMed.disabled = disabled;
    btnStrong.disabled = disabled;
    btnDict.disabled = disabled;
    btnBf.disabled = disabled;
    btnRt.disabled = disabled;
    btnBench.disabled = disabled;
}

// Fetch Side-by-Side Benchmarks & Entropy
async function fetchBenchmarkData() {
    const password = passwordInput.value;
    const algorithm = algoSelect.value;
    
    if (!password) return;
    
    logToConsole("Running full comparison benchmark on the target password...", "system");
    disableInputs(true);
    
    try {
        const response = await fetch("/api/benchmark", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ password, algorithm })
        });
        
        if (response.ok) {
            const data = await response.json();
            updateInsightsUI(data);
            logToConsole("Benchmark run completed.", "success");
        } else {
            const err = await response.json();
            logToConsole(`Benchmark failed: ${err.detail}`, "error");
        }
    } catch (e) {
        logToConsole("Connection to benchmark API failed.", "error");
    } finally {
        disableInputs(false);
    }
}

// Update Insights & Table UI
function updateInsightsUI(data) {
    // 1. Update Entropy Card
    const ent = data.entropy;
    entropyBits.textContent = ent.entropy_bits.toFixed(2);
    
    // Strength styling
    entropyStrength.textContent = ent.strength.replace("_", " ");
    entropyStrength.className = `badge-strength ${ent.strength}`;
    
    entropyPoolSize.textContent = ent.pool_size;
    entropyPoolDesc.textContent = ent.pool_description;
    entropyCombinations.textContent = formatNumber(ent.combinations);
    entropyCrackTime.textContent = formatEstimatedTime(ent.estimated_crack_time_seconds);

    // 2. Update Table Rows
    // Rainbow Table Row
    const rt = data.rainbow_table;
    rowRainbow.querySelector(".col-cracked").textContent = rt.cracked ? "YES (INSTANT)" : "NO";
    rowRainbow.querySelector(".col-cracked").className = "col-cracked " + (rt.cracked ? "yes" : "no");
    rowRainbow.querySelector(".col-time").textContent = formatTime(rt.time_taken);
    rowRainbow.querySelector(".col-attempts").textContent = rt.cracked ? "1 lookup" : "1 lookup";

    // Dictionary Row
    const dict = data.dictionary;
    rowDictionary.querySelector(".col-cracked").textContent = dict.cracked ? "YES" : "NO";
    rowDictionary.querySelector(".col-cracked").className = "col-cracked " + (dict.cracked ? "yes" : "no");
    rowDictionary.querySelector(".col-time").textContent = formatTime(dict.time_taken);
    rowDictionary.querySelector(".col-attempts").textContent = dict.attempts;
    rowDictionary.querySelector(".col-speed").textContent = dict.time_taken > 0 ? `${formatNumber(Math.round(dict.attempts / dict.time_taken))} h/s` : "N/A";

    // Brute Force Row
    const bf = data.brute_force;
    rowBruteforce.querySelector(".col-cracked").textContent = bf.cracked ? "YES" : (bf.status === "timed_out" ? "TIMEOUT" : "NO");
    rowBruteforce.querySelector(".col-cracked").className = "col-cracked " + (bf.cracked ? "yes" : "no");
    rowBruteforce.querySelector(".col-time").textContent = formatTime(bf.time_taken);
    rowBruteforce.querySelector(".col-attempts").textContent = bf.attempts;
    rowBruteforce.querySelector(".col-speed").textContent = bf.time_taken > 0 ? `${formatNumber(Math.round(bf.attempts / bf.time_taken))} h/s` : "N/A";
}

// Attack Button Handlers
btnDict.addEventListener("click", () => startStreamingAttack("dictionary"));
btnBf.addEventListener("click", () => startStreamingAttack("brute_force"));
btnRt.addEventListener("click", startRainbowLookup);
btnBench.addEventListener("click", fetchBenchmarkData);

// Console Clear Handler
btnClearConsole.addEventListener("click", () => {
    consoleOutput.innerHTML = '<div class="console-line system-line">[SYSTEM] Console buffer cleared. Ready.</div>';
});

// Run Initial Hashing
updateHash();
checkBfWarning();
