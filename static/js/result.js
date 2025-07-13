function checkAnother() { 
    // redirect to home page
    window.location.href = '/'; 
}

function downloadJSON() {
    // download json data as file
    const jsonEl = document.getElementById('json-data');
    if (!jsonEl || !jsonEl.textContent) {
        showPopup('Error', 'No JSON data available to download.');
        return;
    }
    
    try {
        const jsonData = jsonEl.textContent;
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'tabayyun_result.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        showPopup('Success', 'JSON data downloaded successfully!');
    } catch (error) {
        console.error('Download error:', error);
        showPopup('Error', 'Failed to download JSON data.');
    }
} 