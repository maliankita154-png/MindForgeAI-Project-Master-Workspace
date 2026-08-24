(() => {
    "use strict";

    /* =========================================================
       AETHERA COMMAND CENTER
       Real 2025 / 2026 data + Charts + Search + Filters
       ========================================================= */

    const DATA = window.AETHERA_DATA || {};

    let rainfallChart = null;
    let waterChart = null;
    let reservoirChart = null;
    let comparisonChart = null;

    /* =========================================================
       HELPERS
       ========================================================= */

    function number(value) {
        if (value === null || value === undefined || value === "") {
            return 0;
        }

        const n = Number(
            String(value)
                .replace(/,/g, "")
                .replace(/[^\d.-]/g, "")
        );

        return Number.isFinite(n) ? n : 0;
    }


    function text(value) {
        if (value === null || value === undefined) {
            return "";
        }

        return String(value);
    }


    function monthName(value) {

        const months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ];

        if (typeof value === "number") {
            return months[value - 1] || "";
        }

        const str = text(value).trim();

        if (!str) {
            return "";
        }

        const date = new Date(str);

        if (!isNaN(date.getTime())) {
            return months[date.getMonth()];
        }

        const lower = str.toLowerCase();

        const found = months.find(
            m => lower.includes(m.toLowerCase())
        );

        return found || str;
    }


    function yearFrom(value) {

        const match = text(value).match(/\b(20\d{2})\b/);

        return match ? match[1] : "";
    }


    /* =========================================================
       NORMALISE RAINFALL
       ========================================================= */

    function getRainfallData() {

        const result = [];

        const sources = [
            DATA.rainfall2025,
            DATA.rainfall2026,
            DATA.rainfallCompare
        ];

        sources.forEach(source => {

            if (!source) {
                return;
            }

            if (Array.isArray(source)) {

                source.forEach(row => {

                    if (!row) {
                        return;
                    }

                    const date =
                        row.date ||
                        row.Date ||
                        row.month ||
                        row.Month ||
                        "";

                    const rainfall =
                        row.rainfall_mm ??
                        row.rainfall ??
                        row.Rainfall ??
                        row.value ??
                        0;

                    result.push({
                        date: text(date),
                        year:
                            yearFrom(date) ||
                            text(row.year || row.Year),
                        month:
                            monthName(
                                row.month ||
                                row.Month ||
                                date
                            ),
                        rainfall: number(rainfall)
                    });

                });

            }

            else if (
                typeof source === "object"
            ) {

                Object.entries(source).forEach(
                    ([key, value]) => {

                        if (Array.isArray(value)) {

                            value.forEach(row => {

                                if (
                                    typeof row === "object"
                                ) {

                                    result.push({
                                        date:
                                            text(
                                                row.date ||
                                                row.month ||
                                                key
                                            ),

                                        year:
                                            text(
                                                row.year ||
                                                yearFrom(key)
                                            ),

                                        month:
                                            monthName(
                                                row.month ||
                                                key
                                            ),

                                        rainfall:
                                            number(
                                                row.rainfall_mm ??
                                                row.rainfall ??
                                                row.value ??
                                                0
                                            )
                                    });

                                }

                            });

                        }

                        else {

                            result.push({
                                date: key,
                                year: yearFrom(key),
                                month: monthName(key),
                                rainfall: number(value)
                            });

                        }

                    }
                );

            }

        });

        return result;
    }


    /* =========================================================
       NORMALISE WATER USE
       ========================================================= */

    function getWaterData() {

        const rows = [];

        const source = [
            ...(DATA.water2025 || []),
            ...(DATA.water2026 || DATA.waterUse2026 || [])
        ];

        if (Array.isArray(source)) {

            source.forEach(row => {

                if (!row) {
                    return;
                }

                rows.push({

                    year:
                        text(
                            row.year ||
                            row.Year ||
                            yearFrom(row.date)
                        ),

                    month:
                        text(
                            row.month ||
                            row.Month ||
                            row.date ||
                            ""
                        ),

                    agriculture:
                        number(
                            row.agriculture_mcm ??
                            row.agriculture ??
                            0
                        ),

                    industry:
                        number(
                            row.industry_mcm ??
                            row.industry ??
                            0
                        ),

                    domestic:
                        number(
                            row.domestic_mcm ??
                            row.domestic ??
                            0
                        ),

                    animal:
                        number(
                            row.animal_husbandry_mcm ??
                            row.animal_mcm ??
                            row.animal ??
                            0
                        ),

                    power:
                        number(
                            row.power_mcm ??
                            row.power ??
                            0
                        ),

                    environment:
                        number(
                            row.environment_mcm ??
                            row.environment ??
                            0
                        ),

                    total:
                        number(
                            row.total_use_mcm ??
                            row.total ??
                            0
                        )

                });

            });

        }

        return rows;
    }


    /* =========================================================
       NORMALISE RESERVOIR
       ========================================================= */

    function getReservoirData() {

        const result = [];

        const source =
            DATA.reservoirCompare ||
            DATA.reservoir2026 ||
            [];

        if (Array.isArray(source)) {

            source.forEach(row => {

                if (!row) {
                    return;
                }

                result.push({

                    date:
                        text(
                            row.date ||
                            row.Date ||
                            row.month ||
                            ""
                        ),

                    year:
                        text(
                            row.year ||
                            yearFrom(row.date)
                        ),

                    level:
                        number(
                            row.storage_pct ??
                            row.reservoir ??
                            row.level ??
                            row.storage ??
                            0
                        )

                });

            });

        }

        else if (
            typeof source === "object"
        ) {

            Object.entries(source).forEach(
                ([key, value]) => {

                    result.push({

                        date: key,

                        year: yearFrom(key),

                        level: number(
                            typeof value === "object"
                                ? (
                                    value.storage_pct ??
                                    value.reservoir ??
                                    value.level ??
                                    0
                                )
                                : value
                        )

                    });

                }
            );

        }

        return result;
    }


    /* =========================================================
       CHART DESTROY
       ========================================================= */

    function destroy(chart) {

        if (chart) {
            chart.destroy();
        }

    }


    /* =========================================================
       COMMON CHART OPTIONS
       ========================================================= */

    const commonOptions = {

        responsive: true,

        maintainAspectRatio: false,

        interaction: {
            mode: "index",
            intersect: false
        },

        plugins: {

            legend: {
                display: true
            },

            tooltip: {
                enabled: true
            }

        }

    };


    /* =========================================================
       RAINFALL CHART
       ========================================================= */

    function createRainfallChart() {

        const canvas =
            document.getElementById("rainfallChart");

        if (!canvas || !window.Chart) {
            return;
        }

        const data =
            getRainfallData();

        destroy(rainfallChart);

        const months = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December"
        ];

        const years = ["2025", "2026"];

        const datasets = [];

        years.forEach(year => {

            const values =
                months.map(month => {

                    const records =
                        data.filter(
                            row =>
                                row.year === year &&
                                row.month === month
                        );

                    if (!records.length) {
                        return 0;
                    }

                    return records.reduce(
                        (sum, row) =>
                            sum + row.rainfall,
                        0
                    );

                });

            datasets.push({

                label: `${year} Rainfall`,

                data: values,

                tension: 0.35,

                fill: false,

                borderWidth: 3,

                pointRadius: 4

            });

        });


        rainfallChart =
            new Chart(
                canvas.getContext("2d"),
                {

                    type: "line",

                    data: {
                        labels: months,
                        datasets: datasets
                    },

                    options: {

                        ...commonOptions,

                        scales: {

                            y: {
                                beginAtZero: true,

                                title: {
                                    display: true,
                                    text: "Rainfall (mm)"
                                }
                            }

                        }

                    }

                }
            );

    }


    /* =========================================================
       WATER USE CHART
       ========================================================= */

    function createWaterChart() {

        /*
         IMPORTANT:
         HTML has waterChart.
         Previous JS was searching waterUseChart.
        */

        const canvas =
            document.getElementById("waterChart");

        if (!canvas || !window.Chart) {
            return;
        }

        const rows =
            getWaterData();

        destroy(waterChart);

        const totals = {

            Agriculture: 0,

            Industry: 0,

            Domestic: 0,

            "Animal Husbandry": 0,

            Power: 0,

            Environment: 0

        };


        rows.forEach(row => {

            totals.Agriculture += row.agriculture;

            totals.Industry += row.industry;

            totals.Domestic += row.domestic;

            totals["Animal Husbandry"] +=
                row.animal;

            totals.Power += row.power;

            totals.Environment +=
                row.environment;

        });


        waterChart =
            new Chart(
                canvas.getContext("2d"),
                {

                    type: "bar",

                    data: {

                        labels:
                            Object.keys(totals),

                        datasets: [

                            {

                                label:
                                    "Water Use (MCM)",

                                data:
                                    Object.values(totals),

                                borderWidth: 1,

                                borderRadius: 8

                            }

                        ]

                    },

                    options: {

                        ...commonOptions,

                        plugins: {

                            legend: {
                                display: false
                            }

                        },

                        scales: {

                            y: {

                                beginAtZero: true,

                                title: {
                                    display: true,
                                    text: "Water Use (MCM)"
                                }

                            }

                        }

                    }

                }
            );

    }


    /* =========================================================
       RESERVOIR CHART
       ========================================================= */

    function createReservoirChart() {

        const canvas =
            document.getElementById(
                "reservoirChart"
            );

        if (!canvas || !window.Chart) {
            return;
        }

        const data =
            getReservoirData();

        destroy(reservoirChart);


        const labels =
            data.map(row => row.date);

        const values =
            data.map(row => row.level);


        reservoirChart =
            new Chart(
                canvas.getContext("2d"),
                {

                    type: "line",

                    data: {

                        labels: labels,

                        datasets: [

                            {

                                label:
                                    "Reservoir Storage (%)",

                                data: values,

                                tension: 0.35,

                                fill: true,

                                borderWidth: 3,

                                pointRadius: 3

                            }

                        ]

                    },

                    options: {

                        ...commonOptions,

                        scales: {

                            y: {

                                beginAtZero: true,

                                max: 100,

                                title: {

                                    display: true,

                                    text:
                                        "Storage (%)"

                                }

                            }

                        }

                    }

                }
            );

    }


    /* =========================================================
       2025 vs 2026 COMPARISON
       ========================================================= */

    function createComparisonChart() {

        const canvas =
            document.getElementById(
                "comparisonChart"
            );

        if (!canvas || !window.Chart) {
            return;
        }

        destroy(comparisonChart);

        const rainfall =
            getRainfallData();

        const water =
            getWaterData();


        const rainfall2025 =
            rainfall
                .filter(r => r.year === "2025")
                .reduce(
                    (sum, r) =>
                        sum + r.rainfall,
                    0
                );


        const rainfall2026 =
            rainfall
                .filter(r => r.year === "2026")
                .reduce(
                    (sum, r) =>
                        sum + r.rainfall,
                    0
                );


        const waterTotal =
            water.reduce(
                (sum, r) =>
                    sum + r.total,
                0
            );


        comparisonChart =
            new Chart(
                canvas.getContext("2d"),
                {

                    type: "bar",

                    data: {

                        labels: [
                            "Rainfall",
                            "Water Use"
                        ],

                        datasets: [

                            {

                                label: "2025",

                                data: [
                                    rainfall2025,
                                    0
                                ],

                                borderWidth: 1,

                                borderRadius: 8

                            },

                            {

                                label: "2026",

                                data: [
                                    rainfall2026,
                                    waterTotal
                                ],

                                borderWidth: 1,

                                borderRadius: 8

                            }

                        ]

                    },

                    options: {

                        ...commonOptions,

                        scales: {

                            y: {
                                beginAtZero: true
                            }

                        }

                    }

                }
            );

    }


    /* =========================================================
       SEARCH
       ========================================================= */

    const searchInput =
        document.getElementById(
            "aetheraSearch"
        ) ||
        document.getElementById(
            "waterSearch"
        );


    const searchButton =
        document.getElementById(
            "aetheraSearchButton"
        ) ||
        document.getElementById(
            "searchButton"
        );


    const searchResults =
        document.getElementById(
            "aetheraSearchResults"
        ) ||
        document.getElementById(
            "searchResults"
        );


    function searchData() {

        if (!searchInput || !searchResults) {
            return;
        }

        const query =
            searchInput.value
                .trim()
                .toLowerCase();


        if (!query) {

            searchResults.hidden = true;

            searchResults.innerHTML = "";

            return;
        }


        const rainfall =
            getRainfallData();

        const water =
            getWaterData();

        const reservoir =
            getReservoirData();


        const results = [];


        rainfall.forEach(row => {

            const searchable =
                `${row.date}
                 ${row.year}
                 ${row.month}
                 rainfall
                 ${row.rainfall}
                 mm`.toLowerCase();

            if (
                searchable.includes(query)
            ) {

                results.push({

                    type: "RAINFALL",

                    text:
                        `${row.date || row.month}
                         | ${row.year}
                         | Rainfall:
                         ${row.rainfall} mm`

                });

            }

        });


        water.forEach(row => {

            const searchable =
                `${row.year}
                 ${row.month}
                 water
                 water use
                 agriculture
                 industry
                 domestic
                 animal
                 power
                 environment
                 ${row.agriculture}
                 ${row.industry}
                 ${row.domestic}
                 ${row.animal}
                 ${row.power}
                 ${row.environment}
                 ${row.total}`.toLowerCase();


            if (
                searchable.includes(query)
            ) {

                results.push({

                    type: "WATER USE",

                    text:
                        `${row.month}
                         | Agriculture:
                         ${row.agriculture} MCM
                         | Industry:
                         ${row.industry} MCM
                         | Domestic:
                         ${row.domestic} MCM
                         | Total:
                         ${row.total} MCM`

                });

            }

        });


        reservoir.forEach(row => {

            const searchable =
                `${row.date}
                 ${row.year}
                 reservoir
                 storage
                 ${row.level}`.toLowerCase();


            if (
                searchable.includes(query)
            ) {

                results.push({

                    type: "RESERVOIR",

                    text:
                        `${row.date}
                         | ${row.year}
                         | Reservoir:
                         ${row.level}%`

                });

            }

        });


        searchResults.hidden = false;


        if (!results.length) {

            searchResults.innerHTML = `

                <div class="search-result">

                    <strong>
                        No matching data found
                    </strong>

                    <p>
                        Try:
                        <b>2025</b>,
                        <b>2026</b>,
                        <b>rainfall</b>,
                        <b>agriculture</b>,
                        <b>reservoir</b>
                        or a month name.
                    </p>

                </div>

            `;

            return;
        }


        searchResults.innerHTML = `

            <div class="search-result">

                <strong>
                    ${results.length}
                    matching record(s)
                </strong>

            </div>

            ${results
                .slice(0, 20)
                .map(result => `

                    <div class="search-result">

                        <strong>
                            ${result.type}
                        </strong>

                        <div class="search-result-data">
                            ${result.text.replace(/\s*\|\s*/g, "<br>")}
                        </div>

                    </div>

                `)
                .join("")
            }

        `;

    }


    if (searchButton) {

        searchButton.addEventListener(
            "click",
            searchData
        );

    }


    if (searchInput) {

        searchInput.addEventListener(
            "keydown",
            event => {

                if (event.key === "Enter") {
                    searchData();
                }

            }
        );

    }


    /* =========================================================
       FILTERS
       ========================================================= */

    const yearFilter =
        document.getElementById("yearFilter") ||
        document.getElementById("aetheraYear");


    const monthFilter =
        document.getElementById("monthFilter") ||
        document.getElementById("aetheraMonth");


    const datasetFilter =
        document.getElementById("dataFilter") ||
        document.getElementById("aetheraDataset");


    const resetButton =
        document.getElementById("resetFilters") ||
        document.getElementById("aetheraReset");


    function applyFilters() {

        const year =
            yearFilter?.value || "all";

        const month =
            monthFilter?.value || "all";

        const dataset =
            datasetFilter?.value || "all";


        const rainfall =
            getRainfallData();

        const water =
            getWaterData();

        const reservoir =
            getReservoirData();


        /*
           Filter table rows visually.
        */

        document
            .querySelectorAll(
                ".data-table tbody tr"
            )
            .forEach(row => {

                const rowText =
                    row.innerText.toLowerCase();

                let visible = true;


                if (
                    year !== "all" &&
                    !rowText.includes(year)
                ) {

                    /*
                       2026 table has no year column,
                       therefore keep it for 2026.
                    */

                    if (
                        year !== "2026"
                    ) {
                        visible = false;
                    }

                }


                if (
                    month !== "all" &&
                    !rowText.includes(
                        month.toLowerCase()
                    )
                ) {

                    visible = false;

                }


                row.style.display =
                    visible ? "" : "none";

            });


        updateInsight(
            year,
            month,
            dataset
        );

    }


    if (yearFilter) {

        yearFilter.addEventListener(
            "change",
            applyFilters
        );

    }


    if (monthFilter) {

        monthFilter.addEventListener(
            "change",
            applyFilters
        );

    }


    if (datasetFilter) {

        datasetFilter.addEventListener(
            "change",
            applyFilters
        );

    }


    if (resetButton) {

        resetButton.addEventListener(
            "click",
            () => {

                if (yearFilter) {
                    yearFilter.value = "all";
                }

                if (monthFilter) {
                    monthFilter.value = "all";
                }

                if (datasetFilter) {
                    datasetFilter.value = "all";
                }

                if (searchInput) {
                    searchInput.value = "";
                }

                if (searchResults) {

                    searchResults.hidden =
                        true;

                    searchResults.innerHTML =
                        "";

                }

                document
                    .querySelectorAll(
                        ".data-table tbody tr"
                    )
                    .forEach(row => {
                        row.style.display = "";
                    });

                updateInsight(
                    "all",
                    "all",
                    "all"
                );

            }
        );

    }


    /* =========================================================
       AI INSIGHT
       ========================================================= */

    function updateInsight(
        year,
        month,
        dataset
    ) {

        const title =
            document.getElementById(
                "aetheraInsightTitle"
            ) ||
            document.getElementById(
                "insightTitle"
            );


        const message =
            document.getElementById(
                "aetheraInsight"
            ) ||
            document.getElementById(
                "insightText"
            );


        if (!title || !message) {
            return;
        }


        let period =
            "all available data";


        if (year !== "all") {
            period = year;
        }


        if (month !== "all") {
            period += ` — ${month}`;
        }


        let focus =
            "rainfall, water demand, reservoir levels and sector-wise water use";


        if (dataset === "rainfall") {
            focus = "rainfall patterns";
        }

        if (dataset === "water") {
            focus = "sector-wise water utilization";
        }

        if (dataset === "reservoir") {
            focus = "reservoir storage conditions";
        }


        title.textContent =
            `Water intelligence — ${period}`;


        message.textContent =
            `AETHERA is analysing ${focus} for ${period}. ` +
            `Use Search to find specific records or use ` +
            `the filters to compare the available data.`;

    }


    /* =========================================================
       INITIALISE
       ========================================================= */

    function initialise() {

        console.log(
            "AETHERA DATA:",
            DATA
        );


        createRainfallChart();

        createWaterChart();

        createReservoirChart();

        createComparisonChart();


        updateInsight(
            "all",
            "all",
            "all"
        );


        /*
           Small diagnostic message in console.
        */

        console.log(
            "Rainfall records:",
            getRainfallData().length
        );

        console.log(
            "Water records:",
            getWaterData().length
        );

        console.log(
            "Reservoir records:",
            getReservoirData().length
        );

    }


    if (
        document.readyState === "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            initialise
        );

    }
    else {

        initialise();

    }

})();