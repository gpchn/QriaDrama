function greet(name) {
  pywebview.api.greet(name).then((response) => {
    document.getElementById("result").innerText = response;
  });
}
