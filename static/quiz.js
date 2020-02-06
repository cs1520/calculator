// Creates an empty XMLHTTP request that we will add form values to
function createEmptyRequest() {
  let xmlhttp;
  if (window.XMLHttpRequest) {
    xmlhttp = new XMLHttpRequest();
  } else {
    xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
  }
  if (!xmlhttp) {
    alert("Your browser does not support AJAX!");
  }
  return xmlhttp;
}

function autocompleteName(peoplesoft_id) {
  let xmlhttp = createEmptyRequest();
  let targetUrl = "/student/" + peoplesoft_id;

  xmlhttp.onreadystatechange = function() {
    if (xmlhttp.readyState == 4) {
      // Response code for AJAX call
      console.log(xmlhttp.status);
      if (xmlhttp.status === 404) {
        return;
      }
      try {
        let response = JSON.parse(xmlhttp.responseText);
        document.getElementById("student-name").value = response["name"];
        document.getElementById("student-email").value = response["email"];
      } catch (exc) {
        console.error("There was a problem at the server.");
      }
    }
  };

  xmlhttp.open("GET", targetUrl, true);
  xmlhttp.send();
}
