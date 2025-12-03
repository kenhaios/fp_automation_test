/**
 * SMS Helper Utilities for Maestro Tests
 * Automatically fetches and sets the latest verification code when executed
 */

/**
 * Clean and normalize SMS body to handle encoding artifacts and special characters
 * @param {string} body - The raw SMS body content
 * @returns {string} Cleaned SMS body
 */
function cleanSMSBody(body) {
    if (!body) return '';
    
    console.log('Cleaning SMS body - Original length:', body.length);
    
    // Step 1: Remove carriage returns and newlines
    let cleaned = body.replace(/\r\n/g, ' ').replace(/\r/g, ' ').replace(/\n/g, ' ');
    console.log('After removing line breaks:', cleaned);
    
    // Step 2: Handle quoted-printable encoding (remove = at end of lines)
    cleaned = cleaned.replace(/=\s/g, '');
    console.log('After removing quoted-printable artifacts:', cleaned);
    
    // Step 3: Remove extra whitespace
    cleaned = cleaned.replace(/\s+/g, ' ').trim();
    console.log('After normalizing whitespace:', cleaned);
    
    return cleaned;
}

/**
 * Extract verification code from cleaned SMS body using multiple strategies
 * @param {string} cleanedBody - The cleaned SMS body content
 * @returns {string|null} The extracted verification code or null if not found
 */
function extractVerificationCode(cleanedBody) {
    if (!cleanedBody) return null;
    
    console.log('Extracting verification code from:', cleanedBody);
    
    // Strategy 1: Look for 6 consecutive digits
    let match = cleanedBody.match(/\b\d{6}\b/);
    if (match) {
        console.log('Strategy 1 (6 consecutive digits) found:', match[0]);
        return match[0];
    }
    
    // Strategy 2: Look for 5-7 digits (in case of formatting issues)
    match = cleanedBody.match(/\b\d{5,7}\b/);
    if (match) {
        const code = match[0];
        console.log('Strategy 2 (5-7 digits) found:', code);
        // If it's 6 digits, return it; if longer, take first 6; if shorter, might be valid too
        if (code.length === 6) {
            return code;
        } else if (code.length > 6) {
            console.log('Code too long, taking first 6 digits:', code.substring(0, 6));
            return code.substring(0, 6);
        } else {
            console.log('Code shorter than 6 digits, using as-is:', code);
            return code;
        }
    }
    
    // Strategy 3: Look for digits around "verification code" or "code" keywords
    match = cleanedBody.match(/(?:verification\s+code|code)\s*:?\s*(\d{4,8})/i);
    if (match) {
        console.log('Strategy 3 (context-based) found:', match[1]);
        return match[1];
    }
    
    // Strategy 4: Look for any sequence of 4-8 digits (last resort)
    match = cleanedBody.match(/\d{4,8}/);
    if (match) {
        console.log('Strategy 4 (any digits) found:', match[0]);
        return match[0];
    }
    
    console.log('No verification code found with any strategy');
    return null;
}

/**
 * Fetches the latest verification code from SMS messages for a specific phone number with retry logic
 * @param {string} phoneNumber - The phone number to filter SMS messages by
 * @param {number} maxAttempts - Maximum number of retry attempts (default: 10)
 * @param {number} retryDelay - Delay between retry attempts in milliseconds (default: 3000)
 * @returns {string} The 6-digit verification code
 * @throws {Error} If no verification code is found after all retry attempts or API request fails
 */
