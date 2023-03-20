chrome.commands.onCommand.addListener(async (command) => {
    if (command === 'get_trello_email') {
      try {
        const tabs = await new Promise((resolve) =>
          chrome.tabs.query({ active: true, currentWindow: true }, resolve)
        );
  
        const activeTab = tabs[0];
        if (activeTab.url.startsWith('https://trello.com')) {
          chrome.scripting.executeScript({
            target: { tabId: activeTab.id },
            files: ['content-script.js'],
          });
        } else {
          console.error(
            'The Trello Toolbox Tonic extension only works on https://trello.com'
          );
        }
      } catch (error) {
        console.error('Error executing Trello Toolbox Tonic:', error);
      }
    }
  });
  