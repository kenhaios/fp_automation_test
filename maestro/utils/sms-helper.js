/**
 * OTP Helper Utilities for Maestro Tests
 * Automatically fetches and sets the latest verification code from SMS or Email when executed
 * 
 * Supports both SMS and Email OTP extraction:
 * - SMS: Filters by phone number in subject line
 * - Email: Filters by email address in To field and FasterPay sender
 * 
 * Usage:
 * SMS Mode (default):
 *   env: { PHONE_NUMBER: "+1234567890" }
 * 
 * Email Mode:
 *   env: { MESSAGE_TYPE: "email", EMAIL_ADDRESS: "user@fp.com" }
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
 * Clean and normalize email body to handle HTML content and quoted-printable encoding
 * @param {string} body - The raw email body content (HTML)
 * @returns {string} Cleaned email body as plain text
 */
function cleanEmailBody(body) {
    if (!body) return '';
    
    console.log('Cleaning email body - Original length:', body.length);
    
    // Step 1: Handle quoted-printable encoding
    let cleaned = body
        // Remove =\r\n (soft line breaks)
        .replace(/=\r\n/g, '')
        // Decode =3D to = 
        .replace(/=3D/g, '=')
        // Decode other quoted-printable sequences
        .replace(/=([0-9A-F]{2})/g, (match, hex) => String.fromCharCode(parseInt(hex, 16)));
    
    console.log('After quoted-printable decoding:', cleaned.substring(0, 200) + '...');
    
    // Step 2: Remove HTML tags and extract text content
    cleaned = cleaned
        // Remove DOCTYPE and HTML comments
        .replace(/<!doctype[^>]*>/gi, '')
        .replace(/<!--[\s\S]*?-->/g, '')
        // Remove script and style content
        .replace(/<(script|style)[^>]*>[\s\S]*?<\/\1>/gi, '')
        // Remove all HTML tags
        .replace(/<[^>]*>/g, ' ')
        // Decode HTML entities
        .replace(/&nbsp;/g, ' ')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&amp;/g, '&')
        .replace(/&quot;/g, '"')
        .replace(/&#39;/g, "'");
    
    console.log('After HTML removal:', cleaned.substring(0, 200) + '...');
    
    // Step 3: Clean up whitespace and line breaks
    cleaned = cleaned
        .replace(/\r\n/g, ' ')
        .replace(/\r/g, ' ')
        .replace(/\n/g, ' ')
        .replace(/\s+/g, ' ')
        .trim();
    
    console.log('After whitespace cleanup:', cleaned);
    
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

/**
 * Fetches the latest verification code from email messages for a specific email address with retry logic
 * @param {string} emailAddress - The email address to filter email messages by
 * @param {number} maxAttempts - Maximum number of retry attempts (default: 10)
 * @param {number} retryDelay - Delay between retry attempts in milliseconds (default: 3000)
 * @returns {string} The 6-digit verification code
 * @throws {Error} If no verification code is found after all retry attempts or API request fails
 */
function getLatestEmailVerificationCode(emailAddress, maxAttempts = 10, retryDelay = 3000) {
    console.log('Starting email verification code retrieval for email address:', emailAddress);
    console.log('Max attempts:', maxAttempts, 'Retry delay:', retryDelay + 'ms');
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        console.log('Email attempt', attempt + '/' + maxAttempts, '- Fetching email messages...');
        
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
                throw new Error('Failed to fetch email messages: ' + response.status);
            }
            
            const data = json(response.body);
            const messages = data.items || [];
            console.log('Found', messages.length, 'total messages');
            
            // Find the most recent email message for the specific email address
            let verificationCode = null;
            for (let i = 0; i < data.items.length; i++) {
                const message = data.items[i];
                
                // Check if this is an email message for the specific email address
                if (message.Content && message.Content.Headers) {
                    // Check From field for support@fasterpay.com
                    const fromHeaders = message.Content.Headers.From;
                    const subjectHeaders = message.Content.Headers.Subject;
                    const toArray = message.To;
                    
                    if (fromHeaders && subjectHeaders && toArray) {
                        const fromEmail = fromHeaders[0];
                        const subject = subjectHeaders[0];
                        console.log('Checking email - From:', fromEmail, 'Subject:', subject);
                        
                        // Check if this is from FasterPay support and has verification in subject
                        if (fromEmail.includes('support@fasterpay.com') && 
                            subject.toLowerCase().includes('verification')) {
                            
                            // Check if this email is for the target email address
                            const isForTargetEmail = toArray.some(toObj => 
                                toObj.Mailbox && toObj.Domain && 
                                (toObj.Mailbox + '@' + toObj.Domain) === emailAddress
                            );
                            
                            if (isForTargetEmail) {
                                console.log('Found email for address:', emailAddress);
                                const body = message.Content.Body;
                                console.log('== Email body found, length:', body ? body.length : 0);

                                // Clean and normalize the email body to handle HTML and encoding issues
                                const cleanedBody = cleanEmailBody(body);
                                console.log('== Cleaned email body:', cleanedBody.substring(0, 200) + '...');

                                // Extract 6-digit verification code from cleaned email body
                                const codeMatch = extractVerificationCode(cleanedBody);
                                console.log('== Email code match:', codeMatch);
                                if (codeMatch) {
                                    verificationCode = codeMatch;
                                    console.log('Successfully extracted verification code from email:', verificationCode);
                                    return verificationCode; // Return immediately when found
                                }
                            }
                        }
                    }
                }
            }
            
            // If we reach here, no email was found for this email address
            console.log('No email found for email address', emailAddress, 'in attempt', attempt);
            
            // If this is not the last attempt, wait and retry
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before next email attempt...');
                // Simple delay implementation for Maestro
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
            
        } catch (error) {
            console.log('Error in email attempt', attempt + ':', error.message);
            if (attempt === maxAttempts) {
                throw error;
            }
            
            // Wait before retrying on error (unless it's the last attempt)
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before retrying email after error...');
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
        }
    }
    
    // If we've exhausted all attempts without finding the email
    throw new Error('No verification code found in email messages for email address: ' + emailAddress + ' after ' + maxAttempts + ' attempts');
}

