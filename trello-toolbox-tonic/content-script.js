function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
  
async function main() {
    console.log("Trello Toolbox Tonic called");
    const activeCard = document.querySelector('.active-card');
    const closeCardSelector = '.icon-md.icon-close.dialog-close-button.js-close-window';
  
    if (activeCard) {
      console.log("There is an active card");
      activeCard.click();
      await sleep(1000); // wait for the card to open
  
      // Check if the share button is visible; if not, wait for another 1000ms
      let shareButton = document.querySelector('.button-link.js-more-menu');
      if (!shareButton) {
        await sleep(1000);
        shareButton = document.querySelector('.button-link.js-more-menu');
      }
    }
  
    if (shareButton) {
        console.log("Clicking sharebutton");
        shareButton.click();
        elapsedTime = 0;

        let emailInput = document.querySelector('.pop-over input.js-email');
        // Wait for the email input to become visible or reach the maximum wait time
        while (!emailInput && elapsedTime < maxWaitTime) {
            await sleep(250);
            elapsedTime += 250;
            emailInput = document.querySelector('.pop-over input.js-email');
        }

        if (emailInput) {
            const emailValue = emailInput.value;
            console.log(emailValue);
            navigator.clipboard.writeText(emailValue);
        
            const closeButton = document.querySelector('.pop-over-header-close-btn.icon-sm.icon-close');
            if (closeButton) {
                closeButton.click();
            }
        
            if (activeCard) {
                const closeOpenedCardButton = document.querySelector(closeCardSelector);
                if (closeOpenedCardButton) {
                closeOpenedCardButton.click();
                }
            }
            } else {
            console.error('Trello Toolbox Tonic: Email input not found.');
            }
    } else {
        console.error('Trello Toolbox Tonic: Share button not found.');
    }
}    
  
  main();