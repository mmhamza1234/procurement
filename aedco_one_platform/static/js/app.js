/**
 * AEDCO One Platform — Newsletter Editor Frontend
 * Handles sector selection, newsletter generation, and preview functionality
 */

class AEDCOPlatform {
    constructor() {
        this.selectedSector = null;
        this.currentMode = 'test';
        this.generationInProgress = false;
        this.currentRun = null;
        
        this.initializeEventListeners();
        this.initializeSectors();
        this.updateCairoTime();
        this.updateDateInfo();
        
        // Update Cairo time every minute
        setInterval(() => this.updateCairoTime(), 60000);
    }
    
    initializeEventListeners() {
        // Mode toggle
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setMode(e.target.dataset.mode);
            });
        });
        
        // Generate button
        document.getElementById('generate-btn').addEventListener('click', () => {
            this.generateNewsletter();
        });
        
        // File upload
        this.initializeFileUpload();
        
        // Download buttons
        document.getElementById('download-principals').addEventListener('click', () => {
            this.downloadFile('Principals');
        });
        
        document.getElementById('download-egyptian').addEventListener('click', () => {
            this.downloadFile('Egyptian Clients');
        });
        
        document.getElementById('download-all-btn').addEventListener('click', () => {
            this.downloadAllFiles();
        });
    }
    
    initializeSectors() {
        const container = document.getElementById('sectors-container');
        const uploadSector = document.getElementById('upload-sector');
        
        // Get sectors from backend
        this.fetchSectors().then(sectors => {
            Object.entries(sectors).forEach(([key, sector]) => {
                // Create sector card
                const sectorCard = this.createSectorCard(key, sector);
                container.appendChild(sectorCard);
                
                // Add to upload dropdown
                const option = document.createElement('option');
                option.value = key;
                option.textContent = sector.name;
                uploadSector.appendChild(option);
            });
        });
    }
    
    createSectorCard(key, sector) {
        const card = document.createElement('div');
        card.className = 'sector-card';
        card.dataset.sector = key;
        
        const icon = this.getSectorIcon(key);
        
        card.innerHTML = `
            <div class="sector-icon">
                <i class="fas ${icon}"></i>
            </div>
            <h6 class="mb-1">${sector.name}</h6>
            <small class="text-muted">${sector.sections.length} sections</small>
        `;
        
        card.addEventListener('click', () => {
            this.selectSector(key, sector);
        });
        
        return card;
    }
    
    getSectorIcon(sectorKey) {
        const icons = {
            'oil_gas': 'fa-oil-can',
            'transportation': 'fa-train',
            'electricity': 'fa-bolt'
        };
        return icons[sectorKey] || 'fa-layer-group';
    }
    
    selectSector(key, sector) {
        // Remove previous selection
        document.querySelectorAll('.sector-card').forEach(card => {
            card.classList.remove('selected');
        });
        
        // Select new sector
        document.querySelector(`[data-sector="${key}"]`).classList.add('selected');
        this.selectedSector = key;
        
        // Update UI
        this.updateSelectedSectorInfo(sector);
        this.updateDateInfo();
        this.enableGenerateButton();
        this.loadPastIssues(key);
        
        // Update upload sector
        document.getElementById('upload-sector').value = key;
    }
    
    updateSelectedSectorInfo(sector) {
        const container = document.getElementById('selected-sector-info');
        container.style.display = 'block';
        
        container.innerHTML = `
            <div class="d-flex align-items-center">
                <i class="fas ${this.getSectorIcon(this.selectedSector)} me-2"></i>
                <div>
                    <strong>${sector.name}</strong>
                    <br>
                    <small class="text-muted">${sector.sections.length} sections configured</small>
                </div>
            </div>
        `;
    }
    
    setMode(mode) {
        this.currentMode = mode;
        
        // Update UI
        document.querySelectorAll('.mode-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.mode === mode);
        });
        
        // Update description
        const description = document.getElementById('mode-description');
        if (mode === 'production') {
            description.textContent = 'Production: Next Monday 09:00 Africa/Cairo';
        } else {
            description.textContent = 'Test: Generates for next 09:00 Africa/Cairo';
        }
        
        this.updateDateInfo();
    }
    
    updateDateInfo() {
        if (!this.selectedSector) return;
        
        // Calculate dates based on mode
        const now = new Date();
        let displayDate, cutoffDate;
        
        if (this.currentMode === 'production') {
            // Next Monday at 09:00
            const daysUntilMonday = (8 - now.getDay()) % 7;
            const monday = new Date(now);
            monday.setDate(now.getDate() + daysUntilMonday);
            monday.setHours(9, 0, 0, 0);
            
            displayDate = monday;
            cutoffDate = new Date(monday);
            cutoffDate.setHours(8, 0, 0, 0);
        } else {
            // Next 09:00
            const today9am = new Date(now);
            today9am.setHours(9, 0, 0, 0);
            
            if (now < today9am) {
                displayDate = today9am;
            } else {
                displayDate = new Date(today9am);
                displayDate.setDate(today9am.getDate() + 1);
            }
            
            cutoffDate = new Date(displayDate);
            cutoffDate.setHours(8, 0, 0, 0);
        }
        
        // Update UI
        document.getElementById('display-date').textContent = displayDate.toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        document.getElementById('cutoff-date').textContent = cutoffDate.toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
    
    updateCairoTime() {
        // Simulate Cairo time (in real app, this would come from backend)
        const now = new Date();
        const cairoTime = new Date(now.getTime() + (2 * 60 * 60 * 1000)); // UTC+2
        
        document.getElementById('cairo-time').textContent = cairoTime.toLocaleTimeString('en-US', {
            timeZone: 'Africa/Cairo',
            hour12: false,
            hour: '2-digit',
            minute: '2-digit'
        }) + ' Africa/Cairo';
    }
    
    enableGenerateButton() {
        const btn = document.getElementById('generate-btn');
        btn.disabled = false;
        btn.innerHTML = '<i class="fas fa-magic me-2"></i>Generate Newsletter';
    }
    
    async generateNewsletter() {
        if (!this.selectedSector || this.generationInProgress) return;
        
        this.generationInProgress = true;
        this.showProgress();
        this.updateStatus('Starting newsletter generation...', 'generating');
        
        try {
            const response = await axios.post('/api/generate', {
                sector: this.selectedSector,
                mode: this.currentMode
            });
            
            if (response.data.success) {
                this.currentRun = response.data;
                this.updateStatus('Newsletter generated successfully!', 'success');
                this.showGeneratedFiles(response.data.manifest);
                this.loadPreview(response.data.manifest);
            } else {
                this.updateStatus(`Generation failed: ${response.data.error}`, 'error');
            }
        } catch (error) {
            console.error('Generation error:', error);
            this.updateStatus(`Generation error: ${error.message}`, 'error');
        } finally {
            this.generationInProgress = false;
            this.hideProgress();
        }
    }
    
    showProgress() {
        const container = document.getElementById('progress-container');
        container.style.display = 'block';
        
        // Simulate progress
        let progress = 0;
        const interval = setInterval(() => {
            progress += Math.random() * 15;
            if (progress >= 100) {
                progress = 100;
                clearInterval(interval);
            }
            
            document.getElementById('progress-fill').style.width = `${progress}%`;
            document.getElementById('progress-text').textContent = `${Math.round(progress)}%`;
        }, 500);
        
        this.progressInterval = interval;
    }
    
    hideProgress() {
        const container = document.getElementById('progress-container');
        container.style.display = 'none';
        
        if (this.progressInterval) {
            clearInterval(this.progressInterval);
        }
    }
    
    updateStatus(message, type = 'info') {
        const container = document.getElementById('status-container');
        
        const alert = document.createElement('div');
        alert.className = `alert alert-${type === 'error' ? 'error' : type === 'success' ? 'success' : 'info'}`;
        alert.innerHTML = `
            <span class="status-indicator status-${type}"></span>
            ${message}
        `;
        
        container.innerHTML = '';
        container.appendChild(alert);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alert.parentNode) {
                alert.remove();
            }
        }, 5000);
    }
    
    showGeneratedFiles(manifest) {
        const container = document.getElementById('files-container');
        const downloadAllContainer = document.getElementById('download-all-container');
        
        if (manifest.files && manifest.files.length > 0) {
            const fileList = document.createElement('ul');
            fileList.className = 'file-list';
            
            manifest.files.forEach(file => {
                const fileItem = document.createElement('li');
                fileItem.className = 'file-item';
                
                fileItem.innerHTML = `
                    <i class="fas fa-file-code file-icon"></i>
                    <div class="file-info">
                        <div class="file-name">${file.filename}</div>
                        <div class="file-meta">${file.edition} • ${(file.size / 1024).toFixed(1)} KB</div>
                    </div>
                    <button class="download-btn" onclick="platform.downloadFile('${file.edition}')">
                        <i class="fas fa-download"></i>
                    </button>
                `;
                
                fileList.appendChild(fileItem);
            });
            
            container.innerHTML = '';
            container.appendChild(fileList);
            
            downloadAllContainer.style.display = 'block';
        }
    }
    
    loadPreview(manifest) {
        if (!manifest.files) return;
        
        // Find Principals and Egyptian Clients files
        const principalsFile = manifest.files.find(f => f.edition === 'Principals');
        const egyptianFile = manifest.files.find(f => f.edition === 'Egyptian Clients');
        
        if (principalsFile) {
            this.loadPreviewContent('principals-preview', principalsFile.path);
            document.getElementById('download-principals').disabled = false;
        }
        
        if (egyptianFile) {
            this.loadPreviewContent('egyptian-preview', egyptianFile.path);
            document.getElementById('download-egyptian').disabled = false;
        }
    }
    
    loadPreviewContent(previewId, filePath) {
        const previewContent = document.getElementById(previewId).querySelector('.preview-content');
        
        // Create iframe for preview
        previewContent.innerHTML = `
            <iframe src="/runs/${this.selectedSector}/${this.getCurrentDateString()}/${this.getFileNameFromPath(filePath)}" 
                    class="preview-iframe"></iframe>
        `;
    }
    
    getCurrentDateString() {
        const now = new Date();
        return now.toISOString().split('T')[0];
    }
    
    getFileNameFromPath(filePath) {
        return filePath.split('/').pop();
    }
    
    async downloadFile(edition) {
        if (!this.currentRun) return;
        
        const file = this.currentRun.manifest.files.find(f => f.edition === edition);
        if (!file) return;
        
        try {
            const response = await axios.get(`/runs/${this.selectedSector}/${this.getCurrentDateString()}/${file.filename}`, {
                responseType: 'blob'
            });
            
            // Create download link
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', file.filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Download error:', error);
            this.updateStatus(`Download failed: ${error.message}`, 'error');
        }
    }
    
    async downloadAllFiles() {
        if (!this.currentRun) return;
        
        try {
            const response = await axios.get(`/api/download-run/${this.selectedSector}/${this.getCurrentDateString()}`, {
                responseType: 'blob'
            });
            
            // Create download link
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${this.selectedSector}_${this.getCurrentDateString()}_newsletters.zip`);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Download error:', error);
            this.updateStatus(`Download failed: ${error.message}`, 'error');
        }
    }
    
    initializeFileUpload() {
        const uploadArea = document.getElementById('upload-area');
        const fileInput = document.getElementById('file-input');
        const uploadBtn = document.getElementById('upload-btn');
        
        // Click to upload
        uploadArea.addEventListener('click', () => {
            fileInput.click();
        });
        
        // Drag and drop
        uploadArea.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadArea.classList.add('dragover');
        });
        
        uploadArea.addEventListener('dragleave', () => {
            uploadArea.classList.remove('dragover');
        });
        
        uploadArea.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadArea.classList.remove('dragover');
            
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                this.handleFileSelection();
            }
        });
        
        // File selection
        fileInput.addEventListener('change', () => {
            this.handleFileSelection();
        });
        
        // Upload button
        uploadBtn.addEventListener('click', () => {
            this.uploadPastIssue();
        });
        
        // Form validation
        ['upload-sector', 'upload-edition', 'upload-date'].forEach(id => {
            document.getElementById(id).addEventListener('change', () => {
                this.validateUploadForm();
            });
        });
    }
    
    handleFileSelection() {
        const fileInput = document.getElementById('file-input');
        const uploadArea = document.getElementById('upload-area');
        
        if (fileInput.files.length > 0) {
            const file = fileInput.files[0];
            uploadArea.innerHTML = `
                <i class="fas fa-file fa-2x text-primary mb-2"></i>
                <p class="mb-1">${file.name}</p>
                <small class="text-muted">${(file.size / 1024).toFixed(1)} KB</small>
            `;
            
            this.validateUploadForm();
        }
    }
    
    validateUploadForm() {
        const sector = document.getElementById('upload-sector').value;
        const edition = document.getElementById('upload-edition').value;
        const date = document.getElementById('upload-date').value;
        const file = document.getElementById('file-input').files[0];
        
        const uploadBtn = document.getElementById('upload-btn');
        uploadBtn.disabled = !(sector && edition && date && file);
    }
    
    async uploadPastIssue() {
        const formData = new FormData();
        formData.append('sector', document.getElementById('upload-sector').value);
        formData.append('edition', document.getElementById('upload-edition').value);
        formData.append('date', document.getElementById('upload-date').value);
        formData.append('file', document.getElementById('file-input').files[0]);
        
        try {
            const response = await axios.post('/api/upload-past-issue', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            
            if (response.data.success) {
                this.updateStatus('Past issue uploaded successfully!', 'success');
                this.loadPastIssues(document.getElementById('upload-sector').value);
                this.resetUploadForm();
            } else {
                this.updateStatus(`Upload failed: ${response.data.error}`, 'error');
            }
        } catch (error) {
            console.error('Upload error:', error);
            this.updateStatus(`Upload error: ${error.message}`, 'error');
        }
    }
    
    resetUploadForm() {
        document.getElementById('upload-sector').value = '';
        document.getElementById('upload-edition').value = '';
        document.getElementById('upload-date').value = '';
        document.getElementById('file-input').value = '';
        
        const uploadArea = document.getElementById('upload-area');
        uploadArea.innerHTML = `
            <i class="fas fa-cloud-upload-alt fa-2x text-muted mb-2"></i>
            <p class="mb-1">Drop file here or click to upload</p>
            <small class="text-muted">Supports: PDF, HTML, EML, TXT</small>
        `;
        
        document.getElementById('upload-btn').disabled = true;
    }
    
    async loadPastIssues(sector) {
        if (!sector) return;
        
        try {
            const response = await axios.get(`/api/past-issues/${sector}`);
            this.displayPastIssues(response.data.past_issues);
        } catch (error) {
            console.error('Error loading past issues:', error);
        }
    }
    
    displayPastIssues(pastIssues) {
        const container = document.getElementById('past-issues-container');
        
        if (!pastIssues || pastIssues.trim() === '') {
            container.innerHTML = '<p class="text-muted text-center">No past issues found</p>';
            return;
        }
        
        // Parse past issues and display them
        const issues = pastIssues.split('--- PAST_ISSUES_START ---')[1];
        if (!issues) {
            container.innerHTML = '<p class="text-muted text-center">No past issues found</p>';
            return;
        }
        
        const issueBlocks = issues.split('---').filter(block => block.trim());
        const issueList = document.createElement('div');
        
        issueBlocks.forEach(block => {
            const lines = block.trim().split('\n');
            const header = lines[0];
            const content = lines.slice(1).join('\n').substring(0, 100) + '...';
            
            const issueItem = document.createElement('div');
            issueItem.className = 'past-issue-item';
            issueItem.innerHTML = `
                <div class="past-issue-date">${header}</div>
                <div class="past-issue-edition">${content}</div>
            `;
            
            issueList.appendChild(issueItem);
        });
        
        container.innerHTML = '';
        container.appendChild(issueList);
    }
    
    async fetchSectors() {
        try {
            const response = await axios.get('/api/sectors');
            return response.data;
        } catch (error) {
            console.error('Error fetching sectors:', error);
            return {};
        }
    }
}

// Initialize platform when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.platform = new AEDCOPlatform();
});