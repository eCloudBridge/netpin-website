/*
 * Google Apps Script for Netpin Contact Form
 * 
 * INSTRUCTIONS TO DEPLOY:
 * 1. Open Google Sheets (sheets.new) and create a new spreadsheet.
 * 2. In row 1, add these headers to columns A through G:
 *    Timestamp | First Name | Last Name | Email | Company | Topic | Message
 * 3. Go to Extensions > Apps Script in the menu.
 * 4. Replace any existing code with this entire script.
 * 5. Save the file (Ctrl+S / Cmd+S).
 * 6. Click "Deploy" > "New deployment" in the top right.
 * 7. Click the gear icon "Select type" and choose "Web app".
 * 8. Under "Execute as", select "Me".
 * 9. Under "Who has access", MUST be set to "Anyone".
 * 10. Click "Deploy". When asked to authorize, follow the prompts. (You may need to bypass the "Google hasn't verified this app" warning by clicking "Advanced").
 * 11. Copy the Web App URL generated.
 * 12. Finally, open `contact.html` in your website code and carefully replace 'YOUR_GOOGLE_SCRIPT_URL_HERE' with your copied URL!
 */

const SHEET_NAME = "Sheet1";

function doPost(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    
    if (!sheet) {
        throw new Error("Target sheet could not be found.");
    }
    
    // Extract parameters from the incoming POST body
    const timestamp = new Date();
    const firstName = e.parameter.firstName || "";
    const lastName = e.parameter.lastName || "";
    const email = e.parameter.email || "";
    const company = e.parameter.company || "";
    const topic = e.parameter.topic || "";
    const message = e.parameter.message || "";
    
    // Append the row cleanly into the designated sheet
    sheet.appendRow([
      timestamp, 
      firstName, 
      lastName, 
      email, 
      company, 
      topic, 
      message
    ]);
    
    // Return standard success response required by the contact.html fetch() block
    return ContentService
      .createTextOutput(JSON.stringify({ "result": "success" }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Return error response gracefully
    return ContentService
      .createTextOutput(JSON.stringify({ "result": "error", "error": error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
