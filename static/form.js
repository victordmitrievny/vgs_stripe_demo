// Define VGS form submission using VGScollect library
const vgsForm = window.VGSCollect.create(
  'tnt491nnxg5',
  'sandbox', 
  (state) => {}).setRouteId('');

const css = {
  boxSizing: 'border-box',
  fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI"',
  color: '#000000',
  '&::placeholder': {
    color: '#bcbcbc'
  }
};

const cardHolder = vgsForm.field('#cc-holder', {
  type: 'text',
  name: 'card_holder',
  placeholder: 'John Doe',
  validations: ['required'],
  css: css,
  });

const cardNumber = vgsForm.field('#cc-number', {
  type: 'card-number',
  name: 'card_number',
  placeholder: '4111 1111 1111 1111',
  showCardIcon: true,
  validations: ['required', 'validCardNumber'],
  css: css,
  });

const cardSecurityCode = vgsForm.field('#cc-cvc', {
  type: 'card-security-code',
  name: 'card_cvc',
  placeholder: '123',
  showCardIcon: true,
  validations: ['required', 'validCardSecurityCode'],
  css: css,
  });

const cardExpDate = vgsForm.field('#cc-expiration-date', {
  type: 'card-expiration-date',
  name: 'card_exp',
  placeholder: 'MM / YY',
  validations: ['required', 'validCardExpirationDate'],
  css: css,
  });

const submitVGSCollectForm = () => {
  // Show loading circle
  document.getElementById('loading-circle').style.display = 'block';
  // Submit data
  vgsForm.submit('/post', {}, (status, data) => {
    if (status >= 200 && status <= 300) {
      // Redirect to a new page based on the response status
      if (data.status === 'Authorised') { 
        window.location.href = '/payment-success';
      } else {
        window.location.href = '/payment-failure';
      }
    } else if (!status) {
        // Network Error occurred
        console.error('Network Error: Please check your internet connection.');
    } else {
        // Server Error
        console.error('Server Error: Status ' + status);
    }
  }, (validationError) => {
    // Form validation error
    console.error('Form Validation Error:', validationError);
  });
}

// Listen for data submission
document.getElementById('vgs-collect-form').addEventListener('submit', (e) => {
  e.preventDefault();
  submitVGSCollectForm();
}); 
