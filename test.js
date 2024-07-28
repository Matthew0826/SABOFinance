const puppeteer = require('puppeteer');
(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await page.goto('https://docs.google.com/spreadsheets/d/1qbCcjiO8y9Fz0yAJm2HxnzlmC02w3zv5xGx1-TpaFHs/edit?usp=sharing');
    // Click the button 
    // Wait for the checkbox to be visible 
    // await page.waitForSelector('#choice_2_155_1');
    // // Click the checkbox 
    // await page.click('#choice_2_155_1');
    // await page.click('#choice_2_155_2');
    // await page.click('#choice_2_155_3');
    // await page.click('#choice_2_155_4');
    // await page.click('#choice_2_155_5');
    // await page.click('#choice_2_155_6');
    // await page.click('#choice_2_155_7');

    // await page.type('#input_2_2_3', 'test');
    // Wait for the sheet to load
    //await page.waitForSelector('div.docs-sheet');

    // Extract text from a specific cell (e.g., A1)
    // This selector might need to be adjusted based on actual Google Sheets structure
    const cellText = await page.evaluate(() => {
        // Find the cell by its known class or data attribute
        // Google Sheets has dynamic classes, so this may need adjustment
        const cell = document.querySelector('[aria-label="A1"]'); // Example selector
        return cell ? cell.textContent.trim() : 'Cell not found';
    });

    console.log('Cell text:', cellText);
    await browser.close();
})();