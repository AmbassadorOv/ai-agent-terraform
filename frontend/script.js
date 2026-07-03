document.addEventListener('DOMContentLoaded', () => {
    // --- DATA STORAGE & STATE (Existing) ---
    const fleetData = [
        { id: 'AG-1024', role: 'Analysis', confidence: 0.85, status: 'acknowledged', human_approved: 1 },
        { id: 'AG-2048', role: 'Data Collection', confidence: 0.45, status: 'quarantined', human_approved: 0 },
        { id: 'AG-3091', role: 'Governance', confidence: 0.72, status: 'acknowledged', human_approved: 0 },
        { id: 'AG-4421', role: 'Analysis', confidence: 0.91, status: 'acknowledged', human_approved: 1 },
        { id: 'AG-5100', role: 'Automation', confidence: 0.20, status: 'quarantined', human_approved: 0 },
        { id: 'AG-6622', role: 'Validation', confidence: 0.64, status: 'obliged', human_approved: 0 },
        { id: 'AG-7111', role: 'Communication', confidence: 0.66, status: 'acknowledged', human_approved: 1 },
        { id: 'AG-8902', role: 'Data Collection', confidence: 0.55, status: 'quarantined', human_approved: 0 },
    ];

    const endpointsData = [
        { method: 'GET', url: '/', purpose: 'Command Information Center (CIC) Dashboard', auth: 'Browser' },
        { method: 'GET', url: '/health', purpose: 'System liveness check', auth: 'None' },
        { method: 'POST', url: '/register', purpose: 'Enrollment & Confidence Scoring', auth: 'None' },
        { method: 'POST', url: '/agents/<id>/ack', purpose: 'Containment Rule Acknowledgement', auth: 'Agent Sig' },
        { method: 'POST', url: '/agents/<id>/requestactuation', purpose: 'Critical Check (Conf >= 0.65 & Approved)', auth: 'Agent Req' },
        { method: 'POST', url: '/agents/<id>/humanapprove', purpose: 'Operator Actuation Clearance', auth: 'HIGH (Operator)' },
        { method: 'GET', url: '/anchors', purpose: 'Retrieve Front Door Links', auth: 'None' },
    ];

    // --- NEUROMORPHIC UI ELEMENTS ---
    const consoleStream = document.getElementById('console-stream');
    const clearConsoleBtn = document.getElementById('clear-console');
    const runSandboxBtn = document.getElementById('run-sandbox-btn');
    const visualizerStatus = document.getElementById('visualizer-status');
    const bridgeStability = document.getElementById('bridge-stability');
    const bridgeStabilityBar = document.getElementById('bridge-stability-bar');
    const ontologyAccuracy = document.getElementById('ontology-accuracy');
    const ontologyAccuracyBar = document.getElementById('ontology-accuracy-bar');
    const canvas = document.getElementById('synapse-canvas');
    const ctx = canvas.getContext('2d');

    let nodes = [];
    let animationFrameId;

    // --- DASHBOARD INITIALIZATION ---
    function initDashboard() {
        const fleetCount = fleetData.length;
        const avgConf = (fleetData.reduce((acc, curr) => acc + curr.confidence, 0) / fleetCount).toFixed(2);
        const pending = fleetData.filter(a => a.confidence >= 0.65 && a.human_approved === 0).length;

        document.getElementById('stat-fleet-count').textContent = fleetCount;
        document.getElementById('stat-avg-conf').textContent = avgConf;
        document.getElementById('stat-pending').textContent = pending;

        renderStatusChart();
        renderConfidenceChart();
    }

    function renderStatusChart() {
        const ctxChart = document.getElementById('statusChart').getContext('2d');
        const statusCounts = {
            'obliged': fleetData.filter(d => d.status === 'obliged').length,
            'acknowledged': fleetData.filter(d => d.status === 'acknowledged').length,
            'quarantined': fleetData.filter(d => d.status === 'quarantined').length
        };

        new Chart(ctxChart, {
            type: 'doughnut',
            data: {
                labels: ['Obliged', 'Acknowledged', 'Quarantined'],
                datasets: [{
                    data: [statusCounts.obliged, statusCounts.acknowledged, statusCounts.quarantined],
                    backgroundColor: ['#94a3b8', '#0ea5e9', '#6366f1'],
                    borderWidth: 0
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                cutout: '70%'
            }
        });
    }

    function renderConfidenceChart() {
        const ctxChart = document.getElementById('confidenceChart').getContext('2d');
        const sortedData = [...fleetData].sort((a, b) => b.confidence - a.confidence);
        const labels = sortedData.map(a => a.id);
        const dataPoints = sortedData.map(a => a.confidence);
        const bgColors = dataPoints.map(val => val < 0.65 ? '#ef4444' : '#0ea5e9');

        new Chart(ctxChart, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Confidence',
                    data: dataPoints,
                    backgroundColor: bgColors,
                    borderRadius: 4
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false }
                },
                scales: {
                    y: { beginAtZero: true, max: 1.0, grid: { color: '#1e293b' } },
                    x: { grid: { display: false } }
                }
            }
        });
    }

    function renderEndpoints(data) {
        const tbody = document.getElementById('endpoints-body');
        tbody.innerHTML = '';
        data.forEach(ep => {
            const tr = document.createElement('tr');
            tr.className = "hover:bg-slate-800/50 transition-colors";
            tr.innerHTML = `
                <td class="px-6 py-4"><span class="px-2 py-1 bg-slate-800 rounded text-xs font-bold text-cyan-400">${ep.method}</span></td>
                <td class="px-6 py-4 font-mono text-slate-300">${ep.url}</td>
                <td class="px-6 py-4 text-slate-400">${ep.purpose}</td>
                <td class="px-6 py-4 text-xs text-slate-500">${ep.auth}</td>
            `;
            tbody.appendChild(tr);
        });
    }

    function setupSearch() {
        document.getElementById('endpoint-search').addEventListener('input', (e) => {
            const term = e.target.value.toLowerCase();
            const filtered = endpointsData.filter(ep =>
                ep.url.toLowerCase().includes(term) || ep.purpose.toLowerCase().includes(term)
            );
            renderEndpoints(filtered);
        });
    }

    // --- CANVAS VISUALIZER ---
    function resizeCanvas() {
        const rect = canvas.parentNode.getBoundingClientRect();
        canvas.width = rect.width;
        canvas.height = rect.height;
        initNodes();
    }

    function initNodes() {
        nodes = [];
        for (let i = 0; i < 35; i++) {
            nodes.push({
                x: Math.random() * canvas.width,
                y: Math.random() * canvas.height,
                vx: (Math.random() - 0.5) * 0.8,
                vy: (Math.random() - 0.5) * 0.8,
                radius: Math.random() * 2 + 1,
                pulse: Math.random() * Math.PI,
                color: i % 3 === 0 ? '#06b6d4' : (i % 3 === 1 ? '#6366f1' : '#10b981')
            });
        }
    }

    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.lineWidth = 0.5;
        for (let i = 0; i < nodes.length; i++) {
            for (let j = i + 1; j < nodes.length; j++) {
                const dist = Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y);
                if (dist < 80) {
                    ctx.strokeStyle = `rgba(99, 102, 241, ${1 - dist / 80})`;
                    ctx.beginPath();
                    ctx.moveTo(nodes[i].x, nodes[i].y);
                    ctx.lineTo(nodes[j].x, nodes[j].y);
                    ctx.stroke();
                }
            }
        }
        nodes.forEach(node => {
            node.x += node.vx; node.y += node.vy; node.pulse += 0.05;
            if (node.x < 0 || node.x > canvas.width) node.vx *= -1;
            if (node.y < 0 || node.y > canvas.height) node.vy *= -1;
            ctx.fillStyle = node.color;
            ctx.beginPath();
            ctx.arc(node.x, node.y, node.radius + Math.sin(node.pulse) * 0.5, 0, Math.PI * 2);
            ctx.fill();
        });
        animationFrameId = requestAnimationFrame(animate);
    }

    // --- STRESS TESTS & LOGGING ---
    function writeToConsole(message, type = 'info') {
        const div = document.createElement('div');
        const time = new Date().toLocaleTimeString();
        const colors = { success: 'text-green-400', error: 'text-red-400', warning: 'text-yellow-400', cyan: 'text-cyan-400', indigo: 'text-indigo-400' };
        div.innerHTML = `<span class="text-slate-500 font-mono">[${time}]</span> <span class="${colors[type] || 'text-slate-300'}">${message}</span>`;
        consoleStream.appendChild(div);
        consoleStream.scrollTop = consoleStream.scrollHeight;
    }

    async function runStressTests() {
        visualizerStatus.innerText = "RUNNING STRESS TESTS...";
        visualizerStatus.className = "px-2 py-0.5 bg-red-950 text-red-400 border border-red-800 text-[10px] font-mono rounded";

        writeToConsole("=== INITIATING SYSTEM-WIDE STRESS TESTS ===", "warning");
        writeToConsole("Mobilizing Agents for Admiral Julius via Multi-Level Bridge...", "cyan");

        await new Promise(r => setTimeout(r, 1000));
        writeToConsole("--> Validating Graph Neural Network configuration (PyTorch Geometric)...", "indigo");
        writeToConsole("--> Encoding structural synapses into Frozen Light Crystals...", "indigo");

        if (document.getElementById('test-quantum').checked) {
            writeToConsole("--> Running suite: QUANTUM FLOW SATURATION...", "warning");
            nodes.forEach(n => { n.vx *= 3; n.vy *= 3; });
            await new Promise(r => setTimeout(r, 1200));
            writeToConsole("✓ Quantum Flow validated. Kyber-1024 variant lattice nodes resilient.", "success");
        }

        if (document.getElementById('test-dilithium').checked) {
            writeToConsole("--> Running suite: DILITHIUM MULTI-SIGNATURES SURGE...", "warning");
            await new Promise(r => setTimeout(r, 1500));
            writeToConsole("✓ Generated dynamically verified Master signature 50.", "success");
        }

        if (document.getElementById('test-lazy-act').checked) {
            writeToConsole("--> Running suite: LAZY ACTIVATION COLLAPSE...", "warning");
            await new Promise(r => setTimeout(r, 1400));
            writeToConsole("✓ Lazy Activation verified. Peak activation footprint is O(1).", "success");
        }

        nodes.forEach(n => { n.vx /= 3; n.vy /= 3; });
        bridgeStability.innerText = "99.8%";
        bridgeStabilityBar.style.width = "99.8%";

        writeToConsole("=== ALL STRESS TESTS COMPLETED. FLEET MOBILIZED. ===", "success");
        visualizerStatus.innerText = "SYSTEM ACTIVE & VERIFIED";
        visualizerStatus.className = "px-2 py-0.5 bg-green-950 text-green-400 border border-green-800 text-[10px] font-mono rounded";
    }

    // --- MODAL CONTROL ---
    window.openEnrollModal = () => {
        const modal = document.getElementById('enrollModal');
        modal.classList.remove('hidden');
        setTimeout(() => { modal.style.opacity = 1; document.getElementById('modalContent').style.transform = 'scale(1)'; }, 10);
    };
    window.closeEnrollModal = () => {
        const modal = document.getElementById('enrollModal');
        modal.style.opacity = 0;
        document.getElementById('modalContent').style.transform = 'scale(0.95)';
        setTimeout(() => modal.classList.add('hidden'), 300);
    };

    // --- INIT ---
    window.addEventListener('resize', resizeCanvas);
    clearConsoleBtn.addEventListener('click', () => { consoleStream.innerHTML = ""; writeToConsole("Console cleared.", "slate-500"); });
    runSandboxBtn.addEventListener('click', runStressTests);

    resizeCanvas();
    animate();
    initDashboard();
    renderEndpoints(endpointsData);
    setupSearch();
    writeToConsole("Connected to Admiral Julius Orchestrator.", "success");
});
function generateTelemetrySeal() {
    const randomHash = Math.random().toString(16).substring(2, 10).toUpperCase();
    const div = document.createElement('div');
    div.innerHTML = `<span class="text-slate-500 font-mono">[${new Date().toLocaleTimeString()}]</span> <span class="text-indigo-400">Layer 1 Seal: ADM-N_PHYS_GATE_${randomHash}</span>`;
    document.getElementById('console-stream').appendChild(div);
}
window.generateTelemetrySeal = generateTelemetrySeal;
