/**
 * AI Legal Document Summarization System — Frontend Logic
 * Handles file upload, API communication, and result rendering.
 */

(function () {
    'use strict';

    // ─── DOM Elements ──────────────────────────────────────────────────
    const dropzone = document.getElementById('dropzone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const fileName = document.getElementById('file-name');
    const fileSize = document.getElementById('file-size');
    const fileRemove = document.getElementById('file-remove');
    const submitBtn = document.getElementById('submit-btn');
    const uploadForm = document.getElementById('upload-form');

    const uploadSection = document.getElementById('upload-section');
    const loadingSection = document.getElementById('loading-section');
    const resultsSection = document.getElementById('results-section');
    const errorSection = document.getElementById('error-section');

    const loadingStatus = document.getElementById('loading-status');
    const stepExtract = document.getElementById('step-extract');
    const stepEntity = document.getElementById('step-entity');
    const stepSummarize = document.getElementById('step-summarize');

    const newAnalysisBtn = document.getElementById('new-analysis-btn');
    const errorRetryBtn = document.getElementById('error-retry-btn');
    const errorMessage = document.getElementById('error-message');

    let selectedFile = null;

    // ─── Utility ───────────────────────────────────────────────────────
    function formatBytes(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + ' ' + sizes[i];
    }

    function formatNumber(num) {
        if (num >= 1000) return (num / 1000).toFixed(1) + 'K';
        return num.toString();
    }

    function showSection(section) {
        [uploadSection, loadingSection, resultsSection, errorSection].forEach(s => {
            s.style.display = 'none';
        });
        section.style.display = 'block';
    }

    // ─── Dropzone Events ───────────────────────────────────────────────
    dropzone.addEventListener('click', () => fileInput.click());

    dropzone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropzone.classList.add('drag-over');
    });

    dropzone.addEventListener('dragleave', () => {
        dropzone.classList.remove('drag-over');
    });

    dropzone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropzone.classList.remove('drag-over');
        if (e.dataTransfer.files.length > 0) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFile(fileInput.files[0]);
        }
    });

    function handleFile(file) {
        const validTypes = ['.pdf', '.docx', '.txt'];
        const ext = '.' + file.name.split('.').pop().toLowerCase();

        if (!validTypes.includes(ext)) {
            alert('Unsupported file type. Please upload PDF, DOCX, or TXT files.');
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            alert('File too large. Maximum size is 16 MB.');
            return;
        }

        selectedFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = formatBytes(file.size);
        fileInfo.style.display = 'flex';
        submitBtn.disabled = false;
    }

    fileRemove.addEventListener('click', () => {
        selectedFile = null;
        fileInput.value = '';
        fileInfo.style.display = 'none';
        submitBtn.disabled = true;
    });

    // ─── Form Submit ───────────────────────────────────────────────────
    uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!selectedFile) return;

        const mode = document.querySelector('input[name="mode"]:checked').value;

        // Show loading
        showSection(loadingSection);
        animateLoadingSteps();

        // Build form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        formData.append('mode', mode);

        try {
            const response = await fetch('/api/summarize', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Server error occurred.');
            }

            renderResults(data);
            showSection(resultsSection);
        } catch (err) {
            errorMessage.textContent = err.message || 'An unexpected error occurred.';
            showSection(errorSection);
        }
    });

    // ─── Loading Animation ─────────────────────────────────────────────
    function animateLoadingSteps() {
        const steps = [stepExtract, stepEntity, stepSummarize];
        const messages = [
            'Parsing document structure...',
            'Extracting legal intelligence...',
            'Performing document synthesis...'
        ];

        steps.forEach(s => { s.className = 'step'; });
        steps[0].classList.add('active');
        loadingStatus.textContent = messages[0];

        let current = 0;
        const interval = setInterval(() => {
            if (current < steps.length - 1) {
                steps[current].classList.remove('active');
                steps[current].classList.add('done');
                current++;
                steps[current].classList.add('active');
                loadingStatus.textContent = messages[current];
            } else {
                clearInterval(interval);
            }
        }, 2000);
    }

    // ─── Render Results ────────────────────────────────────────────────
    function renderResults(data) {
        // Stats
        document.getElementById('stat-words').textContent = formatNumber(data.word_count || 0);
        document.getElementById('stat-sentences').textContent = formatNumber(data.sentence_count || 0);
        document.getElementById('stat-chars').textContent = formatNumber(data.text_length || 0);

        // Count total entities
        const entities = data.entities || {};
        let totalEntities = 0;
        Object.values(entities).forEach(arr => {
            if (Array.isArray(arr)) totalEntities += arr.length;
        });
        document.getElementById('stat-entities').textContent = totalEntities;

        // Description
        document.getElementById('results-desc').textContent =
            `Analysis of "${data.filename}" — ${data.language} Document (${data.word_count} words)`;

        // Entities
        renderEntities(entities);

        // Extractive summary
        const extractivePanel = document.getElementById('extractive-panel');
        if (data.summary && data.summary.extractive) {
            document.getElementById('extractive-text').textContent = data.summary.extractive;
            extractivePanel.style.display = 'block';
        } else {
            extractivePanel.style.display = 'none';
        }

        // Abstractive summary
        const abstractivePanel = document.getElementById('abstractive-panel');
        if (data.summary && data.summary.abstractive) {
            document.getElementById('abstractive-text').textContent = data.summary.abstractive;
            abstractivePanel.style.display = 'block';
        } else {
            abstractivePanel.style.display = 'none';
        }

        // Original text
        document.getElementById('original-text').textContent = data.original_text || '';
    }

    function renderEntities(entities) {
        const container = document.getElementById('entities-content');
        container.innerHTML = '';

        const groups = [
            { key: 'persons', label: '👤 Persons', className: 'person' },
            { key: 'organizations', label: '🏛️ Organizations', className: 'org' },
            { key: 'dates', label: '📅 Dates', className: 'date' },
            { key: 'locations', label: '📍 Locations', className: 'location' },
            { key: 'case_numbers', label: '📂 Case Numbers', className: 'case-number' },
            { key: 'law_sections', label: '⚖️ Law Sections', className: 'law-section' },
        ];

        let hasAny = false;

        groups.forEach(group => {
            const items = entities[group.key];
            if (!items || !Array.isArray(items) || items.length === 0) return;

            hasAny = true;
            const groupDiv = document.createElement('div');
            groupDiv.className = 'entity-group';

            const label = document.createElement('div');
            label.className = 'entity-group-label';
            label.textContent = group.label;
            groupDiv.appendChild(label);

            const tagsDiv = document.createElement('div');
            tagsDiv.className = 'entity-tags';

            items.forEach(item => {
                const tag = document.createElement('span');
                tag.className = `entity-tag ${group.className}`;
                tag.textContent = item;
                tagsDiv.appendChild(tag);
            });

            groupDiv.appendChild(tagsDiv);
            container.appendChild(groupDiv);
        });

        if (!hasAny) {
            container.innerHTML = '<p class="no-entities">No entities identified in this document.</p>';
        }
    }

    // ─── Panel Toggles ─────────────────────────────────────────────────
    document.querySelectorAll('.panel-toggle').forEach(btn => {
        btn.addEventListener('click', () => {
            const targetId = btn.getAttribute('data-target');
            const content = document.getElementById(targetId);
            if (content) {
                content.classList.toggle('collapsed');
                btn.style.transform = content.classList.contains('collapsed')
                    ? 'rotate(0deg)' : 'rotate(180deg)';
            }
        });
    });

    // ─── Reset / Retry ─────────────────────────────────────────────────
    function resetToUpload() {
        selectedFile = null;
        fileInput.value = '';
        fileInfo.style.display = 'none';
        submitBtn.disabled = true;
        showSection(uploadSection);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    newAnalysisBtn.addEventListener('click', resetToUpload);
    errorRetryBtn.addEventListener('click', resetToUpload);

})();
