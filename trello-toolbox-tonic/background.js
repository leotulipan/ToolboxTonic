// 1. Click the share button
const shareButton = document.querySelector('.button-link.js-more-menu');
if (shareButton) {
  shareButton.click();
} else {
  console.error('Share button not found');
}

setTimeout(() => {
  // 2. Check if the pop-over is shown
  const popOver = document.querySelector('.pop-over.is-shown');
  if (popOver) {
    // 3. Get the value from input with class "js-email"
    const emailInput = popOver.querySelector('.js-email');
    if (emailInput) {
      const emailValue = emailInput.value;
      
      // 4. Console log the value and copy it to the clipboard
      console.log('Email value:', emailValue);
      navigator.clipboard.writeText(emailValue).then(() => {
        console.log('Email value copied to clipboard');
      }).catch(err => {
        console.error('Failed to copy email value to clipboard:', err);
      });
      
      // 5. Close the pop-over
      const closeButton = popOver.querySelector('.pop-over-header-close-btn');
      if (closeButton) {
        closeButton.click();
      } else {
        console.error('Close button not found');
      }
    } else {
      console.error('Email input not found');
    }
  } else {
    console.error('Pop-over not found or not shown');
  }
}, 1000);
