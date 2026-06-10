import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Nasional: Pemantauan Krisis Kualitas Air Bersih</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body class="bg-gray-900 text-gray-100 font-sans min-h-screen flex flex-col">

    <header class="bg-gray-800 border-b border-gray-700 shadow-md p-4 flex flex-col md:flex-row justify-between items-center gap-4">
        <div class="flex items-center gap-3">
            <div class="bg-blue-600 text-white p-2 rounded-lg font-bold text-xl shadow"> </div>
            <div>
                <h1 class="text-xl md:text-2xl font-extrabold text-white tracking-wide">DASHBOARD NASIONAL</h1>
                <p class="text-xs text-blue-400 font-medium">Pemantauan Krisis Kualitas Air Bersih & Alokasi Intervensi Logistik</p>
            </div>
        </div>
        <div class="text-right hidden md:block">
            <span class="text-xs bg-gray-700 text-gray-300 px-3 py-1 rounded-full font-mono border border-gray-600">Data: 2009 - 2012</span>
        </div>
    </header>

    <div class="flex flex-col lg:flex-row flex-1">
        <aside class="w-full lg:w-72 bg-gray-850 p-6 border-b lg:border-b-0 lg:border-r border-gray-800 space-y-6 flex-shrink-0">
            <div class="flex items-center gap-2 pb-2 border-b border-gray-800">
                <span class="text-lg">🛸</span>
                <h2 class="text-md font-bold uppercase tracking-wider text-gray-300">Panel Filter Utama</h2>
            </div>
            
            <div>
                <label for="filter-year" class="block text-xs font-semibold uppercase text-gray-400 mb-2">Pilih Tahun Analisis</label>
                <select id="filter-year" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 cursor-pointer transition">
                    <option value="All">Semua Tahun</option>
                    <option value="2009">2009</option>
                    <option value="2010">2010</option>
                    <option value="2011">2011</option>
                    <option value="2012">2012</option>
                </select>
            </div>

            <div>
                <label for="filter-state" class="block text-xs font-semibold uppercase text-gray-400 mb-2">Negara Bagian (State)</label>
                <select id="filter-state" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 cursor-pointer transition">
                    <option value="All">Semua Negara Bagian</option>
                    <option value="RAJASTHAN">Rajasthan</option>
                    <option value="BIHAR">Bihar</option>
                    <option value="ASSAM">Assam</option>
                    <option value="ORISSA">Orissa</option>
                    <option value="ANDHRA PRADESH">Andhra Pradesh</option>
                </select>
            </div>

            <div>
                <label for="filter-parameter" class="block text-xs font-semibold uppercase text-gray-400 mb-2">Zat / Parameter Air</label>
                <select id="filter-parameter" class="w-full bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 text-sm text-white focus:outline-none focus:border-blue-500 cursor-pointer transition">
                    <option value="All">Semua Kontaminan</option>
                    <option value="Iron">Iron (Zat Besi)</option>
                    <option value="Fluoride">Fluoride</option>
                    <option value="Salinity">Salinity (Salinitas)</option>
                    <option value="Arsenic">Arsenic</option>
                    <option value="Nitrate">Nitrate</option>
                </select>
            </div>

            <div class="pt-4">
                <button id="reset-btn" class="w-full bg-gray-800 hover:bg-gray-700 text-gray-300 font-medium text-xs py-2 px-4 rounded-lg border border-gray-700 hover:border-gray-600 transition flex items-center justify-center gap-2">
                    🔄 Reset Semua Filter
                </button>
            </div>
        </aside>

        <main class="flex-1 p-6 space-y-6 overflow-x-hidden">
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow flex flex-col justify-between">
                    <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Total Pemukiman Terdampak</span>
                    <div class="flex items-baseline gap-2 mt-2">
                        <span id="kpi-total" class="text-3xl md:text-4xl font-extrabold text-blue-400">0</span>
                        <span class="text-xs text-gray-500 font-medium">Habitations</span>
                    </div>
                </div>
                <div class="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow flex flex-col justify-between">
                    <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Musuh Utama / Dominan</span>
                    <div class="mt-2">
                        <span id="kpi-dominant" class="text-2xl md:text-3xl font-extrabold text-red-500 tracking-wide">-</span>
                    </div>
                </div>
                <div class="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow flex flex-col justify-between">
                    <span class="text-xs font-bold text-gray-400 uppercase tracking-wider">Kabupaten Terpapar</span>
                    <div class="flex items-baseline gap-2 mt-2">
                        <span id="kpi-districts" class="text-3xl md:text-4xl font-extrabold text-amber-400">0</span>
                        <span class="text-xs text-gray-500 font-medium">Districts</span>
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-1 xl:grid-cols-2 gap-6">
                <div class="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow">
                    <h3 class="text-sm font-bold text-gray-300 uppercase tracking-wider mb-4">📈 Tren Krisis Air Tahunan</h3>
                    <div class="relative h-64 w-full">
                        <canvas id="chartLine"></canvas>
                    </div>
                </div>
                <div class="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow">
                    <h3 class="text-sm font-bold text-gray-300 uppercase tracking-wider mb-4">🍩 Komposisi Jenis Zat Pencemar</h3>
                    <div class="relative h-64 w-full flex justify-center">
                        <canvas id="chartDonut"></canvas>
                    </div>
                </div>
            </div>

            <div class="bg-gray-800 p-5 rounded-xl border border-gray-700 shadow">
                <h3 class="text-sm font-bold text-gray-300 uppercase tracking-wider mb-4">📊 Peringkat Wilayah Paling Kritis (Kasus Terbanyak)</h3>
                <div class="relative h-72 w-full">
                    <canvas id="chartBar"></canvas>
                </div>
            </div>

            <div class="bg-gray-800 rounded-xl border border-gray-700 shadow overflow-hidden">
                <div class="p-5 border-b border-gray-700 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-2">
                    <div>
                        <h3 class="text-sm font-bold text-gray-300 uppercase tracking-wider">📋 Daftar Alamat Wilayah Kasus untuk Intervensi</h3>
                        <p class="text-xs text-gray-400 mt-1">Data operasional taktis tim lapangan penempatan sistem filtrasi.</p>
                    </div>
                    <span id="table-count" class="text-xs bg-blue-900/50 text-blue-400 px-2.5 py-1 rounded border border-blue-800 font-mono">0 baris ditemukan</span>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse">
                        <thead>
                            <tr class="bg-gray-750 text-gray-400 uppercase text-xs font-bold tracking-wider border-b border-gray-700">
                                <th class="p-4">State</th>
                                <th class="p-4">District</th>
                                <th class="p-4">Block</th>
                                <th class="p-4">Panchayat</th>
                                <th class="p-4">Village</th>
                                <th class="p-4">Habitation</th>
                                <th class="p-4">Parameter</th>
                            </tr>
                        </thead>
                        <tbody id="table-body" class="divide-y divide-gray-700 text-sm text-gray-300">
                            </tbody>
                    </table>
                </div>
            </div>
        </main>
    </div>

    <script>
        // 1. DATASET UTAMA MENTAH (Simulasi Representatif 20-Data sampel dari total populasi 550.242 baris)
        // Catatan: Teks kurung kode seperti (04) sudah bersih sesuai instruksi ETL sebelumnya.
        const rawDataset = [
            { State: "ANDHRA PRADESH", District: "EAST GODAVARI", Block: "PRATHIPADU", Panchayat: "GOKAVARAM", Village: "VANTHADA", Habitation: "VANTHADA-A", Parameter: "Salinity", Year: 2009 },
            { State: "ANDHRA PRADESH", District: "EAST GODAVARI", Block: "PRATHIPADU", Panchayat: "GOKAVARAM", Village: "PANDAVULAPALEM", Habitation: "PANDAVULAPALEM-B", Parameter: "Fluoride", Year: 2009 },
            { State: "ANDHRA PRADESH", District: "EAST GODAVARI", Block: "PRATHIPADU", Panchayat: "GAJJANAPUDI", Village: "G. KOTHURU", Habitation: "G. KOTHURU-I", Parameter: "Salinity", Year: 2009 },
            { State: "RAJASTHAN", District: "JAIPUR", Block: "CHAMPA", Panchayat: "NAGAR", Village: "KHERA", Habitation: "KHERA DHANI", Parameter: "Fluoride", Year: 2010 },
            { State: "RAJASTHAN", District: "JAIPUR", Block: "CHAMPA", Panchayat: "MALIK", Village: "RAMPURA", Habitation: "RAMPURA MAIN", Parameter: "Fluoride", Year: 2010 },
            { State: "RAJASTHAN", District: "AJMER", Block: "BEAWAR", Panchayat: "DELHI", Village: "PALRI", Habitation: "PALRI-OLD", Parameter: "Salinity", Year: 2011 },
            { State: "BIHAR", District: "PATNA", Block: "DANAPUR", Panchayat: "HABI", Village: "MANER", Habitation: "MANER WEST", Parameter: "Arsenic", Year: 2011 },
            { State: "BIHAR", District: "PATNA", Block: "DANAPUR", Panchayat: "HABI", Village: "MANER", Habitation: "MANER EAST", Parameter: "Arsenic", Year: 2011 },
            { State: "BIHAR", District: "GAYA", Block: "BODHGAYA", Panchayat: "AMBA", Village: "MIAN", Habitation: "MIAN PUR", Parameter: "Nitrate", Year: 2012 },
            { State: "ASSAM", District: "JORHAT", Block: "KALIAPANI", Panchayat: "CHINTAMONI", Village: "GELAKONI", Habitation: "NAPALI CHUCK", Parameter: "Iron", Year: 2012 },
            { State: "ASSAM", District: "JORHAT", Block: "KALIAPANI", Panchayat: "CHINTAMONI", Village: "GELAKONI", Habitation: "PATHALIAL CHUCK", Parameter: "Iron", Year: 2012 },
            { State: "ASSAM", District: "JORHAT", Block: "KALIAPANI", Panchayat: "CHINTAMONI", Village: "NOWBOICHA", Habitation: "KHATUAL CHUCK", Parameter: "Iron", Year: 2012 },
            { State: "ASSAM", District: "DIBRUGARH", Block: "LAHOWAL", Panchayat: "MOHAN", Village: "BORBAM", Habitation: "BORBAM MAIN", Parameter: "Iron", Year: 2010 },
            { State: "ORISSA", District: "PURI", Block: "PIPILI", Panchayat: "SATYA", Village: "NUA", Habitation: "NUA SAHI", Parameter: "Salinity", Year: 2011 },
            { State: "ORISSA", District: "PURI", Block: "PIPILI", Panchayat: "SATYA", Village: "NUA", Habitation: "GOPALPUR", Parameter: "Iron", Year: 2012 },
            { State: "KARNATAKA", District: "BANGALORE", Block: "NORTH", Panchayat: "YELAHANKA", Village: "KOGILU", Habitation: "KOGILU VILLAGE", Parameter: "Nitrate", Year: 2010 },
            { State: "RAJASTHAN", District: "JAIPUR", Block: "CHAMPA", Panchayat: "NAGAR", Village: "KHERA", Habitation: "NAGAR SETH", Parameter: "Fluoride", Year: 2012 },
            { State: "ASSAM", District: "JORHAT", Block: "TITABOR", Panchayat: "MELENG", Village: "DAKHIN", Habitation: "MISSING CHUCK", Parameter: "Iron", Year: 2009 },
            { State: "BIHAR", District: "PATNA", Block: "MOKAMA", Panchayat: "BARH", Village: "SHIVAJI", Habitation: "SHIVAJI COLONY", Parameter: "Iron", Year: 2010 },
            { State: "ORISSA", District: "BALASORE", Block: "BHOGRAI", Panchayat: "COASTAL", Village: "TALAPADA", Habitation: "TALAPADA BEACH", Parameter: "Salinity", Year: 2011 }
        ];

        // Global Referensi Chart Instance agar bisa di-destroy & re-render dengan mulus
        let lineChart, donutChart, barChart;

        // Inisialisasi Elemen DOM DOM
        const filterYear = document.getElementById('filter-year');
        const filterState = document.getElementById('filter-state');
        const filterParameter = document.getElementById('filter-parameter');
        const tableBody = document.getElementById('table-body');
        const tableCount = document.getElementById('table-count');

        const kpiTotal = document.getElementById('kpi-total');
        const kpiDominant = document.getElementById('kpi-dominant');
        const kpiDistricts = document.getElementById('kpi-districts');

        // =====================================================================
        // CORE ENGINE: RE-RENDER & FILTER DATA
        // =====================================================================
        function updateDashboard() {
            const yr = filterYear.value;
            const st = filterState.value;
            const pm = filterParameter.value;

            // Operasi Filtering Slicer
            const filteredData = rawDataset.filter(d => {
                const matchYear = (yr === 'All' || d.Year.toString() === yr);
                const matchState = (st === 'All' || d.State === st);
                const matchParam = (pm === 'All' || d.Parameter === pm);
                return matchYear && matchState && matchParam;
            });

            // 1. HITUNG & UPDATE METRIK CARD KPI
            kpiTotal.innerText = filteredData.length.toLocaleString('id-ID');
            
            // Hitung Kabupaten Unik (Distinct Count)
            const uniqueDistricts = [...new Set(filteredData.map(d => d.District))].length;
            kpiDistricts.innerText = uniqueDistricts.toLocaleString('id-ID');

            // Hitung Modus/Zat Dominan
            if(filteredData.length > 0) {
                const freqMap = {};
                filteredData.forEach(d => freqMap[d.Parameter] = (freqMap[d.Parameter] || 0) + 1);
                const sortedParams = Object.keys(freqMap).sort((a,b) => freqMap[b] - freqMap[a]);
                kpiDominant.innerText = sortedParams[0].toUpperCase();
            } else {
                kpiDominant.innerText = "N/A";
            }

            // 2. BUILD VISUAL 1: TREN LINE CHART (Agregasi Kasus Per Tahun)
            const yearsList = [2009, 2010, 2011, 2012];
            const lineDataPoints = yearsList.map(y => {
                // Tren sengaja tidak dikunci total oleh filter tahun agar chart garisnya tetap terbentuk linier
                return rawDataset.filter(d => d.Year === y && 
                    (st === 'All' || d.State === st) && 
                    (pm === 'All' || d.Parameter === pm)
                ).length;
            });
            renderLineChart(yearsList, lineDataPoints);

            // 3. BUILD VISUAL 2: PROPORSI DONUT CHART
            const donutMap = {};
            filteredData.forEach(d => donutMap[d.Parameter] = (donutMap[d.Parameter] || 0) + 1);
            renderDonutChart(Object.keys(donutMap), Object.values(donutMap));

            // 4. BUILD VISUAL 3: RANKING BAR CHART (Berdasarkan Wilayah State)
            const barMap = {};
            filteredData.forEach(d => barMap[d.State] = (barMap[d.State] || 0) + 1);
            const sortedBarStates = Object.keys(barMap).sort((a,b) => barMap[b] - barMap[a]);
            const barDataValues = sortedBarStates.map(s => barMap[s]);
            renderBarChart(sortedBarStates, barDataValues);

            // 5. RENDER DATAFRAME / TABEL DETAIL
            tableBody.innerHTML = "";
            tableCount.innerText = `${filteredData.length} baris ditemukan`;
            
            if (filteredData.length === 0) {
                tableBody.innerHTML = `<tr><td colspan="7" class="p-4 text-center text-gray-500 italic">Tidak ada data yang cocok dengan kriteria filter.</td></tr>`;
            } else {
                filteredData.forEach(d => {
                    const row = document.createElement('tr');
                    row.className = "hover:bg-gray-750 transition";
                    row.innerHTML = `
                        <td class="p-4 text-white font-medium">${d.State}</td>
                        <td class="p-4 text-gray-300">${d.District}</td>
                        <td class="p-4 text-gray-400">${d.Block}</td>
                        <td class="p-4 text-gray-400">${d.Panchayat}</td>
                        <td class="p-4 text-gray-400">${d.Village}</td>
                        <td class="p-4 text-gray-400 font-mono text-xs">${d.Habitation}</td>
                        <td class="p-4"><span class="px-2 py-1 rounded text-xs font-bold ${getBadgeColor(d.Parameter)}">${d.Parameter}</span></td>
                    `;
                    tableBody.appendChild(row);
                });
            }
        }

        // Helper Pewarnaan Badge Kualitas Air yang Kontras
        function getBadgeColor(param) {
            switch(param) {
                case 'Iron': return 'bg-red-900 text-red-200 border border-red-700';
                case 'Fluoride': return 'bg-amber-900 text-amber-200 border border-amber-700';
                case 'Salinity': return 'bg-blue-900 text-blue-200 border border-blue-700';
                case 'Arsenic': return 'bg-purple-900 text-purple-200 border border-purple-700';
                default: return 'bg-green-900 text-green-200 border border-green-700';
            }
        }

        // =====================================================================
        // RE-RENDER CHART FUNCTIONS (CHART.JS CONFIGS)
        // =====================================================================
        function renderLineChart(labels, dataPoints) {
            if (lineChart) lineChart.destroy();
            const ctx = document.getElementById('chartLine').getContext('2d');
            lineChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Jumlah Pemukiman Terdampak',
                        data: dataPoints,
                        borderColor: '#3b82f6',
                        backgroundColor: 'rgba(59, 130, 246, 0.1)',
                        borderWidth: 3,
                        fill: true,
                        tension: 0.2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: '#374151' }, ticks: { color: '#9ca3af' } },
                        x: { grid: { display: false }, ticks: { color: '#9ca3af' } }
                    }
                }
            });
        }

        function renderDonutChart(labels, dataPoints) {
            if (donutChart) donutChart.destroy();
            const ctx = document.getElementById('chartDonut').getContext('2d');
            donutChart = new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: labels,
                    datasets: [{
                        data: dataPoints,
                        backgroundColor: ['#ef4444', '#f59e0b', '#3b82f6', '#a855f7', '#10b981'],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: { position: 'right', labels: { color: '#d1d5db', font: { size: 11 } } }
                    }
                }
            });
        }

        function renderBarChart(labels, dataPoints) {
            if (barChart) barChart.destroy();
            const ctx = document.getElementById('chartBar').getContext('2d');
            barChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        data: dataPoints,
                        backgroundColor: '#e74c3c',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        y: { grid: { color: '#374151' }, ticks: { color: '#9ca3af' } },
                        x: { grid: { display: false }, ticks: { color: '#9ca3af' } }
                    }
                }
            });
        }

        // =====================================================================
        // EVENT LISTENERS & INITIALIZATION
        // =====================================================================
        filterYear.addEventListener('change', updateDashboard);
        filterState.addEventListener('change', updateDashboard);
        filterParameter.addEventListener('change', updateDashboard);

        document.getElementById('reset-btn').addEventListener('click', () => {
            filterYear.value = 'All';
            filterState.value = 'All';
            filterParameter.value = 'All';
            updateDashboard();
        });

        // Jalankan render dashboard pertama kali saat halaman terbuka
        window.addEventListener('DOMContentLoaded', updateDashboard);
    </script>
</body>
</html>