/**
 * Fallback function to get latest verification code from emails without email filtering with retry logic
 * @param {number} maxAttempts - Maximum number of retry attempts (default: 10)
 * @param {number} retryDelay - Delay between retry attempts in milliseconds (default: 3000)
 * @returns {string} The 6-digit verification code
 */
function getLatestEmailVerificationCodeFallback(maxAttempts = 10, retryDelay = 3000) {
    console.log('Starting email verification code retrieval (fallback mode - no email filtering)');
    console.log('Max attempts:', maxAttempts, 'Retry delay:', retryDelay + 'ms');
    
    for (let attempt = 1; attempt <= maxAttempts; attempt++) {
        console.log('Email fallback attempt', attempt + '/' + maxAttempts, '- Fetching email messages...');
        
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
                throw new Error('Failed to fetch email messages: ' + response.status);
            }
            
            const data = json(response.body);
            const messages = data.items || [];
            console.log('Found', messages.length, 'total messages (email fallback mode)');
            
            // Find the most recent email message (without email address filtering)
            let verificationCode = null;
            for (let i = 0; i < data.items.length; i++) {
                const message = data.items[i];
                
                // Check if this is an email message from FasterPay support
                if (message.Content && message.Content.Headers) {
                    const fromHeaders = message.Content.Headers.From;
                    const subjectHeaders = message.Content.Headers.Subject;
                    
                    if (fromHeaders && subjectHeaders) {
                        const fromEmail = fromHeaders[0];
                        const subject = subjectHeaders[0];
                        console.log('Checking email (fallback) - From:', fromEmail, 'Subject:', subject);
                        
                        // Check if this is from FasterPay support and has verification in subject
                        if (fromEmail.includes('support@fasterpay.com') && 
                            subject.toLowerCase().includes('verification')) {
                            console.log('Found FasterPay verification email (fallback mode)');
                            const body = message.Content.Body;
                            console.log('== Email fallback body found, length:', body ? body.length : 0);
                            
                            // Clean and normalize the email body to handle HTML and encoding issues
                            const cleanedBody = cleanEmailBody(body);
                            console.log('== Email fallback cleaned body:', cleanedBody.substring(0, 200) + '...');
                            
                            // Extract 6-digit verification code from cleaned email body
                            const codeMatch = extractVerificationCode(cleanedBody);
                            console.log('== Email fallback code match:', codeMatch);
                            if (codeMatch) {
                                verificationCode = codeMatch;
                                console.log('Successfully extracted verification code (email fallback):', verificationCode);
                                return verificationCode; // Return immediately when found
                            }
                        }
                    }
                }
            }
            
            // If we reach here, no email was found
            console.log('No FasterPay verification email found in fallback attempt', attempt);
            
            // If this is not the last attempt, wait and retry
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before next email fallback attempt...');
                // Simple delay implementation for Maestro
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
            
        } catch (error) {
            console.log('Error in email fallback attempt', attempt + ':', error.message);
            if (attempt === maxAttempts) {
                throw error;
            }
            
            // Wait before retrying on error (unless it's the last attempt)
            if (attempt < maxAttempts) {
                console.log('Waiting', retryDelay + 'ms', 'before retrying email fallback after error...');
                const startTime = Date.now();
                while (Date.now() - startTime < retryDelay) {
                    // Wait loop
                }
            }
        }
    }
    
    // If we've exhausted all attempts without finding any email
    throw new Error('No verification code found in any recent FasterPay verification emails after ' + maxAttempts + ' attempts (email fallback mode)');
}

