// Cipher Tools - Main JavaScript

document.addEventListener('DOMContentLoaded', () => {
    // Utility function for copying text to clipboard
    const copyToClipboard = (text) => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.setAttribute('readonly', '');
        textarea.style.position = 'absolute';
        textarea.style.left = '-9999px';
        document.body.appendChild(textarea);
        
        const selected = document.getSelection().rangeCount > 0 
            ? document.getSelection().getRangeAt(0) 
            : false;
            
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        
        if (selected) {
            document.getSelection().removeAllRanges();
            document.getSelection().addRange(selected);
        }
        
        return true;
    };
    
    // Initialize copy buttons that aren't handled by jQuery
    const copyButtons = document.querySelectorAll('.copy-btn:not([data-target])');
    if (copyButtons.length > 0) {
        copyButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                const text = button.getAttribute('data-copy-text') || '';
                if (text && copyToClipboard(text)) {
                    const originalText = button.innerHTML;
                    button.innerHTML = 'Copied!';
                    setTimeout(() => {
                        button.innerHTML = originalText;
                    }, 1500);
                }
            });
        });
    }
    
    // Special handling for Caesar cipher
    const caesarShiftInputs = document.querySelectorAll('.shift-value');
    if (caesarShiftInputs.length > 0) {
        caesarShiftInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const value = parseInt(e.target.value, 10);
                if (isNaN(value) || value < 1) {
                    e.target.value = 1;
                } else if (value > 25) {
                    e.target.value = 25;
                }
            });
        });
    }
    
    // Special handling for Affine cipher parameter a
    const affineAInputs = document.querySelectorAll('.a-value');
    if (affineAInputs.length > 0) {
        affineAInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                let value = parseInt(e.target.value, 10);
                if (isNaN(value) || value < 1) {
                    e.target.value = 1;
                } else if (value > 25) {
                    e.target.value = 25;
                }
                
                // Check if a is coprime with 26 (not divisible by 2 or 13)
                if (value % 2 === 0 || value % 13 === 0) {
                    // Create or update warning message
                    let warningId = 'affine-a-warning';
                    let warning = document.getElementById(warningId);
                    
                    if (!warning) {
                        warning = document.createElement('div');
                        warning.id = warningId;
                        warning.className = 'alert alert-warning mt-2';
                        warning.innerHTML = 'Warning: Parameter "a" must be coprime with 26 for proper decryption.';
                        input.parentNode.parentNode.appendChild(warning);
                    }
                } else {
                    // Remove warning if exists
                    const warning = document.getElementById('affine-a-warning');
                    if (warning) {
                        warning.remove();
                    }
                }
            });
        });
    }
    
    // Special handling for Affine cipher parameter b
    const affineBInputs = document.querySelectorAll('.b-value');
    if (affineBInputs.length > 0) {
        affineBInputs.forEach(input => {
            input.addEventListener('input', (e) => {
                const value = parseInt(e.target.value, 10);
                if (isNaN(value) || value < 0) {
                    e.target.value = 0;
                } else if (value > 25) {
                    e.target.value = 25;
                }
            });
        });
    }
    
    // Auto-grow textareas
    const autoGrowTextareas = document.querySelectorAll('.auto-grow');
    if (autoGrowTextareas.length > 0) {
        const adjustHeight = (el) => {
            el.style.height = 'auto';
            el.style.height = (el.scrollHeight) + 'px';
        };
        
        autoGrowTextareas.forEach(textarea => {
            adjustHeight(textarea);
            textarea.addEventListener('input', (e) => {
                adjustHeight(e.target);
            });
        });
    }
}); 