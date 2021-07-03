async function checkQuestions() {
  searchValue = document.getElementById("searchInput").value;
  console.log(searchValue.toLowerCase());
  const response = await fetch(
    // "http://127.0.0.1:8000/api/question-list-top-five/" +
    "https://quora-final.herokuapp.com/api/question-list-top-five/" +
      new URLSearchParams({
        search_query: searchValue,
      })
  );
  const data = await response.json();
  var list = document.getElementById("api_unordered_list");
  data.forEach((element) => {
    if (list.getElementsByTagName("li").length !== 0) {
      for (var i = 0; i < list.getElementsByTagName("li").length; i++) {
        list.removeChild(list.childNodes[i]);
      }
    }
    console.log(element.title);
    var node = document.createElement("LI"); // Create a <li> node
    const temp = element.id + ":: " + element.title;
    var textnode = document.createTextNode(temp); // Create a text node

    node.appendChild(textnode); // Append the text to <li>
    list.appendChild(node);
  });
}