function getLatestVerificationCode(phoneNumber, maxAttempts = 10, retryDelay = 3000) {
    console.log('Starting SMS verification code retrieval for phone number:', phoneNumber);
    console.log('Max attempts:', maxAttempts, 'Retry delay:', retryDelay + 'ms');
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        console.log('Attempt', attempt + '/' + maxAttempts, '- Fetching SMS messages...');
        
        try {
            const response = http.get('http://mail.bamboo.stuffio.com/api/v2/messages?limit=50', {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'mail.bamboo.stuffio.com'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch SMS messages: ' + response.status);
            }
            
            const data = json(response.body);
            const messages = data.items || [];
            console.log('Found', messages.length, 'total messages');
            
            // Find the most recent SMS message for the specific phone number
            let verificationCode = null;
            for (let i = 0; i < data.items.length; i++) {
                const message = data.items[i];
                
                // Check if this is an SMS message for the specific phone number
                if (message.Content && message.Content.Headers && message.Content.Headers.Subject) {
                    const subject = message.Content.Headers.Subject[0];
                    console.log('Checking message subject:', subject);
                    
                    // Match subject pattern: "SMS to [phone_number]"
                    if (subject.includes('SMS') && phoneNumber && subject.includes(phoneNumber)) {
                        console.log('Found SMS for phone number:', phoneNumber);
                        const body = message.Content.Body;
                        console.log('== Found body:', body);
                        console.log('==');

                        // Clean and normalize the SMS body to handle encoding issues
                        const cleanedBody = cleanSMSBody(body);
                        console.log('== Cleaned body:', cleanedBody);
                        console.log('==');

                        // Extract 6-digit verification code from cleaned SMS body
                        const codeMatch = extractVerificationCode(cleanedBody);
                        console.log('==Code match: ', codeMatch);
                        if (codeMatch) {
                            verificationCode = codeMatch;
                            console.log('Successfully extracted verification code:', verificationCode);
                            return verificationCode; // Return immediately when found
                        }
                    }
                }
            }
            
            // If we reach here, no SMS was found for this phone number
            console.log('No SMS found for phone number', phoneNumber, 'in attempt', attempt);
            
            // If this is not the last attempt, wait and retry
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before next attempt...');
                // Simple delay implementation for Maestro
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
            
        } catch (error) {
            console.log('Error in attempt', attempt + ':', error.message);
            if (attempt === maxAttempts) {
                throw error;
            }
            
            // Wait before retrying on error (unless it's the last attempt)
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before retrying after error...');
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
        }
    }
    
    // If we've exhausted all attempts without finding the SMS
    throw new Error('No verification code found in SMS messages for phone number: ' + phoneNumber + ' after ' + maxAttempts + ' attempts');
}

/**
 * Fetches SMS messages with optional filtering
 * @param {Object} options - Filter options
 * @param {number} options.limit - Maximum number of messages to fetch (default: 50)
 * @param {string} options.subjectFilter - Filter messages by subject content
 * @returns {Array} Array of SMS message objects
 */
function getSMSMessages(options = {}) {
    const limit = options.limit || 50;
    const url = `http://mail.bamboo.stuffio.com/api/v2/messages?limit=${limit}`;
    
    const response = http.get(url, {
        headers: {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Accept-Encoding': 'gzip, deflate',
            'Host': 'mail.bamboo.stuffio.com'
        }
    });
    
    if (!response.ok) {
        throw new Error('Failed to fetch SMS messages: ' + response.status);
    }
    
    const data = json(response.body);
    let messages = data.items || [];
    console.log('Messages: ' + messages);
    
    // Filter by subject if specified
    if (options.subjectFilter) {
        messages = messages.filter(message => {
            if (message.Content && message.Content.Headers && message.Content.Headers.Subject) {
                const subject = message.Content.Headers.Subject[0];
                return subject.includes(options.subjectFilter);
            }
            return false;
        });
    }
    
    return messages;
}

// Auto-execute when this script is run by Maestro
// This sets output.otp automatically when the script is executed
// The PHONE_NUMBER environment variable is passed from the calling flow

// Configuration: Retry parameters (can be overridden via environment variables)
const MAX_ATTEMPTS = 10;
const RETRY_DELAY = 3000;

console.log('=== SMS Helper Configuration ===');
console.log('Max attempts:', MAX_ATTEMPTS);
console.log('Retry delay:', RETRY_DELAY + 'ms');
console.log('================================');