/**
 * Fetches email messages with optional filtering
 * @param {Object} options - Filter options
 * @param {number} options.limit - Maximum number of messages to fetch (default: 50)
 * @param {string} options.fromFilter - Filter messages by From header content
 * @param {string} options.subjectFilter - Filter messages by subject content
 * @returns {Array} Array of email message objects
 */
function getEmailMessages(options = {}) {
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
        throw new Error('Failed to fetch email messages: ' + response.status);
    }
    
    const data = json(response.body);
    let messages = data.items || [];
    console.log('Email messages fetched:', messages.length);
    
    // Filter by From header if specified
    if (options.fromFilter) {
        messages = messages.filter(message => {
            if (message.Content && message.Content.Headers && message.Content.Headers.From) {
                const fromEmail = message.Content.Headers.From[0];
                return fromEmail.includes(options.fromFilter);
            }
            return false;
        });
    }
    
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

// Configuration: Message type and target identifiers
let messageType;
try {
    messageType = MESSAGE_TYPE || 'sms';
} catch (e) {
    messageType = 'sms';
}

let phoneNumber;
try {
    phoneNumber = PHONE_NUMBER || null;
} catch (e) {
    phoneNumber = null;
}

let emailAddress;
try {
    emailAddress = EMAIL_ADDRESS || null;
} catch (e) {
    emailAddress = null;
}

console.log('=== OTP Helper Configuration ===');
console.log('Message type:', messageType);
console.log('Max attempts:', MAX_ATTEMPTS);
console.log('Retry delay:', RETRY_DELAY + 'ms');
console.log('================================');

// Debug: Log what environment variables are available
console.log('\nAvailable environment variables:');
console.log('- MESSAGE_TYPE:', messageType !== 'sms' ? 'exists' : 'missing (using default: sms)');
console.log('- PHONE_NUMBER:', phoneNumber ? 'exists' : 'missing');
console.log('- EMAIL_ADDRESS:', emailAddress ? 'exists' : 'missing');

console.log('\nEnvironment values:');
console.log('- MESSAGE_TYPE value:', messageType);
console.log('- PHONE_NUMBER value:', phoneNumber);
console.log('- EMAIL_ADDRESS value:', emailAddress);

// Main execution logic - route to SMS or Email based on MESSAGE_TYPE
if (messageType.toLowerCase() === 'email') {
    console.log('\n=== EMAIL MODE ===');
    
    if (!emailAddress) {
        console.log('Warning: EMAIL_ADDRESS not provided, falling back to latest email without email filtering');
        output.otp = getLatestEmailVerificationCodeFallback(MAX_ATTEMPTS, RETRY_DELAY);
    } else {
        console.log('Using email address filtering for:', emailAddress);
        output.otp = getLatestEmailVerificationCode(emailAddress, MAX_ATTEMPTS, RETRY_DELAY);
    }
    
} else {
    console.log('\n=== SMS MODE ===');
    
    if (!phoneNumber) {
        console.log('Warning: PHONE_NUMBER not provided, falling back to latest SMS without phone filtering');
        output.otp = getLatestVerificationCodeFallback(MAX_ATTEMPTS, RETRY_DELAY);
    } else {
        console.log('Using phone number filtering for:', phoneNumber);
        output.otp = getLatestVerificationCode(phoneNumber, MAX_ATTEMPTS, RETRY_DELAY);
    }
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