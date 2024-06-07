
DEFAULT_CONSENT = {
    'analytics_storage': 'denied',
}
COOKIE_FSD_CONSENT = "fsd_cookie_consent";

function readConsentCookie() {
    cookies = document.cookie.split(";")
    for (i=0; i<cookies.length; i++) {
        let c = cookies[i];
        if (c.split("=")[0].trim() == COOKIE_FSD_CONSENT){
            let value = c.substring(c.indexOf("=")+1);
            return JSON.parse(value);
        }
    }
    return null;
}

function updateCookieConsent(newValue) {
    console.info("in update consent with value " + newValue);
    gtag('consent', 'update', {
        'analytics_storage': newValue
    });
    consentObj = {...DEFAULT_CONSENT}
    consentObj.analytics_storage = newValue;
    document.cookie = COOKIE_FSD_CONSENT + "=" + JSON.stringify(consentObj) + ";path=/";

}

function acceptCookies() {
    console.debug("Accepted cookies");
    updateCookieConsent('granted');
    document.getElementById("cookies-choice-msg").setAttribute("hidden", "true");
    document.getElementById("cookies-accepted-msg").removeAttribute("hidden");
}

function denyCookies() {
    console.debug("Rejected cookies");
    updateCookieConsent('denied');
    document.getElementById("cookies-choice-msg").setAttribute("hidden", "true");
    document.getElementById("cookies-rejected-msg").removeAttribute("hidden");
}

function hideCookiesMessage(){
    document.getElementById("cookie-banner").setAttribute("hidden", "true");
}

function saveAnalyticsPrefs(){
  if(document.getElementById("cookies-analytics").checked == true){
    updateCookieConsent('granted');
    hideCookiesMessage();
  } else {
    updateCookieConsent('denied');
    hideCookiesMessage();
  }
}
