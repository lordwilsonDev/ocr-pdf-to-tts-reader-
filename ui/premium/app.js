document.addEventListener('DOMContentLoaded', () => {
    const progressText = document.querySelector('.progress-orb span');
    let progress = 84;

    // Simulate progress jitter
    setInterval(() => {
        if(progress < 100) {
            progress += Math.random() * 0.1;
            progressText.innerText = `${Math.floor(progress)}%`;
        }
    }, 2000);

    // Micro-animation for digital overlays
    const overlays = document.querySelectorAll('.holographic-data');
    document.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 10;
        const y = (e.clientY / window.innerHeight - 0.5) * 10;
        
        overlays.forEach(o => {
            o.style.transform = `translate(${x}px, ${y}px)`;
        });
    });

    console.log("📜 Manuscript Master HUD Online. OCR telemetry synced.");
});
