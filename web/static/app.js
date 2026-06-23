/**
 * GCP 2026 Training — Frontend interactivity.
 * Handles: quiz option clicks, double-submit prevention.
 */

// ---- Event Listeners ----

document.addEventListener('DOMContentLoaded', () => {
    // Quiz form: prevent double submission using a hidden field,
    // NOT by disabling buttons (disabled button values are not sent!)
    document.querySelectorAll('.quiz-form, .exam-form').forEach(form => {
        let submitted = false;
        form.addEventListener('submit', (e) => {
            if (submitted) {
                e.preventDefault();
                return;
            }
            submitted = true;
            // Fade buttons to show submission without disabling them
            const buttons = form.querySelectorAll('button[type="submit"]');
            buttons.forEach(btn => { btn.style.opacity = '0.6'; });
        });
    });
});
