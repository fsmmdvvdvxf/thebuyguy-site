/* The only file you edit to change how bookings are delivered. */
window.ORDA_BOOKING_CONFIG = {
  // "formsubmit" needs no signup: the first submission triggers a one-time
  // activation email to FORMSUBMIT_EMAIL, and bookings flow after that click.
  // "web3forms" keeps the address out of this public file but needs an access
  // key from web3forms.com. Switching is this one line plus the key below.
  PROVIDER: "formsubmit",
  ENDPOINT: "https://api.web3forms.com/submit",
  ACCESS_KEY: "REPLACE_WITH_WEB3FORMS_ACCESS_KEY",

  // Used only when PROVIDER is "formsubmit"
  FORMSUBMIT_EMAIL: "ordaformaofficial@gmail.com",

  OWNER_EMAIL: "ordaformaofficial@gmail.com",
  TIMEZONE: "America/Chicago",
  SLOT_MINUTES: 30
};
