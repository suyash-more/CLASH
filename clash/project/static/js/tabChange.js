let SECRET = "CLASHRCISTHEBEST";
const simpleCrypto = new SimpleCrypto(SECRET);
const randomString = "9769c8ce900ff047";

const checkTabChange = (attemptNo) => {
  if (attemptNo === 0) {
    window.location.href = `${window.location.origin}/logout/`;
  } else {
    alert(
      "WARNING: Please do not change tabs or swtich windows. Doing this once more will lead to disqualification."
    );
  }
};

window.onblur = () => {
  let attempts = localStorage.getItem(randomString);
  if (attempts === null) {
    let encrypted2 = simpleCrypto.encrypt("2");
    localStorage.setItem(randomString, encrypted2);
  } else {
    let attemptNo = localStorage.getItem(randomString);
    attemptNo = parseInt(simpleCrypto.decrypt(attemptNo));
    checkTabChange(attemptNo);
    attemptNo--;
    let encrypted2 = simpleCrypto.encrypt(attemptNo.toString());
    localStorage.setItem(randomString, encrypted2);
  }
};