// Debug: Log what environment variables are available
console.log('\nAvailable environment variables:', typeof PHONE_NUMBER !== 'undefined' ? 'PHONE_NUMBER exists' : 'PHONE_NUMBER missing');
console.log('\nPHONE_NUMBER value:', typeof PHONE_NUMBER !== 'undefined' ? PHONE_NUMBER : 'undefined');

let phoneNumber = typeof PHONE_NUMBER !== 'undefined' ? PHONE_NUMBER : null;

// Fallback: If PHONE_NUMBER is not available, try without phone number filtering
if (!phoneNumber) {
    console.log('Warning: PHONE_NUMBER not provided, falling back to latest SMS without phone filtering');
    output.otp = getLatestVerificationCodeFallback(MAX_ATTEMPTS, RETRY_DELAY);
} else {
    console.log('\nUsing phone number filtering for:', phoneNumber);
    output.otp = getLatestVerificationCode(phoneNumber, MAX_ATTEMPTS, RETRY_DELAY);
}

/**
 * Fallback function to get latest verification code without phone number filtering with retry logic
 * @param {number} maxAttempts - Maximum number of retry attempts (default: 10)
 * @param {number} retryDelay - Delay between retry attempts in milliseconds (default: 3000)
 * @returns {string} The 6-digit verification code
 */
function getLatestVerificationCodeFallback(maxAttempts = 10, retryDelay = 3000) {
    console.log('Starting SMS verification code retrieval (fallback mode - no phone filtering)');
    console.log('Max attempts:', maxAttempts, 'Retry delay:', retryDelay + 'ms');
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        console.log('Fallback attempt', attempt + '/' + maxAttempts, '- Fetching SMS messages...');
        
        try {
            const response = http.get('http://mail.bamboo.stuffio.com/api/v2/messages?limit=50', {
                headers: {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
                    'Accept': 'application/json, text/plain, */*',
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Connection': 'keep-alive',
                    'Accept-Encoding': 'gzip, deflate',
                    'Host': 'mail.bamboo.stuffio.com'
                }
            });
            
            if (!response.ok) {
                throw new Error('Failed to fetch SMS messages: ' + response.status);
            }
            
            const data = json(response.body);
            const messages = data.items || [];
            console.log('Found', messages.length, 'total messages (fallback mode)');
            
            // Find the most recent SMS message (without phone number filtering)
            let verificationCode = null;
            for (let i = 0; i < data.items.length; i++) {
                const message = data.items[i];
                
                // Check if this is an SMS message (subject contains "SMS")
                if (message.Content && message.Content.Headers && message.Content.Headers.Subject) {
                    const subject = message.Content.Headers.Subject[0];
                    console.log('Checking message subject (fallback):', subject);
                    
                    if (subject.includes('SMS')) {
                        console.log('Found SMS message (fallback mode)');
                        const body = message.Content.Body;
                        console.log('== Fallback body:', body);
                        
                        // Clean and normalize the SMS body to handle encoding issues
                        const cleanedBody = cleanSMSBody(body);
                        console.log('== Fallback cleaned body:', cleanedBody);
                        
                        // Extract 6-digit verification code from cleaned SMS body
                        const codeMatch = extractVerificationCode(cleanedBody);
                        console.log('== Fallback code match:', codeMatch);
                        if (codeMatch) {
                            verificationCode = codeMatch;
                            console.log('Successfully extracted verification code (fallback):', verificationCode);
                            return verificationCode; // Return immediately when found
                        }
                    }
                }
            }
            
            // If we reach here, no SMS was found
            console.log('No SMS found in fallback attempt', attempt);
            
            // If this is not the last attempt, wait and retry
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before next fallback attempt...');
                // Simple delay implementation for Maestro
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
            
        } catch (error) {
            console.log('Error in fallback attempt', attempt + ':', error.message);
            if (attempt === maxAttempts) {
                throw error;
            }
            
            // Wait before retrying on error (unless it's the last attempt)
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before retrying fallback after error...');
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
        }
    }
    
    // If we've exhausted all attempts without finding any SMS
    throw new Error('No verification code found in any recent SMS messages after ' + maxAttempts + ' attempts (fallback mode)');
}