function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
  
async function main() {
    console.log("Trello Toolbox Tonic called");
    const activeCard = document.querySelector('.active-card');
    const closeCardSelector = '.icon-md.icon-close.dialog-close-button.js-close-window';
    let shareButton = document.querySelector('.button-link.js-more-menu');
  
    // Check if there is an activeCard element
    if (activeCard) {
    console.log("Clicking activeCard"); // Print a message to the console
    activeCard.click(); // Click on the activeCard element
    await sleep(250); // Pause the execution for 250 milliseconds, wait for the card to open

    let elapsedTime = 0; // Initialize a timer variable
    let maxWaitTime = 5000; // Set the maximum waiting time to 5000 milliseconds (5 seconds)

    // Wait for the shareButton element to become visible or until the maximum wait time has passed
    while (!shareButton && elapsedTime < maxWaitTime) {
        await sleep(250); // Pause the execution for 250 milliseconds
        elapsedTime += 250; // Increment the elapsed time by 250 milliseconds
        if (shareButton) { // If shareButton becomes visible during the loop
        break; // Exit the loop early
        }
    }
    }

        
    shareButton = document.querySelector('.button-link.js-more-menu');
    if (shareButton) {
        console.log("Clicking shareButton");
        shareButton.click();
        elapsedTime = 0;

        let emailInput = document.querySelector('.pop-over input.js-email');
        // Wait for the email input to become visible or reach the maximum wait time
        while (!emailInput && elapsedTime < maxWaitTime) {
            await sleep(250);
            elapsedTime += 250;
            emailInput = document.querySelector('.pop-over input.js-email');
            if (emailInput) {
                break;
              }
        }

        if (emailInput) {
            const emailValue = emailInput.value;
            console.log(emailValue);
            navigator.clipboard.writeText(emailValue);
        
            console.log("Closing pop-over");
            const closeButton = document.querySelector('.pop-over-header-close-btn.icon-sm.icon-close');
            if (closeButton) {
                closeButton.click();
            }
        
            if (activeCard) {
                console.log("Closing activeCard");
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