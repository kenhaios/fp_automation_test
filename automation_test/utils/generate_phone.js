// Generate random 10-digit phone number
function generateRandomPhone() {
  const firstDigit = Math.floor(Math.random() * 9) + 1; // 1-9
  const restDigits = Array.from({length: 9}, () => Math.floor(Math.random() * 10));
  return firstDigit + restDigits.join('');
}

const phoneNumber = generateRandomPhone();

// Output as JSON - Maestro will parse this
console.log(JSON.stringify({ 
  generatedPhone: phoneNumber 
}));

// OR simple key-value format (alternative)
// console.log(`generatedPhone: ${phoneNumber}`);
output.generatedPhone = phoneNumber;